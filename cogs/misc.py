# misc.py

import asyncio
from decimal import Decimal, ROUND_HALF_UP

import discord
from discord.commands import slash_command, SlashCommandGroup, Option
from discord.ext import commands

import database
from resources import emojis, functions, settings, strings


class MiscCog(commands.Cog):
    """Cog with miscellanous commands"""
    def __init__(self, bot):
        self.bot = bot

    # Commands
    @slash_command(description='All current redeemable codes')
    async def codes(self, ctx: discord.ApplicationContext) -> None:
        """Codes"""
        embed = await embed_codes()
        await ctx.respond(embed=embed)

    @slash_command(description='All badges and how to unlock them')
    async def badges(self, ctx: discord.ApplicationContext) -> None:
        """Badges"""
        embed = await embed_badges()
        await ctx.respond(embed=embed)

    cmd_coolness = SlashCommandGroup("coolness", "Coolness commands")
    @cmd_coolness.command(name='guide', description='How to get coolness')
    async def coolness_guide(self, ctx: discord.ApplicationContext) -> None:
        """Coolness guide"""
        embed = await embed_coolness_guide()
        await ctx.respond(embed=embed)

    cmd_farming = SlashCommandGroup("farming", "Farming commands")
    @cmd_farming.command(name='guide', description='How farming works and what do with crops')
    async def farming_guide(self, ctx: discord.ApplicationContext) -> None:
        """Farming guide"""
        embed = await embed_farming_guide()
        await ctx.respond(embed=embed)

    cmd_beginner = SlashCommandGroup("beginner", "Beginner commands")
    @cmd_beginner.command(name='guide', description='How to start in the game')
    async def beginner_guide(self, ctx: discord.ApplicationContext) -> None:
        """Beginner guide"""
        embed = await embed_beginner_guide()
        await ctx.respond(embed=embed)

    @slash_command(description='A handy dandy random tip')
    async def tip(
        self,
        ctx: discord.ApplicationContext,
        id: Option(int, 'ID of a specific tip. Returns a random tip if empty.', min_value=1,
                   max_value=1000, default=None)
        ) -> None:
        """Tip"""
        try:
            tip: database.Tip = await database.get_tip(id)
        except database.NoDataFound:
            await ctx.respond('There is no tip with that ID', ephemeral=True)
            return
        embed = discord.Embed(
            color = settings.EMBED_COLOR,
            title = f'TIP {tip.id}',
            description = tip.tip
        )
        await ctx.respond(embed=embed)

    @slash_command(description='A basic calculator for your mathematical needs')
    async def calculator(
        self,
        ctx: discord.ApplicationContext,
        calculation: Option(str, 'The calculation you want solved')
        ) -> None:
        """Basic calculator"""
        def formatNumber(num):
            if num % 1 == 0:
                return int(num)
            else:
                num = num.quantize(Decimal('1.1234567890'), rounding=ROUND_HALF_UP)
                return num

        allowedchars = set('1234567890.-+/*%()')
        if not set(calculation).issubset(allowedchars) or '**' in calculation:
            await ctx.respond(
                f'Invalid characters. Please only use numbers and supported operators.\n'
                f'Supported operators are `+`, `-`, `/`, `*` and `%`.',
                ephemeral=True
            )
            return
        error_parsing = (
            f'Error while parsing your input. Please check your input.\n'
            f'Supported operators are `+`, `-`, `/`, `*` and `%`.'
        )
        # Parse open the calculation, convert all numbers to float and store it as a list
        # This is necessary because Python has the annoying habit of allowing infinite integers which can completely lockup a system. Floats have overflow protection.
        pos = 1
        calculation_parsed = []
        number = ''
        last_char_was_operator = False # Not really accurate name, I only use it to check for *, % and /. Multiple + and - are allowed.
        last_char_was_number = False
        calculation_sliced = calculation
        try:
            while pos != len(calculation) + 1:
                slice = calculation_sliced[0:1]
                allowedcharacters = set('1234567890.-+/*%()')
                if set(slice).issubset(allowedcharacters):
                    if slice.isnumeric():
                        if last_char_was_number:
                            number = f'{number}{slice}'
                        else:
                            number = slice
                            last_char_was_number = True
                        last_char_was_operator = False
                    else:
                        if slice == '.':
                            if number == '':
                                number = f'0{slice}'
                                last_char_was_number = True
                            else:
                                number = f'{number}{slice}'
                        else:
                            if number != '':
                                calculation_parsed.append(Decimal(float(number)))
                                number = ''

                            if slice in ('*','%','/'):
                                if last_char_was_operator:
                                    await ctx.respond(error_parsing, ephemeral=True)
                                    return
                                else:
                                    calculation_parsed.append(slice)
                                    last_char_was_operator = True
                            else:
                                calculation_parsed.append(slice)
                                last_char_was_operator = False
                            last_char_was_number = False
                else:
                    await ctx.respond(error_parsing, ephemeral=True)
                    return

                calculation_sliced = calculation_sliced[1:]
                pos += 1
            else:
                if number != '':
                    calculation_parsed.append(Decimal(float(number)))
        except:
            await ctx.respond(error_parsing, ephemeral=True)
            return

        # Reassemble and execute calculation
        calculation_reassembled = ''
        for slice in calculation_parsed:
            calculation_reassembled = f'{calculation_reassembled}{slice}'
        try:
            result = eval(calculation_reassembled)
            result = Decimal(eval(calculation_reassembled))
            result = formatNumber(result)
            if isinstance(result, int):
                result = f'{result:,}'
            else:
                result = f'{result:,}'.rstrip('0').rstrip('.')
            if not len(result) > 2000:
                await ctx.respond(result)
                return
            else:
                await ctx.respond('Well. Whatever you calculated, the result is too long to display. GG.')
                return
        except:
            await ctx.respond(
                f'Well, _that_ didn\'t calculate to anything useful.\n'
                f'What were you trying to do there? :thinking:'
            )
            return

    cmd_coincap = SlashCommandGroup("coincap", "Coincap commands")
    @commands.bot_has_permissions(view_channel=True)
    @commands.guild_only()
    @cmd_coincap.command(name='calculator', description='Calculate the coin cap for a TT/area')
    async def coincap_calculator(
        self,
        ctx: discord.ApplicationContext,
        time_travel: Option(int, 'The TT you want to calculate for. Reads from EPIC RPG if empty.',
                            min_value=1, max_value=999, default=None),
        area: Option(int, 'The area you want to calculate for. Reads from EPIC RPG if empty.',
                     min_value=1, max_value=20, default=None),
    ) -> None:
        if time_travel is None or area is None:
            bot_message_task = asyncio.ensure_future(functions.wait_for_profile_message(self.bot, ctx))
            try:
                bot_message = await functions.wait_for_bot_or_abort(ctx, bot_message_task, 'rpg p')
            except asyncio.TimeoutError:
                await ctx.respond(strings.MSG_BOT_MESSAGE_NOT_FOUND.format(user=ctx.author.name, information='profile'))
                return
            if bot_message is None: return
            tt_found, area_found = await functions.extract_progress_data_from_profile_embed(ctx, bot_message)
            if time_travel is None: time_travel = tt_found
            if area is None: area = area_found

        coin_cap = pow(time_travel, 4) * 500_000_000 + pow(area, 2) * 100_000
        if area == 1: coin_cap += 1

        await ctx.respond(
            f'**{ctx.author.name}**, the coin cap for **TT {time_travel}**, **area {area}** is '
            f'**{coin_cap:,}** {emojis.COIN} coins.\n'
            f'You can not receive coins with `give`, `multidice` or `miniboss` if you would exceed this cap.'
        )


# Initialization
def setup(bot):
    bot.add_cog(MiscCog(bot))


# --- Embeds ---
async def embed_codes():
    """Redeemable codes"""
    temporary_value = temporary_value_2 = permanent_value = ''
    second_event_field = False
    codes = await database.get_all_codes()
    for code in codes:
        if code.temporary:
            if second_event_field:
                temporary_value_2 = f'{temporary_value_2}\n{emojis.BP} `{code.code}`{emojis.BLANK}{code.contents}'
            else:
                temporary_value_check = f'{temporary_value}\n{emojis.BP} `{code.code}`{emojis.BLANK}{code.contents}'
                if len(temporary_value_check) > 1024:
                    temporary_value_2 = f'{emojis.BP} `{code.code}`{emojis.BLANK}{code.contents}'
                    second_event_field = True
                else:
                    temporary_value = f'{temporary_value}\n{emojis.BP} `{code.code}`{emojis.BLANK}{code.contents}'
        else:
            permanent_value = f'{permanent_value}\n{emojis.BP} `{code.code}`{emojis.BLANK}{code.contents}'
    if permanent_value == '': permanent_value = f'{emojis.BP} No codes currently known'
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'REDEEMABLE CODES',
        description = (
            f'Use these codes with `rpg code` to get some free goodies.\n'
            f'Every code can only be redeemed once.'
        )
    )
    embed.set_footer(text=strings.DEFAULT_FOOTER)
    if temporary_value != '':
        embed.add_field(name='EVENT CODES', value=temporary_value, inline=False)
    if second_event_field:
        embed.add_field(name='MORE EVENT CODES', value=temporary_value_2, inline=False)
    embed.add_field(name='PERMANENT CODES', value=permanent_value, inline=False)
    return embed


async def embed_badges() -> discord.Embed:
    """Badges"""
    badges_coolness = (
        f'{emojis.BP} {emojis.BADGE_C1} : Unlocked with 1 {emojis.STAT_COOLNESS} coolness\n'
        f'{emojis.BP} {emojis.BADGE_C100} : Unlocked with 100 {emojis.STAT_COOLNESS} coolness\n'
        f'{emojis.BP} {emojis.BADGE_C200} : Unlocked with 200 {emojis.STAT_COOLNESS} coolness\n'
        f'{emojis.BP} {emojis.BADGE_C500} : Unlocked with 500 {emojis.STAT_COOLNESS} coolness\n'
        f'{emojis.BP} {emojis.BADGE_C1000} : Unlocked with 1,000 {emojis.STAT_COOLNESS} coolness\n'
        f'{emojis.BP} {emojis.BADGE_C2000} : Unlocked with 2,000 {emojis.STAT_COOLNESS} coolness\n'
        f'{emojis.BP} {emojis.BADGE_C5000} : Unlocked with 5,000 {emojis.STAT_COOLNESS} coolness\n'
        f'{emojis.BP} {emojis.BADGE_C10000} : Unlocked with 10,000 {emojis.STAT_COOLNESS} coolness\n'
        f'{emojis.BP} {emojis.BADGE_C20000} : Unlocked with 20,000 {emojis.STAT_COOLNESS} coolness\n'
    )
    badges_achievements = (
        f'{emojis.BP} {emojis.BADGE_A10} : Unlocked with 10 achievements\n'
        f'{emojis.BP} {emojis.BADGE_A25} : Unlocked with 25 achievements\n'
        f'{emojis.BP} {emojis.BADGE_A75} : Unlocked with 75 achievements\n'
        f'{emojis.BP} {emojis.BADGE_A125} : Unlocked with 125 achievements\n'
        f'{emojis.BP} {emojis.BADGE_A175} : Unlocked with 175 achievements\n'
        f'{emojis.BP} {emojis.BADGE_A225} : Unlocked with 225 achievements\n'
    )
    badges_other = (
        f'{emojis.BP} {emojis.BADGE_AREA15} : Unlocked by reaching area 15 ({emojis.TIME_TRAVEL} TT 10)\n'
        f'{emojis.BP} {emojis.BADGE_TOP} : Unlocked by beating D15-2 and reaching the TOP\n'
        f'{emojis.BP} {emojis.BADGE_EPIC_NPC} : Unlocked by beating the "final" fight in the TOP\n'
        f'{emojis.BP} {emojis.BADGE_OMEGA} : Unlock requirements unknown\n'
        f'{emojis.BP} {emojis.BADGE_GODLY} : Unlock requirements unknown\n'
    )
    howtouse = (
        f'{emojis.BP} Use `rpg badge list` to get the ID of the badges you want\n'
        f'{emojis.BP} Use `rpg badge claim [ID]` to claim a badge\n'
        f'{emojis.BP} Use `rpg badge select [ID]` to activate or deactivate a badge'
    )
    note = (
        f'{emojis.BP} You can have 3 badges active (5 with a {emojis.HORSE_T10} T10 horse)\n'
        f'{emojis.BP} You can only claim badges you have unlocked\n'
        f'{emojis.BP} If you don\'t know how to get coolness, see `/coolness guide`'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'BADGES',
        description = 'Badges are cosmetic only profile decorations.'
    )
    embed.set_footer(text=strings.DEFAULT_FOOTER)
    embed.add_field(name='ACHIEVEMENT BADGES', value=badges_achievements, inline=False)
    embed.add_field(name='COOLNESS BADGES', value=badges_coolness, inline=False)
    embed.add_field(name='OTHER BADGES', value=badges_other, inline=False)
    embed.add_field(name='HOW TO USE', value=howtouse, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_coolness_guide() -> discord.Embed:
    """Coolness guide"""
    usage = (
        f'{emojis.BP} Unlocks cosmetic only profile badges (see `/badges`)\n'
        f'{emojis.BP} You need at least 2,000 coolness for dungeon 15-2'
    )
    req = f'{emojis.BP} Unlocks when you reach area 12 in {emojis.TIME_TRAVEL}TT 1'
    howtoget = (
        f'{emojis.BP} `ultraining` awards 2 coolness per stage (see `/ultraining guide`)\n'
        f'{emojis.BP} Do an adventure with full HP and survive with 1 HP\n'
        f'{emojis.BP} Open {emojis.LB_OMEGA} OMEGA and {emojis.LB_GODLY} GODLY lootboxes\n'
        f'{emojis.BP} Get HYPER, ULTRA or ULTIMATE logs from work commands\n'
        f'{emojis.BP} Forge ULTRA-EDGY or higher gear\n'
        f'{emojis.BP} Ascend a pet\n'
        f'{emojis.BP} Do other \'cool\' actions that are currently unknown'
    )
    note = (
        f'{emojis.BP} You don\'t lose coolness when you time travel\n'
        f'{emojis.BP} You can get coolness in every area once it\'s unlocked\n'
        f'{emojis.BP} If you have 100+, you get less (except from `ultraining`)\n'
        f'{emojis.BP} You can check your coolness by using `ultraining p`\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'COOLNESS {emojis.STAT_COOLNESS}',
        description = 'Coolness is a stat you start collecting once you reach area 12.'
    )
    embed.set_footer(text=strings.DEFAULT_FOOTER)
    embed.add_field(name='USAGE', value=usage, inline=False)
    embed.add_field(name='REQUIREMENTS', value=req, inline=False)
    embed.add_field(name='HOW TO GET COOLNESS', value=howtoget, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_farming_guide() -> discord.Embed:
    """Farming guide"""
    planting_normal = (
        f'{emojis.BP} Use `rpg farm` to plant {emojis.SEED} seeds. Buy seeds in the shop for 4,000 coins.\n'
        f'{emojis.BP} This gives you XP and either {emojis.BREAD} bread, {emojis.CARROT} carrots or '
        f'{emojis.POTATO} potatoes\n'
        f'{emojis.BP} You have a 4% chance to receive special seeds (see below)\n'
        f'{emojis.BP} The cooldown of the command is 10m (donor reduction applies)'
    )
    planting_special = (
        f'{emojis.BP} There are three special seeds: {emojis.SEED_BREAD} bread, {emojis.SEED_CARROT} carrot and '
        f'{emojis.SEED_POTATO} potato seed\n'
        f'{emojis.BP} You can plant them with `rpg farm [type]` (e.g. `rpg farm carrot`)\n'
        f'{emojis.BP} The crop will be the same type (e.g. a {emojis.SEED_CARROT} carrot seed gives you '
        f'{emojis.CARROT} carrots)\n'
        f'{emojis.BP} You have a 65% chance to get 1 seed and a 10% chance to get 2 seeds back'
    )
    usage_bread = (
        f'{emojis.BP} {emojis.SWORD_HAIR} `Hair Sword` ➜ 4 {emojis.MERMAID_HAIR} + **220** {emojis.BREAD}\n'
        f'{emojis.BP} {emojis.ARMOR_ELECTRONICAL} `Electronical Armor` ➜ 12 {emojis.CHIP} + 1 {emojis.LOG_HYPER} + '
        f'**180** {emojis.BREAD}\n'
        f'{emojis.BP} {emojis.FOOD_CARROT_BREAD} `Carrot Bread` (+1 Level) ➜ **1** {emojis.BREAD} + '
        f'160 {emojis.CARROT}\n'
        f'{emojis.BP} Can be sold for 3,000 coins and 3 merchant XP\n'
        f'{emojis.BP} Heals the player and gives a temporary +5 LIFE when eaten (`rpg eat bread`)'
    )
    usage_carrot = (
        f'{emojis.BP} {emojis.FOOD_CARROT_BREAD} `Carrot Bread` (+1 Level) ➜ 1 {emojis.BREAD} + **160** '
        f'{emojis.CARROT}\n'
        f'{emojis.BP} {emojis.FOOD_ORANGE_JUICE} `Orange Juice` (+3 AT, +3 DEF) ➜ **320** {emojis.CARROT}\n'
        f'{emojis.BP} {emojis.FOOD_CARROTATO_CHIPS} `Carrotato Chips` (+25 random profession XP) ➜ 80 {emojis.POTATO} '
        f'+ **80** {emojis.CARROT}\n'
        f'{emojis.BP} Can be sold for 2,500 coins and 3 merchant XP\n'
        f'{emojis.BP} Can be used to change the horse name with `rpg horse feed`'
    )
    usage_potato = (
        f'{emojis.BP} {emojis.SWORD_RUBY} `Ruby Sword` ➜ 4 {emojis.RUBY} + 1 {emojis.LOG_MEGA} + **36** '
        f'{emojis.POTATO}\n'
        f'{emojis.BP} {emojis.ARMOR_RUBY} `Ruby Armor` ➜ 7 {emojis.RUBY} + 4 {emojis.UNICORN_HORN} + **120** '
        f'{emojis.POTATO} + 2 {emojis.LOG_MEGA}\n'
        f'{emojis.BP} {emojis.SWORD_ELECTRONICAL} `Electronical Sword` ➜ 8 {emojis.CHIP} + 1 {emojis.LOG_MEGA} '
        f'+ **140** {emojis.POTATO}\n'
        f'{emojis.BP} {emojis.SWORD_WATERMELON} `Watermelon Sword` ➜ 1 {emojis.WATERMELON} + **10** {emojis.POTATO}\n'
        f'{emojis.BP} {emojis.FOOD_CARROTATO_CHIPS} `Carrotato Chips` (+25 random profession XP) '
        f'➜ **80** {emojis.POTATO} + 80 {emojis.CARROT}\n'
        f'{emojis.BP} Can be sold for 2,000 coins and 3 merchant XP'
    )
    stt_score = (
        f'{emojis.BP} 25 {emojis.BREAD} bread = 1 score\n'
        f'{emojis.BP} 30 {emojis.CARROT} carrots = 1 score\n'
        f'{emojis.BP} 35 {emojis.POTATO} potatoes = 1 score\n'
    )
    what_to_plant = (
        f'{emojis.BP} If you want to cook food for levels or stats: {emojis.CARROT} carrots\n'
        f'{emojis.BP} If you want to get more coins or a higher STT score: {emojis.BREAD} bread\n'
        f'{emojis.BP} If you want to flex potatoes for some reason: {emojis.POTATO} potatoes'
    )
    note = (
        f'{emojis.BP} Farming is unlocked in area 4\n'
        f'{emojis.BP} The command can be used in area 1+ when ascended\n'
        f'{emojis.BP} The amount of items you gain increases with your TT\n'
        f'{emojis.BP} You can not farm in the TOP'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'FARMING',
        description = f'It ain\'t much, but it\'s honest work.'
    )
    embed.set_footer(text=strings.DEFAULT_FOOTER)
    embed.add_field(name='PLANTING NORMAL SEEDS', value=planting_normal, inline=False)
    embed.add_field(name='PLANTING SPECIAL SEEDS', value=planting_special, inline=False)
    embed.add_field(name='BREAD USAGE', value=usage_bread, inline=False)
    embed.add_field(name='CARROT USAGE', value=usage_carrot, inline=False)
    embed.add_field(name='POTATO USAGE', value=usage_potato, inline=False)
    embed.add_field(name='STT SCORE', value=stt_score, inline=False)
    embed.add_field(name='WHAT TO FARM?', value=what_to_plant, inline=False)
    embed.add_field(name='NOTE', value=note, inline=False)
    return embed


async def embed_beginner_guide() -> discord.Embed:
    """Beginner guide"""
    goal = (
        f'The goal is to advance until you reach your highest reachable area. At that point you can time travel.\n'
        f'Think of this as new game+. This resets your progress but unlocks more of the game. For more information '
        f'see `/timetravel guide`.\n'
        f'To check out the available commands in this game, use `rpg start` and `rpg help`.'
    )
    areas_dungeons = (
        f'You advance by moving through areas. You can check what you should do in each area in the area guides '
        f'(see `/area guide`).\n'
        f'To leave an area and advance to the next one you have to beat the dungeon for that area (so to leave area 1 '
        f'you do dungeon 1).\n'
        f'Dungeons 1 to 9 are simple tank and spank affairs, there is no gear check. So, if needed, you can enter them '
        f'undergeared and get carried.\n'
        f'**This does not work for dungeons 10+**. To enter those you **need** to have certain gear.'
    )
    first_run = (
        f'Your first run is called TT0 (time travel 0) because you haven\'t time traveled yet. In TT0 you need to '
        f'reach area 11 which means you need to beat dungeon 10.\n'
        f'Now, as mentioned, D10 has gear requirements, so you can not cheese that dungeon, you **need** to craft '
        f'the following gear:\n'
        f'{emojis.SWORD_EDGY} EDGY Sword (requires 1 {emojis.LOG_ULTRA} ULTRA log)\n'
        f'{emojis.ARMOR_EDGY} EDGY Armor (requires a lot of mob drops)\n'
        f'The ULTRA log needed for the sword equals 250,000 wooden logs and the mob drops for the armor are pretty '
        f'rare (see `/monster drops`).\n'
        f'This means that your main goal in TT0 is to farm enough materials to be able to craft this shiny EDGY gear.'
    )
    grinding_trades = (
        f'Grinding all those materials takes time, so you want to do this smartly.\n'
        f'Trade rates are the single most important thing in this game to help you saving time. Every area has '
        f'different trade rates, so every time you advance, your trade rates change (see `/trade rates`). You can '
        f'**not** go back to earlier trade rates, these are tied to your highest unlocked area.\n'
        f'This means you can save a lot of time and materials if you farm **early** and exploit the trade rate '
        f'changes to multiply your inventory. See `/trade guide` for more trading info.\n'
        f'In TT0 the most important area is **area 5**. You want to stay there until you have the recommended '
        f'materials (see `/area guide 5`).\n'
        f'If you do this, you will save a ton of time later on and be able to craft that EDGY gear as soon as '
        f'you reach areas 9 and 10. Don\'t forget to check out the area guides for other recommendations.'
    )
    tips = (
        f'{emojis.BP} Yes, farming in area 5 is boring. But do not leave the area early, you **will** regret it.\n'
        f'{emojis.BP} Do not craft the EDGY Sword before area 10. You will lose materials if you do.'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'STARTER GUIDE',
        description = 'Welcome to EPIC RPG! This is a guide to help you out with your first run.'
    )
    embed.set_footer(text=strings.DEFAULT_FOOTER)
    embed.add_field(name='GOAL OF THE GAME', value=goal, inline=False)
    embed.add_field(name='AREAS & DUNGEONS', value=areas_dungeons, inline=False)
    embed.add_field(name='YOUR FIRST RUN', value=first_run, inline=False)
    embed.add_field(name='GRINDING & TRADES', value=grinding_trades, inline=False)
    embed.add_field(name='TIPS', value=tips, inline=False)
    return embed