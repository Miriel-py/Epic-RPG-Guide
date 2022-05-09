# strings.py

from discord.commands import OptionChoice


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
MSG_WAIT_FOR_INPUT_SLASH = '**{user}**, please use {emoji}`{command}`'
MSG_WRONG_INPUT = 'Wrong input. Aborting.'

DEFAULT_FOOTER = 'Use /help to see all available guides.'

ARGUMENT_TOPIC_DESCRIPTION = 'The topic you want to read about'

ITEM_ALIASES = {
    'ed sw': 'edgy sword',
    'edgy sw': 'edgy sword',
    'omega sw': 'omega sword',
    'o sw': 'omega sword',
    'ed sword': 'edgy sword',
    'ed armor': 'edgy armor',
    'ue sw': 'ultra-edgy sword',
    'ultra-edgy sw': 'ultra-edgy sword',
    'ultraedgy sw': 'ultra-edgy sword',
    'ue sword': 'ultra-edgy sword',
    'ultra-omega sw': 'ultra-omega sword',
    'ultraomega sw': 'ultra-omega sword',
    'ue armor': 'ultra-edgy armor',
    'godly sw': 'godly sword',
    'g sword': 'godly sword',
    'g sw': 'godly sword',
    'unicorn sw': 'unicorn sword',
    'ruby sw': 'ruby sword',
    'fish sw': 'fish sword',
    'apple sw': 'apple sword',
    'zombie sw': 'zombie sword',
    'wooden sw': 'wooden sword',
    'hair sw': 'hair sword',
    'coin sw': 'coin sword',
    'electronical sw': 'electronical sword',
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


PROFESSIONS = (
    'crafter',
    'enchanter',
    'lootboxer',
    'merchant',
    'worker',
)


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