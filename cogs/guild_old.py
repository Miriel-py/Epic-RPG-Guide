# guilds.py

import discord
from discord.ext import commands

from resources import emojis
from resources import settings
from resources import functions


# Guild commands (cog)
class GuildOldCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    guild_aliases = (
        'guilds',
        'stealth',
        'energy',
        'guildstealth',
        'guildenergy',
        'guildreward',
        'guildrewards',
        'guildweekly',
        'guildcmd',
        'guildcommand',
        'guildcommands',
        'guildstat',
        'guildstats',
        'guildshop',
        'omegahorsetoken',
        'omegatoken',
        'guildomegatoken',
        'guildomegahorsetoken',
        'guildhorsetoken',
        'cookierain',
        'guildcookierain',
        'guildrain',
        'guildbuff',
        'guildbuy',
        'guildlevel',
        'guildlvl',
        'guildprogress',
        'magicchair',
        'guildtask',
        'guildtasks',
    )

    # Command "guild"
    @commands.command(aliases=guild_aliases)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def guild(self, ctx, *args):
        prefix = ctx.prefix
        invoked = ctx.invoked_with
        invoked = invoked.lower().replace(prefix,'')
        level_strings = ('level','progress','lvl')
        stat_strings = ('stat','stealth','energy')
        shop_strings = ('shop','omega','horse','cookie','rain','token','buff','buy')

        if args:
            args = [arg.lower() for arg in args]
            all_args = "".join(args)

            if any(string in all_args for string in level_strings):
                embed = await embed_guild_progress(prefix)
                await ctx.send(embed=embed)
                return
            elif any(string in all_args for string in stat_strings):
                embed = await embed_guild_stats(prefix)
                await ctx.send(embed=embed)
                return
            elif 'weekly' in all_args or 'reward' in all_args:
                embed = await embed_guild_weekly(prefix)
                await ctx.send(embed=embed)
                return
            elif 'task' in all_args:
                embed = await embed_guild_tasks(prefix)
                await ctx.send(embed=embed)
                return
            elif 'command' in all_args or 'cmd' in all_args:
                embed = await embed_guild_cmd(prefix)
                await ctx.send(embed=embed)
                return
            elif any(string in all_args for string in shop_strings):
                embed = await embed_guild_shop(prefix)
                await ctx.send(embed=embed)
                return
            else:
                embed = await embed_guild_overview(prefix)
                await ctx.send(embed=embed)
                return
        else:
            if any(string in invoked for string in level_strings):
                embed = await embed_guild_progress(prefix)
                await ctx.send(embed=embed)
                return
            elif any(string in invoked for string in stat_strings):
                embed = await embed_guild_stats(prefix)
                await ctx.send(embed=embed)
                return
            elif 'weekly' in invoked or 'reward' in invoked:
                embed = await embed_guild_weekly(prefix)
                await ctx.send(embed=embed)
                return
            elif 'task' in invoked:
                embed = await embed_guild_tasks(prefix)
                await ctx.send(embed=embed)
                return
            elif 'command' in invoked or 'cmd' in invoked:
                embed = await embed_guild_cmd(prefix)
                await ctx.send(embed=embed)
                return
            elif any(string in invoked for string in shop_strings):
                embed = await embed_guild_shop(prefix)
                await ctx.send(embed=embed)
                return
            else:
                embed = await embed_guild_overview(prefix)
                await ctx.send(embed=embed)
                return

# Initialization
def setup(bot):
    bot.add_cog(GuildOldCog(bot))


# --- Redundancies ---
# Raid & Upgrade
raid_upgrade = (
    f'{emojis.BP} Every member can start a raid **or** upgrade every 2 hours\n'
    f'{emojis.BP} This cooldown is shared among all members\n'
    f'{emojis.BP} Upgrading increases your {emojis.GUILD_STEALTH} stealth\n'
    f'{emojis.BP} Raiding increases your {emojis.GUILD_ENERGY} energy by raiding a random guild\n'
    f'{emojis.BP} The lower the {emojis.GUILD_STEALTH} stealth, the higher the chance to get raided\n'
    f'{emojis.BP} Guilds lose energy when they get raided, so get that stealth up!'
)

# Additional guides
guide_commands = '`{prefix}guild commands` : Guild hierarchy & commands'
guide_level = '`{prefix}guild level` : Guild levels and bonuses'
guide_shop = '`{prefix}guild shop` : The guild shop and what to buy'
guide_stats = '`{prefix}guild stats` : Stealth and energy'
guide_weekly = '`{prefix}guild weekly` : Weekly rewards and strategy'
guide_tasks = '`{prefix}guild tasks` : Weekly guild tasks and rewards'


# --- Embeds ---
# Guild main page
async def embed_guild_overview(prefix):

    requirements =  f'{emojis.BP} You need to reach area 4 once to create or join a guild'

    benefits = (
        f'{emojis.BP} A bonus on XP & coins when winning duels\n'
        f'{emojis.BP} Access to the guild shop\n'
        f'{emojis.BP} Allows you to get weekly rewards based on guild stats\n'
        f'{emojis.BP} Allows you to participate in completing weekly guild tasks\n'
    )

    how_to_join = (
        f'{emojis.BP} Use `rpg guild create` to create your own guild\n'
        f'{emojis.BP} Ask a guild owner to invite you in their guild'
    )

    guides = (
        f'{emojis.BP} {guide_commands.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_level.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_shop.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_stats.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_tasks.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_weekly.format(prefix=prefix)}\n'
    )


    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'GUILD',
        description = 'A guild is a group of up to 10 players that band together to unlock weekly rewards and duel bonuses.'

    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='REQUIREMENT', value=requirements, inline=False)
    embed.add_field(name='BENEFITS', value=benefits, inline=False)
    embed.add_field(name='HOW TO JOIN A GUILD', value=how_to_join, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Guild commands (guide)
async def embed_guild_cmd(prefix):

    owner = (
        f'{emojis.BP} `rpg guild buy` : Buy something from the guild shop\n'
        f'{emojis.BP} `rpg guild change owner` : Transfer guild ownership\n'
        f'{emojis.BP} `rpg guild create` : Create a guild\n'
        f'{emojis.BP} `rpg guild delete` : Delete a guild\n'
        f'{emojis.BP} `rpg guild invite` : Invite a player to your guild\n'
        f'{emojis.BP} `rpg guild kick` : Kick a player from your guild'
    )

    member = (
        f'{emojis.BP} `rpg guild leave` : Leave the guild\n'
        f'{emojis.BP} `rpg guild list` : List all members of the guild\n'
        f'{emojis.BP} `rpg guild raid` : Start a guild raid\n'
        f'{emojis.BP} `rpg guild ranking` : Opens the global guild leaderboard\n'
        f'{emojis.BP} `rpg guild shop` : Opens the guild shop\n'
        f'{emojis.BP} `rpg guild tasks` : Show/claim the weekly guild tasks\n'
        f'{emojis.BP} `rpg guild upgrade` : Upgrade guild {emojis.GUILD_STEALTH} stealth\n'
    )

    guides = (
        f'{emojis.BP} {guide_level.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_shop.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_stats.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_tasks.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_weekly.format(prefix=prefix)}\n'
    )


    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'GUILD HIERARCHY & COMMANDS',
        description = (
            f'Every guild has 1 owner and up to 9 members.\n'
            f'A lot of the guild commands can only be used by the owner.'
        )
    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='OWNER COMMANDS', value=owner, inline=False)
    embed.add_field(name='MEMBER COMMANDS', value=member, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Guild levelling & bonuses
async def embed_guild_progress(prefix):

    level_bonus = (
        f'{emojis.BP} The guild level increases the duel bonus\n'
        f'{emojis.BP} The duel bonus increases XP and coins you get when winning a duel\n'
        f'{emojis.BP} Each guild level increases the bonus by 2%\n'
        f'{emojis.BP} To level up the guild the members need to collect guild XP'
    )

    guild_xp = (
        f'{emojis.BP} Participate in the weekly contest (see `{prefix}guild weekly`)\n'
        f'{emojis.BP} Win duels against players **not** in your guild (1~3 XP)\n'
        f'{emojis.BLANK} To get 3 XP, duel against players +/- 50% of your level\n'
    )

    guides = (
        f'{emojis.BP} {guide_commands.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_shop.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_stats.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_tasks.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_weekly.format(prefix=prefix)}\n'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'GUILD LEVELS AND BONUSES',
        description = 'You can level up your guild to get an increasing duel bonus.'

    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='LEVEL / BONUS', value=level_bonus, inline=False)
    embed.add_field(name='HOW TO GET GUILD XP', value=guild_xp, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Guild shop
async def embed_guild_shop(prefix):

    rewards_old = (
        f'{emojis.BP} {emojis.GUILD_BUFF} **ENERGY buff**: Increases {emojis.GUILD_ENERGY} guild energy by 400  (2 {emojis.GUILD_COIN})\n'
        f'{emojis.BP} {emojis.CD_COOLDOWN} **Cooldown reset**: Resets the guild raid/upgrade cooldown (3 {emojis.GUILD_COIN})\n'
        f'{emojis.BP} {emojis.GUILD_LOOTBOXST} **Lootboxst**: All members get a random lootbox (up to EDGY) in duels for 24h (5 {emojis.GUILD_COIN})\n'
        f'{emojis.BP} {emojis.MAGIC_CHAIR} **Magic chair**: All EPIC RPG players get +20% lootbox drop chance for 45m (20 {emojis.GUILD_COIN}).\n'
        f'{emojis.BP} {emojis.OMEGA_HORSE_TOKEN} **OMEGA horse token**: All members get an {emojis.OMEGA_HORSE_TOKEN} OMEGA horse token which resets the horse breed/race cooldown (15 {emojis.GUILD_COIN})\n'
    )
    rewards_new = (
        f'{emojis.BP} {emojis.LB_EPIC} **EPIC lootbox**: 1 EPIC lootbox (4 {emojis.GUILD_RING})\n'
        f'{emojis.BP} {emojis.LB_EDGY} **EDGY lootbox**: 1 EDGY lootbox (20 {emojis.GUILD_RING})\n'
        f'{emojis.BP} {emojis.COOKIE_RAIN} **Cookie rain**: Up to 200 cookies (25 {emojis.GUILD_RING})\n'
        f'{emojis.BP} {emojis.SEED} **Special seed**: 1 bread, carrot or potato seed (35 {emojis.GUILD_RING})\n'
        f'{emojis.BP} {emojis.GUILD_ACHIEVEMENT} **Achievement**: Unlocks achievement `180` '
        f'(100 {emojis.GUILD_RING})\n'
        f'{emojis.BP} {emojis.OMEGA_HORSE_TOKEN} **Omega horse token**: Resets the horse breed/race cooldown '
        f'(150 {emojis.GUILD_RING})\n'
        f'{emojis.BP} {emojis.MAGIC_CHAIR} **Magic chair**: All players get +20% lootbox drop chance for 45m '
        f'(200 {emojis.GUILD_RING})\n'
        f'{emojis.BP} {emojis.GUILD_TOOTHBRUSH} **Legendary toothbrush**: Starts a lootbox summoning '
        f'(350 {emojis.GUILD_RING})\n'
    )

    guides = (
        f'{emojis.BP} {guide_commands.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_level.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_stats.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_tasks.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_weekly.format(prefix=prefix)}\n'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'GUILD SHOP',
        description = (
            f'The items in the guild shop cost {emojis.GUILD_RING} guild rings which you get by getting high enough '
            f'{emojis.GUILD_ENERGY} energy in the weekly guild event.\n'
            f'These rewards are personal and do not affect other guild members.\n\n'
            f'If your guild still has {emojis.GUILD_COIN} guild coins, the guild owner must spend **all** of them '
            f'to unlock the ring shop.'
        )
    )
    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='AVAILABLE REWARDS', value=rewards_new, inline=False)
    embed.add_field(name='OLD GUILD COIN REWARDS', value=rewards_old, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
    return embed

# Guild stats
async def embed_guild_stats(prefix):

    stealth = (
        f'{emojis.BP} Decreases the likelihood of getting raided by 1% per STEALTH\n'
        f'{emojis.BP} Can be increased by using `rpg guild upgrade`\n'
        f'{emojis.BP} Maximum amount is 95\n'
        f'{emojis.BP} Each upgrade gives you 0~7 stealth\n'
        f'{emojis.BLANK} The amount decreases the more you already have\n'
    )

    energy = (
        f'{emojis.BP} Energy determines your weekly rank and reward\n'
        f'{emojis.BP} You need 2,000 energy to get the max reward\n'
        f'{emojis.BP} Can be increased by using `rpg guild raid`\n'
        f'{emojis.BP} Ranking over 2,000 energy doesn\'t provide any additional rewards but is advised nonetheless so you stay over 2,000 in case you get raided'
    )

    guides = (
        f'{emojis.BP} {guide_commands.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_level.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_shop.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_tasks.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_weekly.format(prefix=prefix)}\n'
    )


    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'GUILD STATS',
        description = 'The guild stats are used to get the weekly rewards.'

    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name=f'STEALTH {emojis.GUILD_STEALTH}', value=stealth, inline=False)
    embed.add_field(name=f'ENERGY {emojis.GUILD_ENERGY}', value=energy, inline=False)
    embed.add_field(name='RAIDING & UPGRADING', value=raid_upgrade, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Guild weekly event
async def embed_guild_weekly(prefix):

    rewards = (
        f'{emojis.BP} 2,000 {emojis.GUILD_ENERGY}: 200 guild XP, 100 {emojis.GUILD_RING} guild rings\n'
        f'{emojis.BP} 1,000 {emojis.GUILD_ENERGY}: 150 guild XP, 50 {emojis.GUILD_RING} guild rings\n'
        f'{emojis.BP} 500 {emojis.GUILD_ENERGY}: 100 guild XP, 20 {emojis.GUILD_RING} guild rings\n'
        f'{emojis.BP} 250 {emojis.GUILD_ENERGY}: 75 guild XP\n'
        f'{emojis.BP} 100 {emojis.GUILD_ENERGY}: 50 guild XP\n'
        f'{emojis.BP} 50 {emojis.GUILD_ENERGY}: 25 guild XP\n'
        f'{emojis.BP} 10 {emojis.GUILD_ENERGY}: 5 guild XP'
    )

    strategy = (
        f'{emojis.BP} Increase your {emojis.GUILD_STEALTH} stealth to 95\n'
        f'{emojis.BP} Once your stealth is up, start raiding for the rest of the week\n'
    )

    schedule = f'{emojis.BP} Stats reset every Saturday 22:00 UTC'

    guides = (
        f'{emojis.BP} {guide_commands.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_level.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_shop.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_stats.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_tasks.format(prefix=prefix)}\n'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'WEEKLY GUILD REWARDS',
        description = (
            f'Once a week, you get rewards based on your {emojis.GUILD_ENERGY} energy. After that, your stats reset and you start over.\n'
            f'To increase your stats, raid or upgrade the guild.\n'
            f'To learn more about the stats, use `{prefix}guild stats`'
        )
    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='WEEKLY REWARDS', value=rewards, inline=False)
    embed.add_field(name='RAIDING & UPGRADING', value=raid_upgrade, inline=False)
    embed.add_field(name='STRATEGY', value=strategy, inline=False)
    embed.add_field(name='SCHEDULE', value=schedule, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed


async def embed_guild_tasks(prefix: str) -> discord.Embed:
    """Weekly guild tasks (40%, 100%, 200%)"""
    guild_tasks_1 = (
        f'{emojis.BP} Answer `16/40/80` EPIC guard questions correctly\n'
        f'{emojis.BP} Chop `48/120/240` MEGA logs\n'
        f'{emojis.BP} Complete `6/15/30` dungeons\n'
        f'{emojis.BP} Craft `12/30/60` swords or armors\n'
        f'{emojis.BP} Collect `800/2,000/4,000` profession XP\n'
        f'{emojis.BP} Complete `8/20/40` quests\n'
        f'{emojis.BP} Cook `30/75/150` recipes\n'
        f'{emojis.BP} Go on an adventure `48/120/240` times\n'
        f'{emojis.BP} Drop `40/100/200` lootboxes\n'
        f'{emojis.BP} Drop `40/100/200` monster items\n'
    )

    guild_tasks_2 = (
        f'{emojis.BP} Fish `6/15/30` EPIC fish\n'
        f'{emojis.BP} Gain `16/40/80` levels (outside random events)\n'
        f'{emojis.BP} Hunt `32/800/1,600` times\n'
        f'{emojis.BP} Obtain `20/50/100` special seeds\n'
        f'{emojis.BP} Open `72/180/360` lootboxes\n'
        f'{emojis.BP} Pick up `48/120/240` bananas\n'
        f'{emojis.BP} Raid `2/5/10` times for the guild\n'
        f'{emojis.BP} Trigger or start `12/30/60` random events\n'
        f'{emojis.BP} Vote for the bot `10/25/50` times\n'
        f'{emojis.BP} Win `20/50/100` duels\n'
    )

    rewards = (
        f'{emojis.BP} Stage 1: 10 {emojis.GUILD_RING} guild rings + 25 guild XP\n'
        f'{emojis.BP} Stage 2: 8 {emojis.GUILD_RING} guild rings + 20 guild XP\n'
        f'{emojis.BP} Stage 3: 6 {emojis.GUILD_RING} guild rings + 15 guild XP\n'
    )

    notes = (
        f'{emojis.BP} All guild members can contribute to these tasks\n'
        f'{emojis.BP} Guild tasks reset on monday, 00:00 UTC\n'
    )

    guides = (
        f'{emojis.BP} {guide_commands.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_level.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_shop.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_stats.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_weekly.format(prefix=prefix)}\n'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'GUILD TASKS',
        description = (
            f'Guild tasks have 3 stages and can be completed once a week.\n'
            f'Every guild gets 4 random tasks every week.'
        )

    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='POSSIBLE TASKS (I)', value=guild_tasks_1, inline=False)
    embed.add_field(name='POSSIBLE TASKS (II)', value=guild_tasks_2, inline=False)
    embed.add_field(name='REWARDS', value=rewards, inline=False)
    embed.add_field(name='NOTE', value=notes, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed