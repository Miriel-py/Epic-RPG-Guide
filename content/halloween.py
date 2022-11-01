# halloween.py
"""Contains all halloween guides"""

import discord

from resources import emojis, functions, settings, strings, views


# --- Topics ---
TOPIC_OVERVIEW = 'Overview'
TOPIC_CHANCES = 'Chances'
TOPIC_SCROLL_BOSS = 'Pumpkin bat (scroll boss)'

TOPICS = [
    TOPIC_OVERVIEW,
    TOPIC_CHANCES,
    TOPIC_SCROLL_BOSS,
]


# --- Commands ---
async def command_halloween_guide(ctx: discord.ApplicationContext, topic: str) -> None:
    """Horse festival guide command"""
    topics_functions = {
        TOPIC_OVERVIEW: embed_overview,
        TOPIC_CHANCES: embed_chances,
        TOPIC_SCROLL_BOSS: embed_scroll_boss,
    }
    view = views.TopicView(ctx, topics_functions, active_topic=topic)
    embed = await topics_functions[topic]()
    interaction = await ctx.respond(embed=embed, view=view)
    view.interaction = interaction
    await view.wait()
    try:
        await functions.edit_interaction(interaction, view=None)
    except discord.errors.NotFound:
        pass


# --- Embeds ---
async def embed_overview() -> discord.Embed:
    """Halloween overview embed"""
    activities = (
        f'{emojis.BP} Get various item **drops** (see below)\n'
        f'{emojis.BP} **Craft** various items (see {strings.SLASH_COMMANDS_EPIC_RPG["hal recipes"]})\n'
        f'{emojis.BP} Complete daily and weekly **tasks** (see {strings.SLASH_COMMANDS_EPIC_RPG["hal tasks"]})\n'
        f'{emojis.BP} Defeat event themed {emojis.HAL_JACK_O_LANTERN}{emojis.HAL_JACK_O_LANTIME} **minibosses**\n'
        f'{emojis.BP} Join the **world boss** fight to unlock codes (see {strings.SLASH_COMMANDS_EPIC_RPG["hal wb"]})\n'
        f'{emojis.BP} Get a unique **SPOOKY horse** type (see {strings.SLASH_COMMANDS_GUIDE["horse boost calculator"]})\n'
        f'{emojis.BP} Complete the event **quest** to get the {emojis.PET_PUMPKIN_BAT} pumpkin bat pet '
        f'(see {strings.SLASH_COMMANDS_EPIC_RPG["hal quest"]})\n'
        f'{emojis.BP} Buy rewards in the {strings.SLASH_COMMANDS_EPIC_RPG["hal shop"]}\n'
    )
    drops = (
        f'{emojis.BP} {emojis.HAL_PUMPKIN} pumpkins and {emojis.HAL_MONSTER_SOUL} monster souls from '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["hunt"]}, '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["training"]} and fish commands\n'
        f'{emojis.BP} {emojis.HAL_SPOOKY_ORB} spooky orbs from {emojis.HAL_BAT_SLIME} bat slimes in '
        f'{strings.SLASH_COMMANDS_EPIC_RPG["adventure"]}\n'
        f'{emojis.BP} {emojis.HAL_EPIC_CANDY} EPIC candies and {emojis.TIME_COOKIE} TIME cookies from defeating '
        f'{emojis.HAL_JACK_O_LANTERN}{emojis.HAL_JACK_O_LANTIME} minibosses\n'
        f'{emojis.BP} {emojis.HAL_PUMPKIN} pumpkins, {emojis.SLEEPY_POTION} sleepy potions and '
        f'{emojis.HAL_SUSPICIOUS_BROOM} suspicious brooms from {strings.SLASH_COMMANDS_EPIC_RPG["hal boo"]}\n'
        f'{emojis.DETAIL} This event command has a `2`h cooldown'
    )
    bonuses = (
        f'{emojis.BP} Miniboss/dungeon cooldown is reduced by `33`%'
    )
    schedule = (
        f'{emojis.BP} Event started on October 18, 2022\n'
        #f'{emojis.BP} World boss fight ends on October 31, 2022, 23:55 UTC\n'
        f'{emojis.BP} Event ends on November 13, 2022, 23:55 UTC\n'
        f'{emojis.BP} Items will vanish on November 20, 2022, 23:55 UTC\n'
        f'{emojis.DETAIL} Exception: {emojis.TIME_COOKIE} TIME cookies do not vanish'
    )
    tldr_guide = (
        f'{emojis.BP} **Optional**: Craft a {emojis.HAL_CANDY_FISH} candy fish and use it to get the SPOOKY horse\n'
        f'{emojis.BP} **Optional**: Craft the {emojis.SWORD_SPOOKY}{emojis.ARMOR_SPOOKY} spooky gear to increase rare '
        f'drop chances in {strings.SLASH_COMMANDS_EPIC_RPG["hal boo"]}\n'
        f'{emojis.BP} Complete your daily and weekly tasks\n'
        f'{emojis.BP} Use {strings.SLASH_COMMANDS_EPIC_RPG["hal boo"]} on cooldown\n'
        f'{emojis.BP} Craft as many {emojis.HAL_CANDY_BELL} candy bells as you are allowed daily\n'
        f'{emojis.BP} Use your first `40` {emojis.HAL_SPOOKY_ORB} spooky orbs to craft `10` {emojis.HAL_SPOOKY_SCROLL} '
        f'spooky scrolls.\n'
        f'{emojis.DETAIL} See topic `Pumpkin bat` for the correct answers.\n'
        f'{emojis.DETAIL} **Do not spend orbs in the shop until you have done this.**\n'
        f'{emojis.BP} Use {emojis.HAL_MONSTER_SOUL} monster souls you get with {strings.SLASH_COMMANDS_EPIC_RPG["hal wb"]}\n'
        f'{emojis.BP} Complete the quest\n'
        f'{emojis.BP} Empty the {strings.SLASH_COMMANDS_EPIC_RPG["hal shop"]}\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = f'HALLOWEEN EVENT 2022 {emojis.HAL_PUMPKIN}',
        description = 'Boo!'
    )
    embed.add_field(name='TL;DR GUIDE', value=tldr_guide, inline=False)
    embed.add_field(name='ACTIVITIES', value=activities, inline=False)
    embed.add_field(name='DROPS', value=drops, inline=False)
    embed.add_field(name='BONUSES', value=bonuses, inline=False)
    embed.add_field(name='EVENT SCHEDULE', value=schedule, inline=False)
    return embed


async def embed_chances() -> discord.Embed:
    """Halloween chances"""
    bat_slime = (
        f'{emojis.BP} Base spawn chance unknown\n'
        f'{emojis.BP} Inceases with {emojis.HAL_CANDY_BELL} candy bells (% unknown, `20` bells max)\n'
        f'{emojis.BP} `+5`% if horse has SPOOKY type (use a {emojis.HAL_CANDY_FISH} candy fish to get this type)\n'
        f'{emojis.BP} `x1.3` if world buff is active (use a {emojis.HAL_RED_SOUL} red soul to activate it)\n'
    )
    monster_soul = (
        f'{emojis.BP} Base drop chance unknown\n'
        f'{emojis.DETAIL} Increases with time since your last hunt\n'
        f'{emojis.DETAIL} Increases with {emojis.TIME_TRAVEL} TT\n'
    )
    miniboss = (
        f'{emojis.BP} `47.5`% chance to get a {emojis.HAL_JACK_O_LANTERN} sleepy jack-o-lantern as miniboss\n'
        f'{emojis.DETAIL} `85`% chance to beat it with 10 players\n'
        f'{emojis.BP} `5`% chance to get a {emojis.HAL_JACK_O_LANTIME} sleepy jack-o-lantime traveler as miniboss\n'
        f'{emojis.DETAIL} `80`% chance to beat it with 10 players\n'
    )
    broom = (
        f'{emojis.BP} Drop chance unknown\n'
        f'{emojis.BP} `70`% chance move up 1 area when using it\n'
        f'{emojis.BP} `15`% chance move **down** 1 area when using it\n'
        f'{emojis.BP} `15`% chance move up 2 areas when using it\n'
    )
    boo = (
        f'{emojis.BP} `70`% success chance when using {strings.SLASH_COMMANDS_EPIC_RPG["hal boo"]}\n'
        f'{emojis.BP} Drop chances to get {emojis.SLEEPY_POTION}{emojis.HAL_SUSPICIOUS_BROOM} rare items unknown\n'
        f'{emojis.DETAIL} `x1.3` with {emojis.SWORD_SPOOKY} Spooky Sword\n'
        f'{emojis.DETAIL} `x1.3` with {emojis.ARMOR_SPOOKY} Spooky Armor\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'HALLOWEEN EVENT CHANCES',
        description = 'This page lists all known event chances.'
    )
    embed.add_field(name=f'BAT SLIME {emojis.HAL_BAT_SLIME}', value=bat_slime, inline=False)
    embed.add_field(name=f'MONSTER SOUL {emojis.HAL_MONSTER_SOUL}', value=monster_soul, inline=False)
    embed.add_field(name=f'MINIBOSSES {emojis.HAL_JACK_O_LANTERN}{emojis.HAL_JACK_O_LANTIME}', value=miniboss, inline=False)
    embed.add_field(name=f'SUSPICIOUS BROOM {emojis.HAL_SUSPICIOUS_BROOM}', value=broom, inline=False)
    embed.add_field(name='BOO', value=boo, inline=False)
    return embed


async def embed_scroll_boss() -> discord.Embed:
    """Scroll boss embed"""
    trigger = (
        f'{emojis.BP} By crafting a {emojis.HAL_SPOOKY_SCROLL} spooky scroll'
    )
    tactics = (
        f'{emojis.BP} Attack from **ahead**: `bazooka`\n'
        f'{emojis.BP} Attack from the **left**: `pumpkin`\n'
        f'{emojis.BP} Attack from the **right**: `attack`\n'
        f'{emojis.BP} Attack from **behind**: `dodge`\n'
    )
    rewards_win = (
        f'{emojis.BP} 200 {emojis.HAL_PUMPKIN} pumpkins\n'
        f'{emojis.BP} 100 {emojis.ARENA_COOKIE} arena cookies\n'
        f'{emojis.BP} 2 {emojis.LB_EDGY} EDGY lootboxes\n'
        f'{emojis.BP} 3 {emojis.EPIC_BERRY} EPIC berries\n'
    )
    rewards_lose = (
        f'{emojis.BP} 150 {emojis.HAL_PUMPKIN} pumpkins\n'
        f'{emojis.BP} 80 {emojis.ARENA_COOKIE} arena cookies\n'
        f'{emojis.BP} 1 {emojis.LB_EDGY} EDGY lootbox\n'
        f'{emojis.BP} 1 {emojis.EPIC_BERRY} EPIC berry\n'
    )
    rewards_timeout = (
        f'{emojis.BP} 120 {emojis.HAL_PUMPKIN} pumpkins\n'
        f'{emojis.BP} 60 {emojis.ARENA_COOKIE} arena cookies\n'
        f'{emojis.BP} 1 {emojis.LB_EDGY} EDGY lootbox\n'
    )
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'PUMPKIN BAT (SCROLL BOSS) GUIDE',
    )
    embed.add_field(name='TRIGGER', value=trigger, inline=False)
    embed.add_field(name='TACTICS', value=tactics, inline=False)
    embed.add_field(name='REWARDS IF YOU WIN', value=rewards_win, inline=False)
    embed.add_field(name='REWARDS IF YOU LOSE', value=rewards_lose, inline=False)
    embed.add_field(name='REWARDS IF YOU TIME OUT', value=rewards_timeout, inline=False)
    return embed