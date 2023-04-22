# strings.py

import re

from discord.commands import OptionChoice

from resources import emojis


MSG_ABORTED = 'Aborted.'
MSG_ABORTING = 'Aborting.'
MSG_BOT_MESSAGE_NOT_FOUND = '**{user}**, couldn\'t find your {information} information, RIP.'
MSG_ERROR = 'Whelp, something went wrong here, sorry.'
MSG_INTERACTION_ERROR = 'You are not allowed to use this interaction.'
MSG_INVALID_AMOUNT = 'That\'s not a valid amount.'
MSG_AMOUNT_TOO_HIGH = 'Are you trying to break me or something? :thinking:'
MSG_AMOUNT_TOO_LOW = 'Imagine trying to use an amount lower than 1.'
MSG_SYNTAX = 'The command syntax is `{syntax}`'
MSG_SEARCH_QUERY_TOO_SHORT = 'The search query needs to be at least 3 characters long.'
MSG_INPUT_TOO_LONG = 'Really.'
MSG_WAIT_FOR_INPUT = '**{user}**, please type `{command}`'
MSG_WAIT_FOR_INPUT_SLASH = '**{user}**, please use {command}'
MSG_WRONG_INPUT = 'Wrong input. Aborting.'

DEFAULT_FOOTER = 'Use /help to see all available guides.'

ARGUMENT_TOPIC_DESCRIPTION = 'The topic you want to read about'

ITEM_ALIASES = {
    'ed sw': 'edgy sword',
    'edgy sw': 'edgy sword',
    'omega sw': 'omega sword',
    'o sw': 'omega sword',
    'omegasword': 'omega sword',
    'omegaarmor': 'omega armor',
    'ed sword': 'edgy sword',
    'edgysword': 'edgy sword',
    'ed armor': 'edgy armor',
    'edgyarmor': 'edgy armor',
    'ue sw': 'ultra-edgy sword',
    'ultra-edgy sw': 'ultra-edgy sword',
    'ultraedgy sw': 'ultra-edgy sword',
    'ultraedgysword': 'ultra-edgy sword',
    'ue sword': 'ultra-edgy sword',
    'ultra-omega sw': 'ultra-omega sword',
    'ultraomega sw': 'ultra-omega sword',
    'ultraomegasword': 'ultra-omega sword',
    'ultraomegaarmor': 'ultra-omega armor',
    'ue armor': 'ultra-edgy armor',
    'ultraedgyarmor': 'ultra-edgy armor',
    'godly sw': 'godly sword',
    'godlysword': 'godly sword',
    'g sword': 'godly sword',
    'g sw': 'godly sword',
    'unicorn sw': 'unicorn sword',
    'unicornsword': 'unicorn sword',
    'ruby sw': 'ruby sword',
    'rubyarmor': 'ruby armor',
    'rubysword': 'ruby sword',
    'fish sw': 'fish sword',
    'fishsword': 'fish sword',
    'apple sw': 'apple sword',
    'applesword': 'apple sword',
    'zombie sw': 'zombie sword',
    'zombiesword': 'zombie sword',
    'wooden sw': 'wooden sword',
    'woodensword': 'wooden sword',
    'fisharmor': 'fish armor',
    'wolfarmor': 'wolf armor',
    'eyearmor': 'eye armor',
    'bananaarmor': 'banana armor',
    'hair sw': 'hair sword',
    'hairsword': 'hair sword',
    'coin sw': 'coin sword',
    'coinsword': 'coin sword',
    'coinarmor': 'coin armor',
    'mermaidarmor': 'mermaid armor',
    'electronical sw': 'electronical sword',
    'electronicalsword': 'electronical sword',
    'electronicalarmor': 'electronical armor',
    'f': 'normie fish',
    'fishes': 'normie fish',
    'fish': 'normie fish',
    'normiefish': 'normie fish',
    'normie fishes': 'normie fish',
    'normiefishes': 'normie fish',
    'gf': 'golden fish',
    'golden fishes': 'golden fish',
    'goldenfish': 'golden fish',
    'goldenfishes': 'golden fish',
    'ef': 'epic fish',
    'epicfish': 'epic fish',
    'epicfishes': 'epic fish',
    'epic fishes': 'epic fish',
    'brandon': 'epic fish',
    'l': 'wooden log',
    'wood': 'wooden log',
    'logs': 'wooden log',
    'log': 'wooden log',
    'wooden logs': 'wooden log',
    'woodenlog': 'wooden log',
    'woodenlogs': 'wooden log',
    'el': 'epic log',
    'epic logs': 'epic log',
    'epic wood': 'epic log',
    'epiclog': 'epic log',
    'epiclogs': 'epic log',
    'epicwood': 'epic log',
    'sl': 'super log',
    'super logs': 'super log',
    'super wood': 'super log',
    'superlog': 'super log',
    'superlogs': 'super log',
    'superwood': 'super log',
    'super': 'super log',
    'ml': 'mega log',
    'mega logs': 'mega log',
    'mega wood': 'mega log',
    'megalog': 'mega log',
    'megalogs': 'mega log',
    'megawood': 'mega log',
    'mega': 'mega log',
    'hl': 'hyper log',
    'hyper logs': 'hyper log',
    'hyper wood': 'hyper log',
    'hyperlog': 'hyper log',
    'hyperlogs': 'hyper log',
    'hyperwood': 'hyper log',
    'hyper': 'hyper log',
    'ul': 'ultra log',
    'ultra logs': 'ultra log',
    'ultra wood': 'ultra log',
    'ultralog': 'ultra log',
    'ultralogs': 'ultra log',
    'ultrawood': 'ultra log',
    'ultra': 'ultra log',
    'a': 'apple',
    'apples': 'apple',
    'bananas': 'banana',
    'r': 'ruby',
    'rubies': 'ruby',
    'rubys': 'ruby',
    'bf': 'baked fish',
    'fs': 'fruit salad',
    'salad': 'fruit salad',
    'salads': 'fruit salad',
    'fruit salads': 'fruit salad',
    'aj': 'apple juice',
    'apple juices': 'apple juice',
    'bp': 'banana pickaxe',
    'pickaxe': 'banana pickaxe',
    'pickaxes': 'banana pickaxe',
    'pick': 'banana pickaxe',
    'picks': 'banana pickaxe',
    'heavy apples': 'heavy apple',
    'ha': 'heavy apple',
    'heavy': 'heavy apple',
    'sc': 'super cookie',
    'cookie': 'super cookie',
    'cookies': 'super cookie',
    'super cookies': 'super cookie',
    'supercookie': 'super cookie',
    'supercookies': 'super cookie',
    'fl': 'filled lootbox',
    'lb': 'filled lootbox',
    'lootbox': 'filled lootbox',
    'lootboxes': 'filled lootbox',
    'filled lootboxes': 'filled lootbox',
    'lbs': 'filled lootbox',
    'cs': 'coin sandwich',
    'coin': 'coin sandwich',
    'sandwich': 'coin sandwich',
    'sandwiches': 'coin sandwich',
    'coin sandwiches': 'coin sandwich',
    'ice cream': 'fruit ice cream',
    'ice': 'fruit ice cream',
    'cream': 'fruit ice cream',
    'ice creams': 'fruit ice cream',
    'icecreams': 'fruit ice cream',
    'icecream': 'fruit ice cream',
    'fruit ice creams': 'fruit ice cream',
    'fruit ice': 'fruit ice cream',
    'fruitice': 'fruit ice cream',
    'hairns': 'hairn',
    'oj': 'orange juice',
    'orange': 'orange juice',
    'oranges': 'orange juice',
    'orange juices': 'orange juice',
    'carrot breads': 'carrot bread',
    'cb': 'carrot bread',
    'cc': 'carrotato chips',
    'carrotato': 'carrotato chips',
    'chips': 'carrotato chips',
    'h': 'hairn',
    'melon': 'watermelon',
    'melons': 'watermelon',
    'water melon':'watermelon',
    'water melons':'watermelon',
    'watermelon':'watermelon',
    'wm': 'watermelon',
    'superfish': 'super fish',
    'superfishes': 'super fish',
    'super fishes': 'super fish',
    'sf': 'super fish',
    'ultimatelog': 'ultimate log',
    'ultimate logs': 'ultimate log',
    'ultimatelogs': 'ultimate log',
    'superarmor': 'super armor',
    'watermelon sw': 'watermelon sword',
    'melon sw': 'watermelon sword',
    'watermelonsw': 'watermelon sword',
    'watermelonsw': 'watermelon sword',
    'melonsw': 'watermelon sword',
    'wm sw': 'watermelon sword',
    'melon sword': 'watermelon sword',
    'watermelonsword': 'watermelon sword',
    'wm sword': 'watermelon sword',
    'wmsword': 'watermelon sword',
    'watermelonarmor': 'watermelon armor',
    'melon armor': 'watermelon armor',
    'melonarmor': 'watermelon armor',
    'wm armor': 'watermelon armor',
    'wmarmor': 'watermelon armor',
    'scaledarmor': 'scaled armor',
    'scalearmor': 'scaled armor',
    'scale armor': 'scaled armor',
    'scaledsword': 'scaled sword',
    'scalesword': 'scaled sword',
    'scaledsw': 'scaled sword',
    'scalesw': 'scaled sword',
    'scaled sw': 'scaled sword',
    'scale sw': 'scaled sword',
    'banana sw': 'banana sword',
    'bananasw': 'banana sword',
    'bananasword': 'banana sword',
    'epicarmor': 'epic armor',
    'epic sw': 'epic sword',
    'epicsw': 'epic sword',
    'epicsword': 'epic sword',
    'lootboxarmor': 'lootbox armor',
    'lbarmor': 'lootbox armor',
    'lb armor': 'lootbox armor',
    'lotterysword': 'lottery sword',
    'lotterysw': 'lottery sword',
    'lottery sw': 'lottery sword',
    'timesword': 'time sword',
    'timesw': 'time sword',
    'time sw': 'time sword',
    'timearmor': 'time armor',
    'voidsword': 'void sword',
    'voidsw': 'void sword',
    'void sw': 'void sword',
    'voidarmor': 'void armor',
    'abysssword': 'abyss sword',
    'abysssw': 'abyss sword',
    'abyss sw': 'abyss sword',
    'abyssarmor': 'abyss armor',
    'corruptedsword': 'corrupted sword',
    'corruptedsw': 'corrupted sword',
    'corrupted sw': 'corrupted sword',
    'corruptedarmor': 'corrupted armor',
    'spacesword': 'space sword',
    'spacesw': 'space sword',
    'space sw': 'space sword',
    'spacearmor': 'space armor',
    'woodenarmor': 'wooden armor',
    'tt': 'time travel',
    'timetravel': 'time travel',
    'darkenergy': 'dark energy',
    'basicsword': 'basic sword',
    'basicsw': 'basic sword',
    'basic sw': 'basic sword',
    'basicarmor': 'basic armor',
    'cookie sword': 'godly cookie',
    'godlycookie': 'godly cookie',
    'cookie sw': 'godly cookie',
    'cookiesw': 'godly cookie',
    'cookiesword': 'godly cookie',
}

item_columns_names = {
    'apple': 'apple',
    'armor_basic': 'Basic Armor',
    'armor_edgy': 'EDGY Armor',
    'armor_coin': 'Coin Armor',
    'armor_fish': 'Fish Armor',
    'armor_lootbox': 'Lootbox Armor',
    'armor_omega': 'OMEGA Armor',
    'armor_super': 'SUPER Armor',
    'armor_ultra_edgy': 'ULTRA-EDGY Armor',
    'armor_ultra_omega': 'ULTRA-OMEGA Armor',
    'banana': 'banana',
    'bread': 'bread',
    'carrot': 'carrot',
    'chip': 'chip',
    'coin': 'coin',
    'cookie': 'arena cookie',
    'dark_energy': 'dark energy',
    'dragon_essence': 'dragon essence',
    'dragon_scale': 'dragon scale',
    'fish': 'normie fish',
    'fish_epic': 'EPIC fish',
    'fish_golden': 'golden fish',
    'fish_super': 'SUPER fish',
    'life_potion': 'life potion',
    'lb_common': 'common lootbox',
    'lb_edgy': 'EDGY lootbox',
    'lb_epic': 'EPIC lootbox',
    'lb_rare': 'rare lootbox',
    'lb_godly': 'GODLY lootbox',
    'lb_omega': 'OMEGA lootbox',
    'lb_uncommon': 'uncommon lootbox',
    'lb_void': 'VOID lootbox',
    'lottery_ticket': 'lottery ticket',
    'life': 'LIFE',
    'log': 'wooden log',
    'log_epic': 'EPIC log',
    'log_hyper': 'HYPER log',
    'log_mega': 'MEGA log',
    'log_super': 'SUPER log',
    'log_ultimate': 'ULTIMATE log',
    'log_ultra': 'ULTRA log',
    'mermaid_hair': 'mermaid hair',
    'potato': 'potato',
    'ruby': 'ruby',
    'unicorn_horn': 'unicorn horn',
    'sword_basic': 'Basic Sword',
    'sword_edgy': 'EDGY Sword',
    'sword_electronical': 'Electronical Sword',
    'sword_godly': 'GODLY Sword',
    'sword_omega': 'OMEGA Sword',
    'sword_ultra_edgy': 'ULTRA-EDGY Sword',
    'sword_ultra_omega': 'ULTRA-OMEGA Sword',
    'time_dragon_essence': 'TIME dragon essence',
    'time_travel': 'time travel',
    'water_melon': 'water melon',
    'watermelon': 'watermelon',
    'wolf_skin': 'wolf skin',
    'zombie_eye': 'zombie eye',
}


PROFESSIONS = {
    'crafter': 'crafter', #English
    'enchanter': 'enchanter',
    'lootboxer': 'lootboxer',
    'merchant': 'merchant',
    'worker': 'worker',
    'crafteador': 'crafter', #Spanish
    'encantador': 'enchanter',
    'lootboxeador': 'lootboxer',
    'comerciante': 'merchant',
    'trabajador': 'worker',
    'craftador': 'crafter', #Portuguese
    'encantador': 'enchanter',
    'lootboxador': 'lootboxer',
    'comerciante': 'merchant',
    'trabalhador': 'worker',
}


PROFESSIONS_EN = {
    'crafter': 'crafter',
    'enchanter': 'enchanter',
    'lootboxer': 'lootboxer',
    'merchant': 'merchant',
    'worker': 'worker',
}


HORSE_TYPES_ENGLISH = {
    'mágico': 'magic',
    'defensor': 'defender',
    'fuerte': 'strong',
    'forte': 'strong',
    'tanque': 'tank',
    'dorado': 'golden',
    'dourado': 'golden',
    'festivo': 'festive',
    'especial': 'special',
    'súper especial': 'super special',
    'super especial': 'super special',
}


DUNGEONS = (
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    15.2,
    16,
    17,
    18,
    19,
    20,
    21,
)

CRAFTER_RETURNED_PERCENTAGES = {
    101: 0.1552,
    102: 0.1597,
    103: 0.1626,
    104: 0.1648,
    105: 0.1666,
    106: 0.1682,
    107: 0.1695,
    108: 0.1707,
    109: 0.1718,
    110: 0.1728,
    111: 0.1737,
    112: 0.1746,
    113: 0.1754,
    114: 0.1761,
    115: 0.1769,
    116: 0.1775,
    117: 0.1782,
    118: 0.1788,
    119: 0.1794,
    120: 0.1799,
    121: 0.1805,
    122: 0.181,
    123: 0.1815,
    124: 0.182,
    125: 0.1824,
    126: 0.1829,
    127: 0.1833,
    128: 0.1838,
    129: 0.1842,
    130: 0.1846,
    131: 0.185,
    132: 0.1853,
    133: 0.1857,
    134: 0.1861,
    135: 0.1864,
    136: 0.1868,
    137: 0.1871,
    138: 0.1875,
    139: 0.1878,
    140: 0.1881,
    141: 0.1884,
    142: 0.1887,
    143: 0.189,
    144: 0.1893,
    145: 0.1896,
    146: 0.1899,
    147: 0.1902,
    148: 0.1904,
    149: 0.1907,
    150: 0.191,
    151: 0.1912,
    152: 0.1915,
    153: 0.1917,
    154: 0.192,
    155: 0.1922,
    156: 0.1925,
    157: 0.1927,
    158: 0.193,
    159: 0.1932,
    160: 0.1934,
    161: 0.1937,
    162: 0.1939,
    163: 0.1941,
    164: 0.1943,
    165: 0.1945,
    166: 0.1947,
    167: 0.195,
    168: 0.1952,
    169: 0.1954,
    170: 0.1956,
    171: 0.1958,
    172: 0.196,
    173: 0.1962,
    174: 0.1964,
    175: 0.1965,
    176: 0.1967,
    177: 0.1969,
    178: 0.1971,
    179: 0.1973,
    180: 0.1975,
    181: 0.1977,
    182: 0.1978,
    183: 0.198,
    184: 0.1982,
    185: 0.1984,
    186: 0.1985,
    187: 0.1987,
    188: 0.1989,
    189: 0.199,
    190: 0.1992,
    191: 0.1994,
    192: 0.1995,
    193: 0.1997,
    194: 0.1999,
    195: 0.2,
    196: 0.2002,
    197: 0.2003,
    198: 0.2005,
    199: 0.2006,
    200: 0.2008,
} # Not used anymore, but I'll keep it for now, in case it's needed elsewhere


NUMBERS_ROMAN_INTEGER = {
    'ix': 1,
    'ii': 2,
    'iii': 3,
    'iv': 4,
    'v': 5,
    'vi': 6,
    'vii': 7,
    'viii': 8,
    'ix': 9,
    'x': 10,
}


# Choices for slash commands
CHOICES_AREA = []
CHOICES_AREA_NO_TOP = []
for area_no in range(1, 21):
    CHOICES_AREA.append(OptionChoice(name=f'Area {area_no}', value=area_no))
    CHOICES_AREA_NO_TOP.append(OptionChoice(name=f'Area {area_no}', value=area_no))
CHOICES_AREA.append(OptionChoice(name='The TOP', value=21))


CHOICES_DUNGEON = []
for dungeon_no in range(1, 21):
    if dungeon_no == 15:
        CHOICES_DUNGEON.append(OptionChoice(name=f'Dungeon 15', value=15))
        CHOICES_DUNGEON.append(OptionChoice(name=f'Dungeon 15-2', value=15.2))
    else:
        CHOICES_DUNGEON.append(OptionChoice(name=f'Dungeon {dungeon_no}', value=dungeon_no))
CHOICES_DUNGEON.append(OptionChoice(name='EPIC NPC fight', value=21))


CHOICE_ASCENDED = 'Ascended'
CHOICE_NOT_ASCENDED = 'Not ascended'
CHOICES_ASCENSION = [
    CHOICE_ASCENDED,
    CHOICE_NOT_ASCENDED,
]


CHOICE_GUIDE_FULL = 'Full'
CHOICE_GUIDE_SHORT = 'Short'
CHOICES_AREA_GUIDES = [
    CHOICE_GUIDE_FULL,
    CHOICE_GUIDE_SHORT,
]


# Links
LINK_INVITE = (
    'https://discord.com/api/oauth2/authorize?client_id=770199669141536768&permissions=313344&scope='
    'applications.commands%20bot'
)
LINK_SUPPORT = 'https://discord.gg/v7WbhnhbgN'
LINK_VOTE = 'https://top.gg/bot/770199669141536768/vote'


# Slash commands
SLASH_COMMANDS_EPIC_RPG_OLD = {
    'achievements dungeons': f'{emojis.EPIC_RPG_LOGO_SMALL}`/achievements dungeons`',
    'achievements events': f'{emojis.EPIC_RPG_LOGO_SMALL}`/achievements events`',
    'achievements misc': f'{emojis.EPIC_RPG_LOGO_SMALL}`/achievements misc`',
    'achievements multiplayer': f'{emojis.EPIC_RPG_LOGO_SMALL}`/achievements multiplayer`',
    'achievements progress': f'{emojis.EPIC_RPG_LOGO_SMALL}`/achievements progress`',
    'achievements working': f'{emojis.EPIC_RPG_LOGO_SMALL}`/achievements working`',
    'adventure': f'{emojis.EPIC_RPG_LOGO_SMALL}`/adventure`',
    'area': f'{emojis.EPIC_RPG_LOGO_SMALL}`/area`',
    'arena': f'{emojis.EPIC_RPG_LOGO_SMALL}`/arena`',
    'axe': f'{emojis.EPIC_RPG_LOGO_SMALL}`/axe`',
    'badge claim': f'{emojis.EPIC_RPG_LOGO_SMALL}`/badge claim`',
    'badge list': f'{emojis.EPIC_RPG_LOGO_SMALL}`/badge list`',
    'badge select': f'{emojis.EPIC_RPG_LOGO_SMALL}`/badge select`',
    'badge unlocked': f'{emojis.EPIC_RPG_LOGO_SMALL}`/badge unlocked`',
    'big arena': f'{emojis.EPIC_RPG_LOGO_SMALL}`/big arena`',
    'big dice': f'{emojis.EPIC_RPG_LOGO_SMALL}`/big dice`',
    'bigboat': f'{emojis.EPIC_RPG_LOGO_SMALL}`/bigboat`',
    'blackjack': f'{emojis.EPIC_RPG_LOGO_SMALL}`/blackjack`',
    'boat': f'{emojis.EPIC_RPG_LOGO_SMALL}`/boat`',
    'bowsaw': f'{emojis.EPIC_RPG_LOGO_SMALL}`/bowsaw`',
    'buy': f'{emojis.EPIC_RPG_LOGO_SMALL}`/buy`',
    'chainsaw': f'{emojis.EPIC_RPG_LOGO_SMALL}`/chainsaw`',
    'chop': f'{emojis.EPIC_RPG_LOGO_SMALL}`/chop`',
    'coinflip': f'{emojis.EPIC_RPG_LOGO_SMALL}`/coinflip`',
    'code': f'{emojis.EPIC_RPG_LOGO_SMALL}`/code`',
    'cook': f'{emojis.EPIC_RPG_LOGO_SMALL}`/cook`',
    'craft': f'{emojis.EPIC_RPG_LOGO_SMALL}`/craft`',
    'cups': f'{emojis.EPIC_RPG_LOGO_SMALL}`/cups`',
    'daily': f'{emojis.EPIC_RPG_LOGO_SMALL}`/daily`',
    'deposit': f'{emojis.EPIC_RPG_LOGO_SMALL}`/deposit`',
    'dice': f'{emojis.EPIC_RPG_LOGO_SMALL}`/dice`',
    'dismantle': f'{emojis.EPIC_RPG_LOGO_SMALL}`/dismantle`',
    'drill': f'{emojis.EPIC_RPG_LOGO_SMALL}`/drill`',
    'duel': f'{emojis.EPIC_RPG_LOGO_SMALL}`/duel`',
    'dungeon': f'{emojis.EPIC_RPG_LOGO_SMALL}`/dungeon`',
    'dynamite': f'{emojis.EPIC_RPG_LOGO_SMALL}`/dynamite`',
    'eat': f'{emojis.EPIC_RPG_LOGO_SMALL}`/eat`',
    'enchant': f'{emojis.EPIC_RPG_LOGO_SMALL}`/enchant`',
    'epic npc': f'{emojis.EPIC_RPG_LOGO_SMALL}`/epic npc`',
    'epic quest': f'{emojis.EPIC_RPG_LOGO_SMALL}`/epic quest`',
    'farm': f'{emojis.EPIC_RPG_LOGO_SMALL}`/farm`',
    'fish': f'{emojis.EPIC_RPG_LOGO_SMALL}`/fish`',
    'forge': f'{emojis.EPIC_RPG_LOGO_SMALL}`/forge`',
    'give': f'{emojis.EPIC_RPG_LOGO_SMALL}`/give`',
    'greenhouse': f'{emojis.EPIC_RPG_LOGO_SMALL}`/greenhouse`',
    'guild': f'{emojis.EPIC_RPG_LOGO_SMALL}`/guild stats`',
    'guild buy': f'{emojis.EPIC_RPG_LOGO_SMALL}`/guild buy`',
    'guild changeowner': f'{emojis.EPIC_RPG_LOGO_SMALL}`/guild changeowner`',
    'guild create': f'{emojis.EPIC_RPG_LOGO_SMALL}`/guild create`',
    'guild delete': f'{emojis.EPIC_RPG_LOGO_SMALL}`/guild delete`',
    'guild invite': f'{emojis.EPIC_RPG_LOGO_SMALL}`/guild invite`',
    'guild kick': f'{emojis.EPIC_RPG_LOGO_SMALL}`/guild kick`',
    'guild leave': f'{emojis.EPIC_RPG_LOGO_SMALL}`/guild leave`',
    'guild list': f'{emojis.EPIC_RPG_LOGO_SMALL}`/guild list`',
    'guild raid': f'{emojis.EPIC_RPG_LOGO_SMALL}`/guild raid`',
    'guild ranking': f'{emojis.EPIC_RPG_LOGO_SMALL}`/guild ranking`',
    'guild shop': f'{emojis.EPIC_RPG_LOGO_SMALL}`/guild shop`',
    'guild stats': f'{emojis.EPIC_RPG_LOGO_SMALL}`/guild stats`',
    'guild tasks': f'{emojis.EPIC_RPG_LOGO_SMALL}`/guild tasks`',
    'guild upgrade': f'{emojis.EPIC_RPG_LOGO_SMALL}`/guild upgrade`',
    'heal': f'{emojis.EPIC_RPG_LOGO_SMALL}`/heal`',
    'help': f'{emojis.EPIC_RPG_LOGO_SMALL}`/help`',
    'horse breeding': f'{emojis.EPIC_RPG_LOGO_SMALL}`/horse breeding`',
    'horse feed': f'{emojis.EPIC_RPG_LOGO_SMALL}`/horse feed`',
    'horse race': f'{emojis.EPIC_RPG_LOGO_SMALL}`/horse race`',
    'horse stats': f'{emojis.EPIC_RPG_LOGO_SMALL}`/horse stats`',
    'horse training': f'{emojis.EPIC_RPG_LOGO_SMALL}`/horse training`',
    'hunt': f'{emojis.EPIC_RPG_LOGO_SMALL}`/hunt`',
    'inventory': f'{emojis.EPIC_RPG_LOGO_SMALL}`/inventory`',
    'jail': f'{emojis.EPIC_RPG_LOGO_SMALL}`/jail`',
    'ladder': f'{emojis.EPIC_RPG_LOGO_SMALL}`/ladder`',
    'lottery': f'{emojis.EPIC_RPG_LOGO_SMALL}`/lottery`',
    'mine': f'{emojis.EPIC_RPG_LOGO_SMALL}`/mine`',
    'miniboss': f'{emojis.EPIC_RPG_LOGO_SMALL}`/miniboss`',
    "minintboss": f'{emojis.EPIC_RPG_LOGO_SMALL}`/minintboss`',
    'multidice': f'{emojis.EPIC_RPG_LOGO_SMALL}`/multidice`',
    'net': f'{emojis.EPIC_RPG_LOGO_SMALL}`/net`',
    'open': f'{emojis.EPIC_RPG_LOGO_SMALL}`/open`',
    'pets': f'{emojis.EPIC_RPG_LOGO_SMALL}`/pets list`',
    'pets adventure': f'{emojis.EPIC_RPG_LOGO_SMALL}`/pets adventure`',
    'pets ascend': f'{emojis.EPIC_RPG_LOGO_SMALL}`/pets ascend`',
    'pets claim': f'{emojis.EPIC_RPG_LOGO_SMALL}`/pets claim`',
    'pets fusion': f'{emojis.EPIC_RPG_LOGO_SMALL}`/pets fusion`',
    'pets list': f'{emojis.EPIC_RPG_LOGO_SMALL}`/pets list`',
    'pets tournament': f'{emojis.EPIC_RPG_LOGO_SMALL}`/pets tournament`',
    'pickaxe': f'{emojis.EPIC_RPG_LOGO_SMALL}`/pickaxe`',
    'pickup': f'{emojis.EPIC_RPG_LOGO_SMALL}`/pickup`',
    'professions crafter': f'{emojis.EPIC_RPG_LOGO_SMALL}`/professions crafter`',
    'professions enchanter': f'{emojis.EPIC_RPG_LOGO_SMALL}`/professions enchanter`',
    'professions lootboxer': f'{emojis.EPIC_RPG_LOGO_SMALL}`/professions lootboxer`',
    'professions merchant': f'{emojis.EPIC_RPG_LOGO_SMALL}`/professions merchant`',
    'professions stats': f'{emojis.EPIC_RPG_LOGO_SMALL}`/professions stats`',
    'professions worker': f'{emojis.EPIC_RPG_LOGO_SMALL}`/professions worker`',
    'profile': f'{emojis.EPIC_RPG_LOGO_SMALL}`/profile`',
    'progress': f'{emojis.EPIC_RPG_LOGO_SMALL}`/progress`',
    'quest': f'{emojis.EPIC_RPG_LOGO_SMALL}`/quest`',
    'refine': f'{emojis.EPIC_RPG_LOGO_SMALL}`/refine`',
    'returning quest': f'{emojis.EPIC_RPG_LOGO_SMALL}`/returning quest`',
    'returning shop': f'{emojis.EPIC_RPG_LOGO_SMALL}`/returning shop`',
    'returning superdaily': f'{emojis.EPIC_RPG_LOGO_SMALL}`/returning superdaily`',
    'shop': f'{emojis.EPIC_RPG_LOGO_SMALL}`/shop`',
    'slots': f'{emojis.EPIC_RPG_LOGO_SMALL}`/slots`',
    'start': f'{emojis.EPIC_RPG_LOGO_SMALL}`/start`',
    'stats': f'{emojis.EPIC_RPG_LOGO_SMALL}`/stats`',
    'time jump': f'{emojis.EPIC_RPG_LOGO_SMALL}`/time jump`',
    'time travel': f'{emojis.EPIC_RPG_LOGO_SMALL}`/time travel`',
    'tractor': f'{emojis.EPIC_RPG_LOGO_SMALL}`/tractor`',
    'training': f'{emojis.EPIC_RPG_LOGO_SMALL}`/training`',
    'transcend': f'{emojis.EPIC_RPG_LOGO_SMALL}`/transcend`',
    'transmute': f'{emojis.EPIC_RPG_LOGO_SMALL}`/transmute`',
    'ultraining': f'{emojis.EPIC_RPG_LOGO_SMALL}`/ultraining start`',
    'ultraining progress': f'{emojis.EPIC_RPG_LOGO_SMALL}`/ultraining progress`',
    'void areas': f'{emojis.EPIC_RPG_LOGO_SMALL}`/void areas`',
    'void info': f'{emojis.EPIC_RPG_LOGO_SMALL}`/void info`',
    'vote': f'{emojis.EPIC_RPG_LOGO_SMALL}`/vote`',
    'weekly': f'{emojis.EPIC_RPG_LOGO_SMALL}`/weekly`',
    'wheel': f'{emojis.EPIC_RPG_LOGO_SMALL}`/wheel`',
    'withdraw': f'{emojis.EPIC_RPG_LOGO_SMALL}`/withdraw`',
    'world': f'{emojis.EPIC_RPG_LOGO_SMALL}`/world status`',
}

SLASH_COMMANDS_EPIC_RPG = {
    'achievements dungeons': '</achievements dungeons:959915736892076042>',
    'achievements events': '</achievements events:959915736892076042>',
    'achievements misc': '</achievements misc:959915736892076042>',
    'achievements multiplayer': '</achievements multiplayer:959915736892076042>',
    'achievements progress': '</achievements progress:959915736892076042>',
    'achievements working': '</achievements working:959915736892076042>',
    'adventure': '</adventure:961046240420855808>',
    'alchemy make': '</alchemy make:1074072459847925810>',
    'area': '</area:956658464879427604>',
    'arena': '</arena:960740633302138920>',
    'axe': '</axe:959162695909781504>',
    'badge claim': '</badge claim:960002338930696224>',
    'badge list': '</badge list:960002338930696224>',
    'badge select': '</badge select:960002338930696224>',
    'badge unlocked': '</badge unlocked:960002338930696224>',
    'big arena': '</big arena:960362922029252719>',
    'big dice': '</big dice:960362922029252719>',
    'bigboat': '</bigboat:959163596754010162>',
    'blackjack': '</blackjack:959916178149605437>',
    'boat': '</boat:959163596087111780>',
    'boosts': '</boosts:1074072450809200771>',
    'bowsaw': '</bowsaw:959162696371146883>',
    'buy': '</buy:964351964651601961>',
    'chainsaw': '</chainsaw:959162697398763590>',
    'chop': '</chop:959162695070928896>',
    'coinflip': '</coinflip:958555800111038495>',
    'code': '</code:959916180620058624>',
    'cook': '</cook:959915740977315860>',
    'craft': '</craft:960002336372162570>',
    'cups': '</cups:958555799288959016>',
    'daily': '</daily:956658466099982386>',
    'deposit': '</deposit:958555796831096883>',
    'dice': '</dice:957815871902994432>',
    'dismantle': '</dismantle:960002337328496660>',
    'drill': '</drill:959164541206417479>',
    'duel': '</duel:960362921198751784>',
    'dungeon': '</dungeon:966956823032791090>',
    'dynamite': '</dynamite:959164543920132126>',
    'eat': '</eat:959916177684062238>',
    'egg buy': '</egg buy:1092910883556044891>',
    'egg eat': '</egg eat:1092910883556044891>',
    'egg god': '</egg god:1092910883556044891>',
    'egg quest': '</egg quest:1092910883556044891>',
    'egg shop': '</egg shop:1092910883556044891>',
    'egg slots': '</egg slots:1092910883556044891>',
    'egg tasks': '</egg tasks:1092910883556044891>',
    'egg use': '</egg use:1092910883556044891>',
    'egg wb': '</egg wb:1092910883556044891>',
    'enchant': '</enchant:959164903745257532>',
    'epic npc': '</epic npc:961046236469792810>',
    'epic quest': '</epic quest:961046236469792810>',
    'farm': '</farm:959915738716598272>',
    'fish': '</fish:959163594665242684>',
    'forge': '</forge:960002338121203722>',
    'give': '</give:958561514355327006>',
    'greenhouse': '</greenhouse:959164279884509194>',
    'guild': '</guild stats:961046237753257994>',
    'guild buy': '</guild buy:961046237753257994>',
    'guild changeowner': '</guild changeowner:961046237753257994>',
    'guild create': '</guild create:961046237753257994>',
    'guild delete': '</guild delete:961046237753257994>',
    'guild invite': '</guild invite:961046237753257994>',
    'guild kick': '</guild kick:961046237753257994>',
    'guild leave': '</guild leave:961046237753257994>',
    'guild list': '</guild list:961046237753257994>',
    'guild raid': '</guild raid:961046237753257994>',
    'guild ranking': '</guild ranking:961046237753257994>',
    'guild shop': '</guild shop:961046237753257994>',
    'guild stats': '</guild stats:961046237753257994>',
    'guild tasks': '</guild tasks:961046237753257994>',
    'guild upgrade': '</guild upgrade:961046237753257994>',
    'hal boo': '</hal boo:1031664514250330192>',
    'hal shop': '</hal shop:1031664514250330192>',
    'hal info': '</hal info:1031664514250330192>',
    'hal quest': '</hal quest:1031664514250330192>',
    'hal recipes': '</hal recipes:1031664514250330192>',
    'hal tasks': '</hal tasks:1031664514250330192>',
    'hal wb': '</hal wb:1031664514250330192>',
    'heal': '</heal:959915737777061928>',
    'help': '</help:951221901311750205>',
    'horse breeding': '</horse breeding:966961638378987540>',
    'horse feed': '</horse feed:966961638378987540>',
    'horse race': '</horse race:966961638378987540>',
    'horse stats': '</horse stats:966961638378987540>',
    'horse training': '</horse training:966961638378987540>',
    'hunt': '</hunt:964351961774325770>',
    'inventory': '</inventory:958555797590265896>',
    'jail': '</jail:966956629411123201>',
    'ladder': '</ladder:959164278072569936>',
    'lottery': '</lottery:957815874063061072>',
    'love quest': '</love quest:1074072468152656033>',
    'love share': '</love share:1074072468152656033>',
    'love shop': '</love shop:1074072468152656033>',
    'love slots': '</love slots:1074072468152656033>',
    'mine': '</mine:959164539922952263>',
    'miniboss': '</miniboss:960740632400388146>',
    "minintboss": '</minintboss:960362922813575209>',
    'multidice': '</multidice:958558816818036776>',
    'net': '</net:959163595428618290>',
    'open': '</open:959164544696070154>',
    'pets': '</pets list:961046238613090385>',
    'pets adventure': '</pets adventure:961046238613090385>',
    'pets ascend': '</pets ascend:961046238613090385>',
    'pets claim': '</pets claim:961046238613090385>',
    'pets fusion': '</pets fusion:961046238613090385>',
    'pets list': '</pets list:961046238613090385>',
    'pets tournament': '</pets tournament:961046238613090385>',
    'pickaxe': '</pickaxe:959164540589842492>',
    'pickup': '</pickup:959164277321768990>',
    'professions crafter': '</professions crafter:959942193747992586>',
    'professions enchanter': '</professions enchanter:959942193747992586>',
    'professions lootboxer': '</professions lootboxer:959942193747992586>',
    'professions merchant': '</professions merchant:959942193747992586>',
    'professions stats': '</professions stats:959942193747992586>',
    'professions worker': '</professions worker:959942193747992586>',
    'profile': '</profile:958554803422781460>',
    'progress': '</progress:958558817921159251>',
    'quest': '</quest start:960740627790848041>',
    'recipes': '</recipes:960362920242446367>',
    'refine': '</refine:959164904609316904>',
    'returning quest': '</returning quest:961046239510691860>',
    'returning shop': '</returning shop:961046239510691860>',
    'returning superdaily': '</returning superdaily:961046239510691860>',
    'shop': '</shop:951221902695874630>',
    'slots': '</slots:958555798273925180>',
    'start': '</start:951221902016381028>',
    'stats': '</stats:958558818831315004>',
    'time jump': '</time jump:960740634258464808>',
    'time travel': '</time travel:960740634258464808>',
    'tractor': '</tractor:959164278890463272>',
    'training': '</training:960362923983765545>',
    'transcend': '</transcend:959164906098286643>',
    'transmute': '</transmute:959164905381056513>',
    'ultraining': '</ultraining start:959942194649772112>',
    'ultraining buy': '</ultraining buy:959942194649772112>',
    'ultraining progress': '</ultraining progress:959942194649772112>',
    'ultraining shop': '</ultraining shop:959942194649772112>',
    'void areas': '</void areas:959942192623931442>',
    'void info': '</void info:959942192623931442>',
    'vote': '</vote:964351963720478760>',
    'weekly': '</weekly:956658465185603645>',
    'wheel': '</wheel:959916179525341194>',
    'withdraw': '</withdraw:958554805020794880>',
    'world': '</world status:953370104236761108>',
    'world info': '</world info:953370104236761108>',
    'xmas calendar': '</xmas calendar:1048310047865852005>',
    'xmas chimney': '</xmas chimney:1048310047865852005>',
    'xmas info': '</xmas info:1048310047865852005>',
    'xmas presents': '</xmas presents:1048310047865852005>',
    'xmas quests': '</xmas quests:1048310047865852005>',
    'xmas recipes': '</xmas recipes:1048310047865852005>',
    'xmas shop': '</xmas shop:1048310047865852005>',
    'xmas slots': '</xmas slots:1048310047865852005>',
    'xmas tasks': '</xmas tasks:1048310047865852005>',
    'xmas tree': '</xmas tree:1048310047865852005>',
    'xmas wb': '</xmas wb:1048310047865852005>',
}

SLASH_COMMANDS_GUIDE_OLD = {
    'about': f'{emojis.LOGO}`/about`',
    'area check': f'{emojis.LOGO}`/area check`',
    'area guide': f'{emojis.LOGO}`/area guide`',
    'ask the oracle': f'{emojis.LOGO}`/ask the oracle`',
    'badges': f'{emojis.LOGO}`/badges`',
    'beginner guide': f'{emojis.LOGO}`/beginner guide`',
    'calculator': f'{emojis.LOGO}`/calculator`',
    'codes': f'{emojis.LOGO}`/codes`',
    'coin cap calculator': f'{emojis.LOGO}`/coin cap calculator`',
    'coolness guide': f'{emojis.LOGO}`/coolness guide`',
    'crafting calculator': f'{emojis.LOGO}`/crafting calculator`',
    'dismantling calculator': f'{emojis.LOGO}`/dismantling calculator`',
    'drop chance calculator': f'{emojis.LOGO}`/drop chance calculator`',
    'duel weapons': f'{emojis.LOGO}`/duel weapons`',
    'dungeon check': f'{emojis.LOGO}`/dungeon check`',
    'dungeon guide': f'{emojis.LOGO}`/dungeon guide`',
    'enchanting guide': f'{emojis.LOGO}`/enchanting guide`',
    'event guide': f'{emojis.LOGO}`/event guide`',
    'farming guide': f'{emojis.LOGO}`/farming guide`',
    'gambling guide': f'{emojis.LOGO}`/gambling guide`',
    'guild guide': f'{emojis.LOGO}`/guild guide`',
    'help': f'{emojis.LOGO}`/help`',
    'horse boost calculator': f'{emojis.LOGO}`/horse boost calculator`',
    'horse guide': f'{emojis.LOGO}`/horse guide`',
    'horse training calculator': f'{emojis.LOGO}`/horse training calculator`',
    'inventory calculator': f'{emojis.LOGO}`/inventory calculator`',
    'monster drops': f'{emojis.LOGO}`/monster drops`',
    'monster search': f'{emojis.LOGO}`/monster search`',
    'pets fuse': f'{emojis.LOGO}`/pets fuse`',
    'pets guide': f'{emojis.LOGO}`/pets guide`',
    'professions calculator': f'{emojis.LOGO}`/professions calculator`',
    'professions guide': f'{emojis.LOGO}`/professions guide`',
    'set progress': f'{emojis.LOGO}`/set progress`',
    'settings': f'{emojis.LOGO}`/settings`',
    'time jump calculator': f'{emojis.LOGO}`/time jump calculator`',
    'time travel guide': f'{emojis.LOGO}`/time travel guide`',
    'time travel bonuses': f'{emojis.LOGO}`/time travel bonuses`',
    'tip': f'{emojis.LOGO}`/tip`',
    'title search': f'{emojis.LOGO}`/title search`',
    'trade calculator': f'{emojis.LOGO}`/trade calculator`',
    'trade rates': f'{emojis.LOGO}`/trade rates`',
    'trade guide': f'{emojis.LOGO}`/trade guide`',
    'ultraining guide': f'{emojis.LOGO}`/ultraining guide`',
    'ultraining stats calculator': f'{emojis.LOGO}`/ultraining stats calculator`',
}

SLASH_COMMANDS_GUIDE = {
    'about': '</about:972045824869679138>',
    'achievement search': '</achievement search:0>',
    'alchemy guide': '</alchemy guide:1074067543620325466>',
    'area check': '</area check:972045824806760468>',
    'area guide': '</area guide:972045824806760468>',
    'ask the oracle': '</ask the oracle:972045824806760477>',
    'badges': '</badges:972045824869679140>',
    'beginner guide': '</beginner guide:972045824869679143>',
    'calculator': '</calculator:972045824940965899>',
    'codes': '</codes:972045824869679139>',
    'coin cap calculator': '</coin cap calculator:972045824940965900>',
    'complain': '</complain:972045824940965900>', # ID needs to be updated
    'coolness guide': '</coolness guide:972045824869679141>',
    'crafting calculator': '</crafting calculator:972045824806760471>',
    'dismantling calculator': '</dismantling calculator:972045824806760472>',
    'drop chance calculator': '</drop chance calculator:972045824806760469>',
    'duel weapons': '</duel weapons:972045824806760473>',
    'dungeon check': '</dungeon check:972045824806760474>',
    'dungeon guide': '</dungeon guide:972045824806760474>',
    'easter guide': '</easter guide:1092914302626832565>',
    'egg guide': '</egg guide:1092915608129118208>',
    'enchanting guide': '</enchanting guide:972045824806760475>',
    'event guide': '</event guide:972045824806760476>',
    'farming guide': '</farming guide:972045824869679142>',
    'gambling guide': '</gambling guide:972045824869679135>',
    'guild guide': '</guild guide:972045824869679134>',
    'halloween guide': '</halloween guide:1031659987837145150>',
    'help': '</help:972045824869679137>',
    'horse boost calculator': '</horse boost calculator:972045824869679136>',
    'horse guide': '</horse guide:972045824869679136>',
    'horse training calculator': '</horse training calculator:972045824869679136>',
    'inventory calculator': '</inventory calculator:972045824806760470>',
    'love guide': '</love guide:1074067543620325469>',
    'monster drops': '</monster drops:972045824940965901>',
    'monster search': '</monster search:972045824940965901>',
    'pets fuse': '</pets fuse:972045824940965902>',
    'pets guide': '</pets guide:972045824940965902>',
    'professions calculator': '</professions calculator:972045824940965903>',
    'professions guide': '</professions guide:972045824940965903>',
    'set progress': '</set progress:972045824940965905>',
    'settings': '</settings:972045824940965904>',
    'time jump calculator': '</time jump calculator:972045824940965906>',
    'time jump score': '</time jump score:972045824940965906>',
    'time travel guide': '</time travel guide:972045824940965906>',
    'time travel bonuses': '</time travel bonuses:972045824940965906>',
    'tip': '</tip:972045824940965898>',
    'title search': '</title search:972045824940965907>',
    'trade calculator': '</trade calculator:972045824999690301>',
    'trade rates': '</trade rates:972045824999690301>',
    'trade guide': '</trade guide:972045824999690301>',
    'ultraining guide': '</ultraining guide:972045824999690302>',
    'ultraining stats calculator': '</ultraining stats calculator:972045824999690302>',
    'valentine guide': '</valentine guide:1074067543620325468>',
    'xmas guide': '</xmas guide:1047763243541745684>',
    'xmas items': '</xmas items:1047763243541745684>',
}

# Tier: Coin increase multiplier
HORSE_MULTIPLIER_COIN = {
    1: 1,
    2: 1.05,
    3: 1.1,
    4: 1.2,
    5: 1.3,
    6: 1.45,
    7: 1.6,
    8: 1.8,
    9: 2,
    10: 3,
}

# Tier: Lootbox chance multiplier
HORSE_MULTIPLIER_LOOTBOX = {
    1: 1,
    2: 1,
    3: 1,
    4: 1,
    5: 1.2,
    6: 1.5,
    7: 2,
    8: 3,
    9: 5,
    10: 7.5,
}

# Tier: Drop chance multiplier
HORSE_MULTIPLIER_DROPS = {
    1: 1,
    2: 1,
    3: 1,
    4: 1,
    5: 1,
    6: 1,
    7: 1.2,
    8: 1.5,
    9: 2,
    10: 3,
}

# Tier: Pet chance multiplier
HORSE_MULTIPLIER_PETS = {
    1: 1,
    2: 1,
    3: 1,
    4: 1,
    5: 1,
    6: 1,
    7: 1,
    8: 1,
    9: 2.5,
    10: 5,
}


# Regex
REGEX_COMMAND_QUICK_TRADE = re.compile(r"(?:\bi\b|\binv\b|\binventory\b)\s+\b(?:\d\d?|top)\b")