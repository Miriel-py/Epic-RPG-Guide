# dungeons.py

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import discord
import asyncio
import emojis
import global_data
import database

from discord.ext import commands
from humanfriendly import format_timespan

# dungeon commands (cog)
class dungeonsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Dungeons menu
    @commands.command(aliases=('dungeons',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def dungeonguide(self, ctx):
        embed = await embed_dungeons_menu(ctx)
        await ctx.send(embed=embed)
    
    # Dungeon guide, can be invoked with "dX", "d X", "dungeonX" and "dungeon X"
    dungeon_aliases = ['dungeon','dung','dung15-1','d15-1','dungeon15-1','dung15-2','d15-2','dungeon15-2','dung152','d152','dungeon152','dung151','d151','dungeon151',]
    for x in range(1,16):
        dungeon_aliases.append(f'd{x}')    
        dungeon_aliases.append(f'dungeon{x}') 
        dungeon_aliases.append(f'dung{x}')

    @commands.command(name='d',aliases=(dungeon_aliases))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True, attach_files=True)
    async def dungeon(self, ctx, *args):
        
        invoked = ctx.message.content
        invoked = invoked.lower()
        prefix = ctx.prefix
        prefix = prefix.lower()
        
        if args:
            if len(args)>2:
                if len(args)==3:
                    arg1 = args[0]
                    arg2 = args[1]
                    arg3 = args[2]
                    if arg1.isnumeric() and arg2.isnumeric() and arg3.isnumeric():
                        await ctx.send(f'Uhm, you may have confused this command with the command `{ctx.prefix}dc`.')
                        return
                else:
                    return
            elif len(args) == 2:
                arg = args[0]
                arg = arg.lower()
                if arg == 'gear':
                    page = args[1]
                    if page.isnumeric():
                        page = int(page)
                        if page in (1,2):
                            await dungeongear(ctx, page)
                            return
                    else:
                        await ctx.send(f'The command syntax is `{prefix}dungeon [#]` or `{prefix}d1`-`{prefix}d15`')           
                else:
                    await ctx.send(f'The command syntax is `{prefix}dungeon [#]` or `{prefix}d1`-`{prefix}d15`')
            elif len(args) == 1:
                arg = args[0]
                arg = arg.lower().replace('-','')
                if arg.isnumeric():
                    arg = int(arg)
                    if 1 <= arg <= 15 or arg in (151,152):
                        dungeon_data = await database.get_dungeon_data(ctx, arg)
                        dungeon_embed = await embed_dungeon(dungeon_data, ctx.prefix)
                        if dungeon_embed[0] == '':
                            await ctx.send(embed=dungeon_embed[1])
                        else:
                            await ctx.send(file=dungeon_embed[0], embed=dungeon_embed[1])
                    else:
                        await ctx.send(f'There is no dungeon {arg}, lol.') 
                else:
                    if arg == 'gear':
                        await dungeongear(ctx, '1')
                        return
                    elif arg == 'stats':
                        await dungeonstats(ctx)
                        return
                    else:
                        await ctx.send(f'The command syntax is `{prefix}dungeon [#]` or `{prefix}d1`-`{prefix}d15`')
        else:
            dungeon_no = invoked.replace(f'{prefix}dungeons','').replace(f'{prefix}dungeon','').replace(f'{prefix}dung','').replace(f'{prefix}d','').replace('-','')
            if dungeon_no.isnumeric():
                dungeon_no = int(dungeon_no)
                if 1 <= dungeon_no <= 15 or dungeon_no in (151,152):
                    dungeon_data = await database.get_dungeon_data(ctx, dungeon_no)
                    dungeon_embed = await embed_dungeon(dungeon_data, ctx.prefix)
                    if dungeon_embed[0] == '':
                        await ctx.send(embed=dungeon_embed[1])
                    else:
                        await ctx.send(file=dungeon_embed[0], embed=dungeon_embed[1])
                else:
                    await ctx.send(f'There is no dungeon {dungeon_no}, lol.') 
            else:
                if dungeon_no == '':
                    await dungeonguide(ctx)
                    return
                else:
                    await ctx.send(f'The command syntax is `{prefix}dungeon [#]` or `{prefix}d1`-`{prefix}d15`')
    
    # Command "dungeonstats" - Returns recommended stats for all dungeons
    @commands.command(aliases=('dstats','ds',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def dungeonstats(self, ctx):
        rec_stats_data = await database.get_rec_stats_data(ctx)
        embed = await embed_dungeon_rec_stats(rec_stats_data, ctx.prefix)
        await ctx.send(embed=embed)
        
    # Command "dungeongear" - Returns recommended gear for all dungeons
    @commands.command(aliases=('dgear','dg','dg1','dg2',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def dungeongear(self, ctx, *args):
        
        invoked = ctx.message.content
        invoked = invoked.lower()
        
        if args:
            if len(args)>1:
                await ctx.send(f'The command syntax is `{ctx.prefix}{ctx.invoked_with}`, `{ctx.prefix}{ctx.invoked_with} [1-2]` or `{ctx.prefix}dg1`-`{ctx.prefix}dg2`') 
                return
            elif len(args)==1:
                page = args[0]
                if page.isnumeric():
                        page = int(page)
                        if page in (1,2):
                            rec_gear_data = await database.get_rec_gear_data(ctx, page)
                            embed = await embed_dungeon_rec_gear(rec_gear_data, ctx.prefix, page)
                            await ctx.send(embed=embed)
                        else:
                            await ctx.send(f'The command syntax is `{ctx.prefix}{ctx.invoked_with}`, `{ctx.prefix}{ctx.invoked_with} [1-2]` or `{ctx.prefix}dg1`-`{ctx.prefix}dg2`') 
                            return
                else:
                    await ctx.send(f'The command syntax is `{ctx.prefix}{ctx.invoked_with}`, `{ctx.prefix}{ctx.invoked_with} [1-2]` or `{ctx.prefix}dg1`-`{ctx.prefix}dg2`') 
                    return
        else:
            page = invoked.replace(f'{ctx.prefix}dungeongear','').replace(f'{ctx.prefix}dgear','').replace(f'{ctx.prefix}dg','')
            if page.isnumeric():
                page = int(page)
                rec_gear_data = await database.get_rec_gear_data(ctx, page)
                embed = await embed_dungeon_rec_gear(rec_gear_data, ctx.prefix, page)
                await ctx.send(embed=embed)
            else:
                if page == '':
                    rec_gear_data = await database.get_rec_gear_data(ctx, 1)
                    embed = await embed_dungeon_rec_gear(rec_gear_data, ctx.prefix, 1)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f'The command syntax is `{ctx.prefix}{ctx.invoked_with}`, `{ctx.prefix}{ctx.invoked_with} [1-2]` or `{ctx.prefix}dg1`-`{ctx.prefix}dg2`') 
                    return
    
    # Command "dungeoncheck" - Checks user stats against recommended stats
    @commands.command(aliases=('dcheck','dungcheck','dc','check',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def dungeoncheck(self, ctx, *args):
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        def epic_rpg_check(m):
            correct_embed = False
            try:
                ctx_author = str(ctx.author.name).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                embed_author = str(m.embeds[0].author).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                if (embed_author.find(f'{ctx_author}\'s profile') > 1) or (embed_author.find(f'{ctx_author}\'s stats') > 1):
                    correct_embed = True
                else:
                    correct_embed = False
            except:
                correct_embed = False
            
            return m.author.id == 555955826880413696 and m.channel == ctx.channel and correct_embed
        
        try: 
            dungeon_no = 0
            if len(args) == 0:
                explanation = (
                    f'This command shows you for which dungeons your stats are high enough.\n'
                    f'You have the following options:\n'
                    f'{emojis.bp} `{ctx.prefix}{ctx.invoked_with} auto` to let me read your stats.\n{emojis.blank} This works with default profiles (no background) and `rpg stats`.\n'
                    f'{emojis.bp} `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` to provide your stats manually'
                )
                await ctx.send(explanation)
            elif len(args) == 1:
                try:
                    arg = args[0]
                    arg = arg.lower()
                    if arg == 'auto':
                        await ctx.send(
                            f'**{ctx.author.name}**, please type:\n'
                            f'{emojis.bp} `rpg stats` if you are an EPIC RPG donor\n'
                            f'{emojis.blank} or\n'
                            f'{emojis.bp} `rpg p` if you are not\n'
                            f'{emojis.blank} or\n'
                            f'{emojis.bp} `abort` to abort\n\n'
                            f'Note: `rpg p` does **not** work with profile backgrounds.\n'
                            f'If you have a background and are not a donor, please use `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` instead.'
                        )
                        answer_user_profile = await bot.wait_for('message', check=check, timeout = 30)
                        answer = answer_user_profile.content
                        answer = answer.lower()
                        if (answer == 'rpg p') or (answer == 'rpg profile') or (answer == 'rpg stats'):
                            answer_bot_at = await bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                            try:
                                profile = str(answer_bot_at.embeds[0].fields[1])
                            except:
                                try:
                                    profile = str(answer_bot_at.embeds[0].fields[0])
                                except:
                                    await ctx.send(
                                        f'Whelp, something went wrong here, sorry.\n'
                                        f'If you have a profile background, use `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` to provide your stats manually.'
                                    )
                                    return
                            start_at = profile.find('**AT**') + 8
                            end_at = profile.find('<:', start_at) - 2
                            user_at = profile[start_at:end_at]
                            user_at = user_at.replace(',','')
                            start_def = profile.find('**DEF**') + 9
                            end_def = profile.find(':', start_def) - 2
                            user_def = profile[start_def:end_def]
                            user_def = user_def.replace(',','')
                            start_current_life = profile.find('**LIFE**') + 10
                            start_life = profile.find('/', start_current_life) + 1
                            end_life = profile.find('\',', start_life)
                            user_life = profile[start_life:end_life]
                            user_life = user_life.replace(',','')
                        elif (answer == 'abort') or (answer == 'cancel'):
                            await ctx.send('Aborting.')
                            return
                        else:
                            await ctx.send('Wrong input. Aborting.')
                            return
                        if user_at.isnumeric() and user_def.isnumeric() and user_life.isnumeric():
                            user_at = int(user_at)
                            user_def = int(user_def)
                            user_life = int(user_life)
                        else:
                            await ctx.send('Whelp, something went wrong here, sorry. Aborting.')
                            return
                        user_stats = [user_at, user_def, user_life]
                        if dungeon_no == 0:
                            dungeon_check_data = await database.get_dungeon_check_data(ctx)
                            embed = await embed_dungeon_check_stats(dungeon_check_data, user_stats, ctx)
                        else:
                            dungeon_check_data = await database.get_dungeon_check_data(ctx, dungeon_no)
                            embed = await embed_dungeon_check_stats_dungeon_specific(dungeon_check_data, user_stats, ctx)
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send(
                            f'The command syntax is:\n'
                            f'• `{ctx.prefix}{ctx.invoked_with} auto` if you do **not** have a profile background\n'
                            f'or\n'
                            f'•`{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` if you have a profile background.'
                        )
                        return
                except asyncio.TimeoutError as error:
                    await ctx.send(
                        f'**{ctx.author.name}**, couldn\'t find your profile, RIP.\n'
                        f'If you have a profile background: Use `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` instead.'
                    )
            elif len(args) == 3:
                user_at = args[0]
                user_def = args[1]
                user_life = args[2]
                if (user_at.find('-') != -1) or (user_def.find('-') != -1) or (user_life.find('-') != -1):
                    await ctx.send('Did you play backwards? Send a post card from area -5.')
                    return
                else:
                    if user_at.isnumeric() and user_def.isnumeric() and user_life.isnumeric():
                        user_at = int(args[0])
                        user_def = int(args[1])
                        user_life = int(args[2])
                        if (user_at == 0) or (user_def == 0) or (user_life == 0) or (user_at > 10000) or (user_def > 10000) or (user_life > 10000):
                            await ctx.send('NICE STATS. Not gonna buy it though.')
                            return 
                        else:
                            dungeon_check_data = await database.get_dungeon_check_data(ctx)
                            user_stats = [user_at, user_def, user_life]
                            embed = await embed_dungeon_check_stats(dungeon_check_data, user_stats, ctx)
                            await ctx.send(embed=embed)
                    else:
                        await ctx.send('These stats look suspicious. Try actual numbers.')
            else:
                await ctx.send(
                    f'The command syntax is:\n'
                    f'• `{ctx.prefix}{ctx.invoked_with} auto` if you do **not** have a profile background\n'
                    f'or\n'
                    f'•`{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` if you have a profile background.'
                )
        except:
            raise      

    # Command "dungeoncheckX" - Checks user stats against recommended stats of a specific dungeon
    dungeon_check_aliases = ['dcheck1','check1','dungcheck1','dc1','dcheck15-1','check15-1','dungcheck15-1','dc15-1','dcheck151','check151','dungcheck151','dc151','dcheck15-2','check15-2','dungcheck15-2','dc15-2','dcheck152','check152','dungcheck152','dc152',]
    for x in range(2,16):
        dungeon_check_aliases.append(f'dcheck{x}')    
        dungeon_check_aliases.append(f'check{x}')
        dungeon_check_aliases.append(f'dungeoncheck{x}') 
        dungeon_check_aliases.append(f'dungcheck{x}')
        dungeon_check_aliases.append(f'dc{x}')

    @commands.command(aliases=dungeon_check_aliases)
    @commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
    async def dungeoncheck1(self, ctx, *args):
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
            
        def epic_rpg_check(m):
            correct_embed = False
            try:
                ctx_author = str(ctx.author.name).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                embed_author = str(m.embeds[0].author).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                if (embed_author.find(f'{ctx_author}\'s profile') > 1) or (embed_author.find(f'{ctx_author}\'s stats') > 1):
                    correct_embed = True
                else:
                    correct_embed = False
            except:
                correct_embed = False
            
            return m.author.id == 555955826880413696 and m.channel == ctx.channel and correct_embed
        
        try: 
            invoked = ctx.invoked_with
            invoked = invoked.lower()
            
            dungeon_no = invoked.replace('dungeoncheck','').replace('dungcheck','').replace('dcheck','').replace('check','').replace('dc','').replace('-','')
            dungeon_no = int(dungeon_no)
        
            if dungeon_no in (10,15,151,152):
                user_stats = (0,0,0)
                if dungeon_no == 151:
                    dungeon_no = 15
                elif dungeon_no == 152:
                    dungeon_no = 15.2
                dungeon_check_data = await database.get_dungeon_check_data(ctx, dungeon_no)
                embed = await embed_dungeon_check_stats_dungeon_specific(dungeon_check_data, user_stats, ctx)
                await ctx.send(embed=embed)
            else:
                if len(args) == 0:
                    explanation = (
                        f'This command shows you if your stats are high enough for dungeon **{dungeon_no}**.\n'
                        f'You have the following options:\n'
                        f'{emojis.bp} `{ctx.prefix}{ctx.invoked_with} auto` to let me read your stats.\n'
                        f'{emojis.blank} This works with default profiles (no background) and `rpg stats`.\n'
                        f'{emojis.bp} `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` to provide your stats manually'
                    )
                    await ctx.send(explanation)
                elif len(args) == 1:
                    arg = args[0]
                    arg = arg.lower()
                    if arg == 'auto':
                        try:
                            await ctx.send(
                                f'**{ctx.author.name}**, please type:\n'
                                f'{emojis.bp} `rpg stats` if you are an EPIC RPG donor\n'
                                f'{emojis.blank} or\n'
                                f'{emojis.bp} `rpg p` if you are not\n'
                                f'{emojis.blank} or\n'
                                f'{emojis.bp} `abort` to abort\n\n'
                                f'Note: `rpg p` does **not** work with profile backgrounds.\n'
                                f'If you have a background and are not a donor, please use `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` instead.'
                            )
                            answer_user_at = await self.bot.wait_for('message', check=check, timeout = 30)
                            answer = answer_user_at.content
                            answer = answer.lower()
                            if (answer == 'rpg p') or (answer == 'rpg profile') or (answer == 'rpg stats'):
                                answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                                try:
                                    profile = str(answer_bot_at.embeds[0].fields[1])
                                except:
                                    try:
                                        profile = str(answer_bot_at.embeds[0].fields[0])
                                    except:
                                        await ctx.send(
                                            f'Whelp, something went wrong here, sorry.\n'
                                            f'If you have a profile background, use `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` to provide your stats manually.'
                                        )
                                        return
                                start_at = profile.find('**AT**') + 8
                                end_at = profile.find('<:', start_at) - 2
                                user_at = profile[start_at:end_at]
                                start_def = profile.find('**DEF**') + 9
                                end_def = profile.find(':', start_def) - 2
                                user_def = profile[start_def:end_def]
                                start_current_life = profile.find('**LIFE**') + 10
                                start_life = profile.find('/', start_current_life) + 1
                                end_life = profile.find('\',', start_life)
                                user_life = profile[start_life:end_life]
                            elif (answer == 'abort') or (answer == 'cancel'):
                                await ctx.send('Aborting.')
                                return
                            else:
                                await ctx.send('Wrong input. Aborting.')
                                return
                            if user_at.isnumeric() and user_def.isnumeric() and user_life.isnumeric():
                                user_at = int(user_at)
                                user_def = int(user_def)
                                user_life = int(user_life)
                            else:
                                await ctx.send('Whelp, something went wrong here, sorry. Aborting.')
                                return
                            dungeon_check_data = await database.get_dungeon_check_data(ctx, dungeon_no)
                            user_stats = [user_at, user_def, user_life]
                            embed = await embed_dungeon_check_stats_dungeon_specific(dungeon_check_data, user_stats, ctx)
                            await ctx.send(embed=embed)
                        except asyncio.TimeoutError as error:
                            await ctx.send(
                                f'**{ctx.author.name}**, couldn\'t find your profile, RIP.\n'
                                f'If you have a profile background: Use `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` instead.'
                            )
                    else:
                        await ctx.send(
                            f'The command syntax is:\n'
                            f'• `{ctx.prefix}{ctx.invoked_with} auto` if you do **not** have a profile background\n'
                            f'or\n'
                            f'•`{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` if you have a profile background.'
                        )
                        return
                elif len(args) == 3:
                    user_at = args[0]
                    user_def = args[1]
                    user_life = args[2]
                    if (user_at.find('-') != -1) or (user_def.find('-') != -1) or (user_life.find('-') != -1):
                        await ctx.send('Did you play backwards? Send a post card from area -5.')
                        return
                    else:
                        if user_at.isnumeric() and user_def.isnumeric() and user_life.isnumeric():
                            user_at = int(args[0])
                            user_def = int(args[1])
                            user_life = int(args[2])
                            if (user_at == 0) or (user_def == 0) or (user_life == 0) or (user_at > 10000) or (user_def > 10000) or (user_life > 10000):
                                await ctx.send('NICE STATS. Not gonna buy it though.')
                                return 
                            else:
                                dungeon_check_data = await database.get_dungeon_check_data(ctx, dungeon_no)
                                user_stats = [user_at, user_def, user_life]
                                embed = await embed_dungeon_check_stats_dungeon_specific(dungeon_check_data, user_stats, ctx)
                                await ctx.send(embed=embed)
                        else:
                            await ctx.send('These stats look suspicious. Try actual numbers.')
                else:
                    await ctx.send(
                        f'The command syntax is:\n'
                        f'• `{ctx.prefix}{ctx.invoked_with} auto` if you do **not** have a profile background\n'
                        f'or\n'
                        f'•`{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` if you have a profile background.'
                    )
        except:
            raise

# Initialization
def setup(bot):
    bot.add_cog(dungeonsCog(bot))

                  

# --- Redundancies ---
# Guides
guide_dungeon = '`{prefix}d1`-`{prefix}d15` : Guide for dungeon 1~15'
guide_check = '`{prefix}dc{dungeon_no}` : Check if you\'re ready for this dungeon'
guide_check_all = '`{prefix}dc1`-`{prefix}dc15` : Dungeon 1~15 stats check'
guide_gear = '`{prefix}dg` : Recommended gear (all dungeons)'
guide_stats = '`{prefix}ds` : Recommended gear (all dungeons)'



# --- Functions ---
# Create field "Recommended gear"
async def function_design_field_rec_gear(field_rec_gear_data):
    
    player_sword = field_rec_gear_data[0]
    player_sword_enchant = field_rec_gear_data[1]
    player_sword_emoji = getattr(emojis, field_rec_gear_data[2])
    player_armor = field_rec_gear_data[3]
    player_armor_enchant = field_rec_gear_data[4]
    player_armor_emoji = getattr(emojis, field_rec_gear_data[5])
    
    if not player_armor_enchant == '':
        player_armor_enchant = f'[{player_armor_enchant}]'
    
    if not player_sword_enchant == '':
        player_sword_enchant = f'[{player_sword_enchant}]'
    
    field_value = f'{emojis.bp} {player_sword_emoji} {player_sword} {player_sword_enchant}'
    if not player_armor == 'None':
        field_value = f'{field_value}\n{emojis.bp} {player_armor_emoji} {player_armor} {player_armor_enchant}'
    
    return field_value

# Create field "Check dungeon stats" for areas and dungeons
async def function_design_field_check_stats(field_check_stats_data, user_data, prefix, short_version):
    
    user_at = user_data[0]
    user_def = user_data[1]
    user_life = user_data[2]
    
    player_at = field_check_stats_data[0]
    player_def = field_check_stats_data[1]
    player_carry_def = field_check_stats_data[2]
    player_life = field_check_stats_data[3]
    dungeon_no = field_check_stats_data[4]
    
    if not dungeon_no == 15.2:
        dungeon_no = int(dungeon_no)
    
    check_at = 'N/A'
    check_def = 'N/A'
    check_carry_def = 'N/A'
    check_life = 'N/A'
    
    user_at_check_result = 'N/A'
    user_def_check_result = 'N/A'
    user_carry_def_check_result = 'N/A'
    user_life_check_result = 'N/A'
    
    check_results = ''

    if dungeon_no <= 9:
        if not player_at == 0:
            if user_at < player_at:
                if user_def >= player_carry_def:
                    user_at_check_result = 'ignore'
                else:
                    user_at_check_result = 'fail'
            elif user_at >= player_at:
                user_at_check_result = 'pass'
        else:
            check_at = f'{emojis.checkignore} **AT**: -'
        
        if not player_def == 0:
            if user_def < player_def:
                user_def_check_result = 'fail'
            elif user_def >= player_def:
                user_def_check_result = 'pass'
        else:
            check_def = f'{emojis.checkignore} **DEF**: -'
    
        if not player_carry_def == 0:
            if user_def < player_carry_def:
                user_carry_def_check_result = 'fail'
            elif user_def >= player_carry_def:
                user_carry_def_check_result = 'pass'
        else:
            check_carry_def = f'{emojis.checkignore} **Carry DEF**: -'
            
        if not player_life == 0:
            if user_life < player_life:
                if user_def >= player_carry_def:
                        user_life_check_result = 'ignore'
                elif player_life - user_life <= 10:
                    user_life_check_result = 'passA'
                elif 11 <= (player_life - user_life) <= 25:
                    user_life_check_result = 'passB'
                elif 26 <= (player_life - user_life) <= 50:
                    user_life_check_result = 'passC'
                else:
                    user_life_check_result = 'fail'
            elif user_life >= player_life:
                user_life_check_result = 'pass'
        else:
            check_life = f'{emojis.checkignore} **LIFE**: -'
    
    elif dungeon_no == 11:
        if user_at < player_at:
            user_at_check_result = 'fail'
        elif user_at >= player_at:
            user_at_check_result = 'pass'
        if user_life < player_life:
            if user_at_check_result == 'pass':
                if player_life - user_life <= 10:
                    user_life_check_result = 'passA'
                elif 11 <= (player_life - user_life) <= 25:
                    user_life_check_result = 'passB'
                elif 26 <= (player_life - user_life) <= 50:
                    user_life_check_result = 'passC'
                elif (player_life - user_life) <= 200:
                    user_life_check_result = 'warn'
                else:
                    user_life_check_result = 'fail'
            else:
                if player_life - user_life <= 10:
                    user_life_check_result = 'passA'
                elif 11 <= (player_life - user_life) <= 25:
                    user_life_check_result = 'passB'
                elif 26 <= (player_life - user_life) <= 50:
                    user_life_check_result = 'passC'
                else:
                    user_life_check_result = 'fail'
        elif user_life >= player_life:
            user_life_check_result = 'pass'
            
    elif dungeon_no == 12:
        if user_def < player_def:
            user_def_check_result = 'fail'
        elif user_def >= player_def:
            user_def_check_result = 'pass'
        if user_life < player_life:
            if player_life - user_life <= 10:
                user_life_check_result = 'passA'
            elif 11 <= (player_life - user_life) <= 25:
                user_life_check_result = 'passB'
            elif 26 <= (player_life - user_life) <= 50:
                user_life_check_result = 'passC'
            else:
                user_life_check_result = 'fail'
        elif user_life >= player_life:
            user_life_check_result = 'pass'
  
    elif dungeon_no == 13:
        if user_life < player_life:
            user_life_check_result = 'fail'
        else:
            user_life_check_result = 'pass'
  
    elif dungeon_no == 14:
        if user_def < player_def:
            user_def_check_result = 'fail'
        elif user_def >= player_def:
            user_def_check_result = 'pass'
        if user_life < player_life:
            if player_life - user_life <= 10:
                user_life_check_result = 'passA'
            elif 11 <= (player_life - user_life) <= 25:
                user_life_check_result = 'passB'
            elif 26 <= (player_life - user_life) <= 50:
                user_life_check_result = 'passC'
            else:
                user_life_check_result = 'fail'
        elif user_life >= player_life:
            user_life_check_result = 'pass'
            
    if user_at_check_result == 'pass':
        check_at = f'{emojis.checkok} **AT**: {player_at}'
    elif user_at_check_result == 'warn':
        check_at = f'{emojis.checkwarn} **AT**: {player_at}'
    elif user_at_check_result == 'fail':
        check_at = f'{emojis.checkfail} **AT**: {player_at}'
    elif user_at_check_result == 'ignore':
        check_at = f'{emojis.checkignore} **AT**: {player_at}'
    
    if user_def_check_result == 'pass':
        check_def = f'{emojis.checkok} **DEF**: {player_def}'
    elif user_def_check_result == 'warn':
        check_def = f'{emojis.checkwarn} **DEF**: {player_def}'
    elif user_def_check_result == 'fail':
        check_def = f'{emojis.checkfail} **DEF**: {player_def}'
    elif user_def_check_result == 'ignore':
        check_def = f'{emojis.checkignore} **DEF**: {player_def}'
    
    if user_carry_def_check_result == 'pass':
        check_carry_def = f'{emojis.checkok} **Carry DEF**: {player_carry_def}'
    elif user_carry_def_check_result == 'warn':
        check_carry_def = f'{emojis.checkwarn} **Carry DEF**: {player_carry_def}'
    elif user_carry_def_check_result == 'fail':
        check_carry_def = f'{emojis.checkfail} **Carry DEF**: {player_carry_def}'
    elif user_carry_def_check_result == 'ignore':
        check_carry_def = f'{emojis.checkignore} **Carry DEF**: {player_carry_def}'
        
    if user_life_check_result == 'pass':
        check_life = f'{emojis.checkok} **LIFE**: {player_life}'
    elif user_life_check_result == 'passA':
        check_life = f'{emojis.checkok} **LIFE**: {player_life} • {emojis.lifeboost}**A**'
    elif user_life_check_result == 'passB':
        check_life = f'{emojis.checkok} **LIFE**: {player_life} • {emojis.lifeboost}**B**'
    elif user_life_check_result == 'passC':
        check_life = f'{emojis.checkok} **LIFE**: {player_life} • {emojis.lifeboost}**C**'
    elif user_life_check_result == 'warn':
        check_life = f'{emojis.checkwarn} **LIFE**: {player_life}'
    elif user_life_check_result == 'fail':
        check_life = f'{emojis.checkfail} **LIFE**: {player_life}'
    elif user_life_check_result == 'ignore':
        check_life = f'{emojis.checkignore} **LIFE**: {player_life}'
    
    if short_version == True:
        bulletpoint = ''
    else:
        bulletpoint = f'{emojis.bp}'
    
    field_value = ''
    if not check_at == 'N/A':
        field_value =   f'{bulletpoint} {check_at}'
    if not check_def == 'N/A':
        field_value =   f'{field_value}\n{bulletpoint} {check_def}'
    if not check_carry_def == 'N/A':
        field_value =   f'{field_value}\n{bulletpoint} {check_carry_def}'
    if not check_life == 'N/A':
        field_value =   f'{field_value}\n{bulletpoint} {check_life}'
    field_value = field_value.strip()
    if field_value == '':
        field_value = f'{bulletpoint}Stats irrelevant'
    if short_version == True:
        field_value =   f'{field_value}\n{emojis.blank}'                        
    
    if short_version == False:
        user_stats_check_results = [['AT',user_at_check_result], ['DEF', user_def_check_result], ['LIFE', user_life_check_result]]
        player_stats_check = [player_at, player_def, player_life]
        
        if dungeon_no in (10,15,15.2):
            check_results = f'{emojis.bp} Stats are irrelevant for this dungeon'
            if dungeon_no == 10:
                check_results = f'{check_results}\n{emojis.bp} This dungeon has gear requirements (see `{prefix}d{dungeon_no}`)'
            elif dungeon_no in (15,15.2):
                dungeon_no = str(dungeon_no).replace('.','-')
                check_results = f'{check_results}\n{emojis.bp} This dungeon has various requirements (see `{prefix}d{dungeon_no}`)'
        elif dungeon_no == 11:
            if user_at_check_result == 'fail':
                check_results = (
                    f'{emojis.bp} You are not yet ready for this dungeon\n'
                    f'{emojis.bp} You should increase your **AT** to **{player_at}**'
                )
                if user_life_check_result == 'fail':
                    check_results = f'{check_results}\n{emojis.bp} You should increase your **LIFE** to **{player_life}** or more'
            else:
                if user_life_check_result == 'warn':
                    check_results = (
                        f'{emojis.bp} Your **LIFE** is below recommendation (**{player_life}**)\n'
                        f'{emojis.bp} You can still attempt the dungeon though, maybe you get lucky!'
                    )
                elif user_life_check_result == 'fail':
                    check_results = (
                        f'{emojis.bp} You are not yet ready for this dungeon\n'
                        f'{emojis.bp} You should increase your **LIFE** to **{player_life}** or more'
                    )
                else:
                    check_results = (
                        f'{emojis.bp} Your stats are high enough for this dungeon\n'
                        f'{emojis.bp} Note that this dungeon is luck based, so you can still die'
                    )
                    if (user_life_check_result == 'passA'):
                        check_results = f'{check_results}\n{emojis.bp} Note: You need a {emojis.lifeboost} LIFE boost A to reach recommended **LIFE**'
                    if (user_life_check_result == 'passB'):
                        check_results = f'{check_results}\n{emojis.bp} Note: You need a {emojis.lifeboost} LIFE boost B to reach recommended **LIFE**'
                    if (user_life_check_result == 'passC'):
                        check_results = f'{check_results}\n{emojis.bp} Note: You need a {emojis.lifeboost} LIFE boost C to reach recommended **LIFE**'
            check_results = f'{check_results}\n{emojis.bp} This dungeon has gear requirements (see `{prefix}d{dungeon_no}`)'
        elif dungeon_no == 12:
            if (user_def_check_result == 'fail') or (check_life == 'fail'):
                check_results = f'{emojis.bp} You are not yet ready for this dungeon'    
                if user_def_check_result == 'fail':
                    check_results = f'{check_results}\n{emojis.bp} You should increase your **DEF** to **{player_def}**'
                if user_life_check_result == 'fail':
                    check_results = f'{check_results}\n{emojis.bp} You should increase your **LIFE** to **{player_life}** or more'
            else:
                check_results = f'{emojis.bp} You are ready for this dungeon'
                if (user_life_check_result == 'passA'):
                    check_results = f'{check_results}\n{emojis.bp} Note: You need a {emojis.lifeboost} LIFE boost A to reach recommended **LIFE**'
                if (user_life_check_result == 'passB'):
                    check_results = f'{check_results}\n{emojis.bp} Note: You need a {emojis.lifeboost} LIFE boost B to reach recommended **LIFE**'
                if (user_life_check_result == 'passC'):
                    check_results = f'{check_results}\n{emojis.bp} Note: You need a {emojis.lifeboost} LIFE boost C to reach recommended **LIFE**'
                check_results = f'{check_results}\n{emojis.bp} Note that higher **LIFE** will still help in beating the dungeon'    
            check_results = f'{check_results}\n{emojis.bp} This dungeon has gear requirements (see `{prefix}d{dungeon_no}`)'
        elif dungeon_no == 13:
            if user_life_check_result == 'fail':
                check_results = (
                    f'{emojis.bp} You are not yet ready for this dungeon\n'
                    f'{emojis.bp} You should increase your **LIFE** to **{player_life}** or more\n'
                    f'{emojis.bp} The **LIFE** is for crafting the {emojis.swordomega} OMEGA Sword, not the dungeon\n'
                    f'{emojis.bp} **Important**: This is **base LIFE**, before buying a {emojis.lifeboost} LIFE boost'
                )
            else:
                check_results = f'{emojis.bp} Your stats are high enough for this dungeon'
            check_results = f'{check_results}\n{emojis.bp} This dungeon has gear requirements (see `{prefix}d{dungeon_no}`)'
                
        elif dungeon_no == 14:
            if (user_def_check_result == 'fail') or user_life_check_result == 'fail':
                check_results = f'{emojis.bp} You are not yet ready for this dungeon'
                
                if user_def_check_result == 'fail':
                    check_results = f'{check_results}\n{emojis.bp} You should increase your **DEF** to **{player_def}**'
                if user_life_check_result == 'fail':
                    check_results = f'{check_results}\n{emojis.bp} You should increase your **LIFE** to **{player_life}** or more'
            else:
                check_results = f'{emojis.bp} Your stats are high enough for this dungeon'
                if (user_life_check_result == 'passA'):
                    check_results = f'{check_results}\n{emojis.bp} Note: You need a {emojis.lifeboost} LIFE boost A to reach recommended **LIFE**'
                if (user_life_check_result == 'passB'):
                    check_results = f'{check_results}\n{emojis.bp} Note: You need a {emojis.lifeboost} LIFE boost B to reach recommended **LIFE**'
                if (user_life_check_result == 'passC'):
                    check_results = f'{check_results}\n{emojis.bp} Note: You need a {emojis.lifeboost} LIFE boost C to reach recommended **LIFE**'
            check_results = f'{check_results}\n{emojis.bp} This dungeon has gear requirements (see `{prefix}d{dungeon_no}`)'
                
        else:
            if user_carry_def_check_result == 'pass':
                check_results = f'{emojis.bp} You are ready **and** can carry other players'
                for check in user_stats_check_results:
                    if (check[1] == 'ignore') or (check[1] == 'warn'):
                        check_results = f'{check_results}\n{emojis.bp} Your **{check[0]}** is low but can be ignored because of your DEF'
            elif (user_at_check_result == 'fail') or (user_def_check_result == 'fail') or (user_life_check_result == 'fail'):
                check_results = f'{emojis.bp} You are not yet ready for this dungeon'
                for x, check in enumerate(user_stats_check_results):
                    if check[1] == 'fail':
                        check_results = f'{check_results}\n{emojis.bp} You should increase your **{check[0]}** to **{player_stats_check[x]}**'
                check_results = f'{check_results}\n{emojis.bp} However, you can still do this dungeon if you get carried'
            elif (user_at_check_result == 'pass') and (user_def_check_result == 'pass') and ((user_life_check_result == 'pass') or (user_life_check_result == 'passA') or (user_life_check_result == 'passB') or (user_life_check_result == 'passC')):
                check_results = f'{emojis.bp} Your stats are high enough for this dungeon'
                if (user_life_check_result == 'passA'):
                    check_results = f'{check_results}\n{emojis.bp} Note: You need a {emojis.lifeboost} LIFE boost A to reach recommended **LIFE**'
                if (user_life_check_result == 'passB'):
                    check_results = f'{check_results}\n{emojis.bp} Note: You need a {emojis.lifeboost} LIFE boost B to reach recommended **LIFE**'
                if (user_life_check_result == 'passC'):
                    check_results = f'{check_results}\n{emojis.bp} Note: You need a {emojis.lifeboost} LIFE boost C to reach recommended **LIFE**'
            
    else:
        check_results = 'N/A'
        
    return (field_value, check_results)



# --- Embeds ---
# Dungeons menu
async def embed_dungeons_menu(ctx):
        
    prefix = ctx.prefix
    
    dungeon_guide = (
        f'{emojis.bp} `{prefix}dungeon [#]` / `{prefix}d1`-`{prefix}d15` : Guide for dungeon 1~15\n'
        f'{emojis.bp} `{prefix}dgear` / `{prefix}dg` : Recommended gear (all dungeons)\n'
        f'{emojis.bp} `{prefix}dstats` / `{prefix}ds` : Recommended stats (all dungeons)'
    )
    
    statscheck = (
        f'{emojis.bp} `{prefix}dc1`-`{prefix}dc15` : Dungeon 1~15 stats check\n'
        f'{emojis.bp} `{prefix}dcheck` / `{prefix}dc` : Dungeon stats check (all dungeons)'
    )
    
    embed = discord.Embed(
        color = global_data.color,
        title = 'DUNGEON GUIDES',
        description = f'Hey **{ctx.author.name}**, what do you want to know?'
    )    
    
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='DUNGEONS', value=dungeon_guide, inline=False)
    embed.add_field(name='STATS CHECK', value=statscheck, inline=False)
    
    return embed

# Dungeon guide
async def embed_dungeon(dungeon_data, prefix):
    
    dungeon_no = dungeon_data[0]
    dungeon_tt = dungeon_data[1]
    boss_name = dungeon_data[2]
    boss_emoji = getattr(emojis, dungeon_data[3])
    boss_at = dungeon_data[4]
    boss_life = dungeon_data[5]
    min_players = dungeon_data[6]
    max_players = dungeon_data[7]
    key_price = dungeon_data[8]
    player_at = dungeon_data[9]
    player_def = dungeon_data[10]
    player_carry_def = dungeon_data[11]
    player_life = dungeon_data[12]
    life_boost = dungeon_data[13]
    player_level = dungeon_data[14]
    player_sword = dungeon_data[15]
    player_sword_enchant = dungeon_data[16]
    player_armor = dungeon_data[17]
    player_armor_enchant = dungeon_data[18]
    time_limit = format_timespan(dungeon_data[19])
    player_sword_emoji = getattr(emojis, dungeon_data[20])
    player_armor_emoji = getattr(emojis, dungeon_data[21])
    img_dungeon = ''
    image_url = ''
    
    field_rec_stats_data = (player_at, player_def, player_carry_def, player_life, life_boost, player_level, dungeon_no)
    field_rec_stats = await global_data.design_field_rec_stats(field_rec_stats_data)
    
    field_rec_gear_data = (player_sword, player_sword_enchant, dungeon_data[20], player_armor, player_armor_enchant, dungeon_data[21])
    field_rec_gear = await function_design_field_rec_gear(field_rec_gear_data)
    
    if min_players == max_players:
        players = f'{emojis.bp} {min_players}'
    else:
        players = f'{emojis.bp} {min_players}-{max_players}'
        boss_life = f'{boss_life} per player'
    
    if boss_at == 0:
        boss_at = '-'
    else:
        boss_at = f'~{boss_at}'
    
    if not boss_life == 0:
        try:
            boss_life = f'{dungeon_data[5]:,}'
        except:
            boss_life = int(dungeon_data[5])
    else:
        boss_life = '-'
    
    if not key_price == 0:
        try:
            key_price = f'{dungeon_data[8]:,}'
        except:
            key_price = int(dungeon_data[8])
        key_price = f'{key_price} coins'
    else:
        key_price = f'You can only enter this dungeon with a {emojis.horset6} T6+ horse.'
    
    if 1 <= dungeon_no <= 9:
        embed_description = 'This is a simple stats based dungeon.'
        requirements = f'{emojis.bp} {emojis.dkey1} Dungeon key **OR** {emojis.horset6} T6+ horse'
        strategy = f'{emojis.bp} Use `stab` or `power`'
        strategy_name = 'STRATEGY'
        rewards = f'{emojis.bp} Unlocks area {dungeon_no+1:g}'
    elif dungeon_no == 10:
        embed_description = 'This is a scripted strategy dungeon.'
        requirements = (
            f'{emojis.bp} {emojis.dkey1} Dungeon key **OR** {emojis.horset6} T6+ horse\n'
            f'{emojis.bp} {player_sword_emoji} {player_sword}\n {emojis.bp} {player_armor_emoji} {player_armor}'
        )
        strategy = (
            f'{emojis.bp} The player that starts the dungeon gets the attacker role.\n'
            f'{emojis.bp} The other player gets the defender role.\n'
            f'{emojis.bp} Attacker command sequence:\n{emojis.blank} `charge edgy sword` x20\n{emojis.blank} `attack`\n'
            f'{emojis.bp} Defender command sequence:\n{emojis.blank} `weakness spell`\n{emojis.blank} `protect`\n{emojis.blank} `charge edgy armor` x4\n{emojis.blank} `protect` x2\n{emojis.blank} `invulnerability`\n{emojis.blank} `healing spell`\n{emojis.blank} `protect` x5\n'
            f'{emojis.bp} Note: The defender will die before the boss.'
        )
        strategy_name = 'STRATEGY'
        rewards = f'{emojis.bp} Unlocks area {dungeon_no+1:g}'
    elif dungeon_no == 11:
        embed_description = 'This is a randomized puzzle-based dungeon.'
        requirements = (
            f'{emojis.bp} {emojis.dkey1} Dungeon key **OR** {emojis.horset6} T6+ horse\n'\
            f'{emojis.bp} {player_sword_emoji} {player_sword}\n{emojis.bp} {emojis.timetravel} TT {dungeon_tt}+'
        )
        strategy = (
            f'{emojis.bp} You can move left, right, up, down or pass\n'
            f'{emojis.bp} Your goal is to reach and hit the boss until it dies\n'
            f'{emojis.bp} Each point of AT you have does 1 damage to the boss\n'
            f'{emojis.bp} You can only attack if you stand right next to the boss\n'
            f'{emojis.bp} After you hit the boss, your position will reset\n'
            f'{emojis.bp} If you end up on a fireball, you take 100 damage\n'
            f'{emojis.bp} If you pass a turn, you take 10 damage\n'
            f'{emojis.bp} The board scrolls down one line with every move you make\n'
            f'{emojis.bp} You do **not** move down with the board\n'
            f'{emojis.bp} **The board moves first** when you make a move\n'
            f'{emojis.bp} Check the image below to see the movement behaviour\n'
            f'{emojis.bp} For details see the [Wiki](https://epic-rpg.fandom.com/wiki/Dungeon_11)'
        )
        strategy_name = 'TIPS'
        rewards = f'{emojis.bp} Unlocks area {dungeon_no+1:g}'
        img_dungeon = discord.File(global_data.dungeon11, filename='dungeon11.png')
        image_url = 'attachment://dungeon11.png'
        image_name = 'MOVEMENT BEHAVIOUR'
    elif dungeon_no == 12:
        embed_description = 'This is a randomized puzzle-based dungeon.'
        requirements = (
            f'{emojis.bp} {emojis.dkey1} Dungeon key **OR** {emojis.horset6} T6+ horse\n'\
            f'{emojis.bp} {player_armor_emoji} {player_armor}\n{emojis.bp} {emojis.timetravel} TT {dungeon_tt}+'
        )
        strategy = f'{emojis.bp} https://epic-rpg.fandom.com/wiki/Dungeon_12'
        strategy_name = 'TIPS'
        rewards = f'{emojis.bp} Unlocks area {dungeon_no+1:g}'
    elif dungeon_no == 13:
        embed_description = 'This is a trivia themed strategy dungeon.'
        requirements = (
            f'{emojis.bp} {emojis.dkey1} Dungeon key **OR** {emojis.horset6} T6+ horse\n'
            f'{emojis.bp} {player_sword_emoji} {player_sword}\n{emojis.bp} {emojis.timetravel} TT {dungeon_tt}+'
        )
        strategy = (
            f'{emojis.bp} You start in room 1, 2 or 3\n'
            f'{emojis.bp} Your goal is to reach the dragon\'s room\n'
            f'{emojis.bp} In each room you will be asked one question\n'
            f'{emojis.bp} Your answer determines your next room\n'
            f'{emojis.bp} Refer to the image below for a walkthrough\n'
            f'{emojis.bp} For details see the [Wiki](https://epic-rpg.fandom.com/wiki/Dungeon_13)'
        )
        strategy_name = 'STRATEGY'
        rewards = f'{emojis.bp} Unlocks area {dungeon_no+1:g}'
        img_dungeon = discord.File(global_data.dungeon13, filename='dungeon13.png')
        image_url = 'attachment://dungeon13.png'
        image_name = 'WALKTHROUGH'
    elif dungeon_no == 14:
        embed_description = 'This is a strategy dungeon.'
        requirements = (
            f'{emojis.bp} {emojis.dkey1} Dungeon key **OR** {emojis.horset6} T6+ horse\n'
            f'{emojis.bp} {player_armor_emoji} {player_armor}\n{emojis.bp} {emojis.timetravel} TT {dungeon_tt}+'
        )
        strategy = f'{emojis.bp} https://epic-rpg.fandom.com/wiki/Dungeon_14'
        strategy_name = 'STRATEGY'
        boss_life = f'2x {boss_life}'
        rewards = f'{emojis.bp} Unlocks area {dungeon_no+1:g}'
    elif dungeon_no == 15:
        dungeon_no = '15-1'
        embed_description = (
            f'This is a strategy dungeon.\n'
            f'To see part 2 of this dungeon, use `{prefix}d15-2`'
        )
        requirements = (
            f'{emojis.bp} {emojis.horset6} T6+ horse\n'
            f'{emojis.bp} {player_sword_emoji} {player_sword}\n {emojis.bp} {player_armor_emoji} {player_armor}\n'
            f'{emojis.bp} {emojis.petcat} T4+ cat pet\n{emojis.bp} {emojis.petdog} T4+ dog pet\n{emojis.bp} {emojis.petdragon} T4+ dragon pet\n'
            f'{emojis.bp} {emojis.timetravel} TT {dungeon_tt}+'
        )
        strategy = f'{emojis.bp} https://epic-rpg.fandom.com/wiki/Dungeon_15'
        strategy_name = 'STRATEGY'
        rewards = f'{emojis.bp} {emojis.timekey} TIME key to unlock super time travel (see `{prefix}stt`)'
    elif dungeon_no == 15.2:
        dungeon_no = '15-2'
        embed_description = (
            f'This is an **optional** strategy dungeon.\n'
            f'To see part 1 of this dungeon, use `{prefix}d15-1`'
        )
        requirements = (
            f'{emojis.bp} {emojis.horset6} T6+ horse\n'
            f'{emojis.bp} {player_sword_emoji} {player_sword}\n'
            f'{emojis.bp} {emojis.petcat} T4+ cat pet\n{emojis.bp} {emojis.petdog} T4+ dog pet\n{emojis.bp} {emojis.petdragon} T4+ dragon pet\n'
            f'{emojis.bp} {emojis.timetravel} TT {dungeon_tt}+'
        )
        strategy = f'{emojis.bp} Currently unknown'
        strategy_name = 'STRATEGY'
        rewards = f'{emojis.bp} {emojis.timedragonessence} TIME dragon essence\n{emojis.bp} Unlocks area \'The TOP\''
    else:
        embed_description = ''
        rewards = 'N/A'
        requirements = f'{emojis.bp} N/A'
        strategy = f'{emojis.bp} N/A'
        strategy_name = 'STRATEGY'
    
    if isinstance(dungeon_no, float):
        dungeon_no = f'{dungeon_no:g}'
    
    embed_title = f'DUNGEON {dungeon_no}'
    
    guides = (
        f'{emojis.bp} {guide_check.format(prefix=prefix,dungeon_no=dungeon_no)}\n'
        f'{emojis.bp} {guide_gear.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_stats.format(prefix=prefix)}'
    )  
    
    embed = discord.Embed(
        color = global_data.color,
        title = embed_title,
        description = embed_description
    )
    
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='BOSS', value=f'{emojis.bp} {boss_emoji} {boss_name}', inline=False)
    embed.add_field(name='PLAYERS', value=players, inline=False)
    embed.add_field(name='TIME LIMIT', value=f'{emojis.bp} {time_limit}', inline=False)
    embed.add_field(name='REWARDS', value=rewards, inline=False)
    embed.add_field(name='REQUIREMENTS', value=requirements, inline=False)
    embed.add_field(name='DUNGEON KEY PRICE', value=f'{emojis.bp} {key_price}', inline=False)
    embed.add_field(name='BOSS STATS', value=f'{emojis.bp} {emojis.statat} **AT**: {boss_at}\n{emojis.bp} {emojis.statlife} **LIFE**: {boss_life}', inline=False)
    embed.add_field(name='RECOMMENDED GEAR', value=field_rec_gear, inline=False)
    embed.add_field(name='RECOMMENDED STATS', value=field_rec_stats, inline=False)
    embed.add_field(name=strategy_name, value=strategy, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
    if not image_url == '':
        embed.set_image(url=image_url)
        embed.add_field(name=image_name, value=f'** **', inline=False)
    
    return (img_dungeon, embed)

# Recommended stats for all dungeons
async def embed_dungeon_rec_stats(rec_stats_data, prefix):

    guides = (
        f'{emojis.bp} {guide_check_all.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_gear.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_stats.format(prefix=prefix)}'
    ) 
    
    embed = discord.Embed(
        color = global_data.color,
        title = 'RECOMMENDED STATS FOR ALL DUNGEONS',
        description = f'\u200b'
    )    
    
    embed.set_footer(text=await global_data.default_footer(prefix))
    
    for dung_x in rec_stats_data:
        dungeon_no = dung_x[6]
        if dungeon_no == 15:
            dungeon_no = '15-1'
        elif dungeon_no == 15.2:
            dungeon_no = '15-2'
        
        if isinstance(dungeon_no, float):
            dungeon_no = f'{dungeon_no:g}'
        
        field_rec_stats = await global_data.design_field_rec_stats(dung_x, True)
        embed.add_field(name=f'DUNGEON {dungeon_no}', value=field_rec_stats, inline=True)
        
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
            
    return embed

# Recommended gear for all dungeons
async def embed_dungeon_rec_gear(rec_gear_data, prefix, page):

    if page == 1:
        title_value = 'RECOMMENDED GEAR FOR DUNGEONS 1 TO 9'
        description_value = f'➜ See `{prefix}dg2` for dungeons 10 to 15.'
    elif page == 2:
        title_value = 'RECOMMENDED GEAR FOR DUNGEONS 10 TO 15'
        description_value = f'➜ See `{prefix}dg1` for dungeons 1 to 9.'
    
    guides = (
        f'{emojis.bp} {guide_dungeon.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_check_all.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_stats.format(prefix=prefix)}'
    )
                   
    embed = discord.Embed(
        color = global_data.color,
        title = title_value,
        description = description_value
    )    
    
    embed.set_footer(text=await global_data.default_footer(prefix))
    
    for dung_x in rec_gear_data:
        dungeon_no = dung_x[6]
        if dungeon_no == 15:
            dungeon_no = '15-1'
        elif dungeon_no == 15.2:
            dungeon_no = '15-2'
        field_rec_gear = await function_design_field_rec_gear(dung_x)
        if isinstance(dungeon_no, float):
            dungeon_no = f'{dungeon_no:g}'
        embed.add_field(name=f'DUNGEON {dungeon_no}', value=field_rec_gear, inline=False)
    
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
            
    return embed

# Stats check (all dungeons)
async def embed_dungeon_check_stats(dungeon_check_data, user_stats, ctx):

    prefix = ctx.prefix

    legend = (
        f'{emojis.bp} {emojis.checkok} : Stat is above recommendation\n'
        f'{emojis.bp} {emojis.checkfail} : Stat is below recommendation\n'
        f'{emojis.bp} {emojis.checkignore} : Stat is below rec. but you are above carry DEF\n'
        f'{emojis.bp} {emojis.checkwarn} : Stat is below rec. but with a lot of luck it _might_ work\n'
        f'{emojis.bp} {emojis.lifeboost} : LIFE boost you have to buy to reach recommendation'
    )
    
    notes = (
        f'{emojis.bp} You can ignore this check for D1-D9 if you get carried\n'
        f'{emojis.bp} This only checks stats, you may still need certain gear for D10+!\n'
        f'{emojis.bp} Use `{ctx.prefix}dc1`-`{ctx.prefix}dc15` for individual checks with more details'
    )
    
    guides = (
        f'{emojis.bp} {guide_gear.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_stats.format(prefix=prefix)}'
    ) 
    
    embed = discord.Embed(
        color = global_data.color,
        title = 'DUNGEON STATS CHECK',
        description = f'**{ctx.author.name}**, here\'s your check for **{user_stats[0]} AT**, **{user_stats[1]} DEF** and **{user_stats[2]} LIFE.**'
    )    
    
    embed.set_footer(text=await global_data.default_footer(ctx.prefix))
    
    for dung_x in dungeon_check_data:
        dungeon_no = dung_x[4]
        
        field_check_stats = await function_design_field_check_stats(dung_x, user_stats, ctx.prefix, True)
        embed.add_field(name=f'DUNGEON {dungeon_no:g}', value=field_check_stats[0], inline=True)
    
    embed.add_field(name='LEGEND', value=legend, inline=False)
    embed.add_field(name='NOTE', value=notes, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
            
    return embed

# Stats check (dungeon specific)
async def embed_dungeon_check_stats_dungeon_specific(dungeon_check_data, user_stats, ctx):

    prefix = ctx.prefix

    legend =    f'{emojis.bp} {emojis.checkok} : Stat is above recommendation\n'\
                f'{emojis.bp} {emojis.checkfail} : Stat is below recommendation\n'\
                f'{emojis.bp} {emojis.checkignore} : Stat is below rec. but you are above carry DEF\n'\
                f'{emojis.bp} {emojis.checkwarn} : Stat is below rec. but with a lot of luck it _might_ work\n'\
                f'{emojis.bp} {emojis.lifeboost} : LIFE boost you have to buy to reach recommendation'
    
    notes =     f'{emojis.bp} You can ignore this check for D1-D9 if you get carried\n'\
                f'{emojis.bp} This check does **not** take into account required gear for D10+!\n'\
                f'{emojis.bp} Use `{ctx.prefix}dc1`-`{ctx.prefix}dc15` for a few more details'
    
    guides = (
        f'{emojis.bp} {guide_check_all.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_gear.format(prefix=prefix)}\n'
        f'{emojis.bp} {guide_stats.format(prefix=prefix)}'
    ) 
    
    dungeon_no = dungeon_check_data[4]
    
    if dungeon_no == 15:
        dungeon_no = '15-1'
    elif dungeon_no == 15.2:
        dungeon_no = '15-2'
    
    if isinstance(dungeon_no, float):
        dungeon_no = f'{dungeon_no:g}'
    
    embed_title = f'DUNGEON {dungeon_no} STATS CHECK'
    
    field_check_stats = await function_design_field_check_stats(dungeon_check_data, user_stats, prefix, False)
    
    embed = discord.Embed(
        color = global_data.color,
        title = embed_title,
        description = f'**{ctx.author.name}**, here\'s your check for **{user_stats[0]} AT**, **{user_stats[1]} DEF** and **{user_stats[2]} LIFE.**'
    )    
    
    embed.set_footer(text=await global_data.default_footer(ctx.prefix))
    embed.add_field(name='CHECK RESULT', value=field_check_stats[0], inline=False)
    embed.add_field(name='DETAILS', value=field_check_stats[1], inline=False)
    #embed.add_field(name=f'LEGEND', value=legend, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)
            
    return embed