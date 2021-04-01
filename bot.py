# bot.py
import os
import discord
import sqlite3
import shutil
import asyncio
import dungeons
import global_data
import emojis
import areas
import dbl
import aiohttp
import database
import logging

from dotenv import load_dotenv
from discord.ext import commands, tasks
from datetime import datetime
from discord.ext.commands import CommandNotFound
from math import ceil

# Read the bot token from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DBL_TOKEN = os.getenv('DBL_TOKEN')

@tasks.loop(minutes=30.0)
async def update_stats(bot):
    try:
        if not DBL_TOKEN == 'none':
            guilds = len(list(bot.guilds))
            guild_count = {'server_count':guilds}
            header = {'Authorization':DBL_TOKEN}
            async with aiohttp.ClientSession() as session:
                async with session.post('https://top.gg/api/bots/770199669141536768/stats',data=guild_count,headers=header) as r:
                    global_data.logger.info(f'Posted server count ({guilds}), status code: {r.status}')
    except Exception as e:
        global_data.logger.error(f'Failed to post server count: {e}')


          

# --- Command Initialization ---

bot = commands.AutoShardedBot(command_prefix=database.get_prefix_all, help_command=None, case_insensitive=True)
cog_extensions = ['cogs.guilds','cogs.events','cogs.pets', 'cogs.horse','cogs.crafting','cogs.professions','cogs.trading','cogs.timetravel','cogs.misc',]
if __name__ == '__main__':
    for extension in cog_extensions:
        bot.load_extension(extension)



# --- Ready & Join Events ---

# Set bot status when ready
@bot.event
async def on_ready():
    
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'default prefix $'))
    await update_stats.start(bot)
    
# Send message to system channel when joining a server
@bot.event
async def on_guild_join(guild):
    
    try:
        prefix = await database.get_prefix(bot, guild, True)
        
        welcome_message =   f'Hello **{guild.name}**! I\'m here to provide some guidance!\n\n'\
                            f'To get a list of all topics, type `{prefix}guide` (or `{prefix}g` for short).\n'\
                            f'If you don\'t like this prefix, use `{prefix}setprefix` to change it.\n\n'\
                            f'Tip: If you ever forget the prefix, simply ping me with a command.\n\n'\
        
        await guild.system_channel.send(welcome_message)
    except:
        return


# --- Error Handling ---

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    elif isinstance(error, (commands.MissingPermissions)):
        missing_perms = ''
        for missing_perm in error.missing_perms:
            missing_perm = missing_perm.replace('_',' ').title()
            if not missing_perms == '':
                missing_perms = f'{missing_perms}, `{missing_perm}`'
            else:
                missing_perms = f'`{missing_perm}`'
        await ctx.send(f'Sorry **{ctx.author.name}**, you need the permission(s) {missing_perms} to use this command.')
    elif isinstance(error, (commands.BotMissingPermissions)):
        missing_perms = ''
        for missing_perm in error.missing_perms:
            missing_perm = missing_perm.replace('_',' ').title()
            if not missing_perms == '':
                missing_perms = f'{missing_perms}, `{missing_perm}`'
            else:
                missing_perms = f'`{missing_perm}`'
        try:
            await ctx.send(f'Sorry **{ctx.author.name}**, I\'m missing the permission(s) {missing_perms} to be able to run this command.')
        except:
            return
    elif isinstance(error, (commands.NotOwner)):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'You\'re missing some arguments.')
    elif isinstance(error, database.FirstTimeUser):
        return
    else:
        await database.log_error(ctx, error) # To the database you go



# --- Server Settings ---
   
# Command "setprefix" - Sets new prefix (if user has "manage server" permission)
@bot.command()
@commands.has_permissions(manage_guild=True)
@commands.bot_has_permissions(send_messages=True)
async def setprefix(ctx, *new_prefix):
    
    if new_prefix:
        if len(new_prefix)>1:
            await ctx.send(f'The command syntax is `{ctx.prefix}setprefix [prefix]`')
        else:
            await database.set_prefix(bot, ctx, new_prefix[0])
            await ctx.send(f'Prefix changed to `{await database.get_prefix(bot, ctx)}`')
    else:
        await ctx.send(f'The command syntax is `{ctx.prefix}setprefix [prefix]`')

# Command "prefix" - Returns current prefix
@bot.command()
@commands.bot_has_permissions(send_messages=True)
async def prefix(ctx):
    
    current_prefix = await database.get_prefix(bot, ctx)
    await ctx.send(f'The prefix for this server is `{current_prefix}`\nTo change the prefix use `{current_prefix}setprefix [prefix]`')



# --- User Settings ---

# Command "settings" - Returns current user progress settings
@bot.command(aliases=('me',))
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def settings(ctx):
    
    current_settings = await database.get_settings(ctx)
    if current_settings == None:
        await database.first_time_user(bot, ctx)
        return
    
    if current_settings:
        username = ctx.author.name
        ascension = current_settings[1]
        
        settings = f'{emojis.bp} Current run: **TT {current_settings[0]}**\n'\
                   f'{emojis.bp} Ascension: **{ascension.capitalize()}**'
        
        embed = discord.Embed(
        color = global_data.color,
        title = f'USER SETTINGS',
        description =   f'Hey there, **{ctx.author.name}**.\n'\
                        f'These settings are used by some guides to tailor the information to your current progress.'
        )    
        
        embed.set_footer(text=f'Tip: Use {ctx.prefix}setprogress to change your settings.')
        embed.add_field(name=f'YOUR CURRENT SETTINGS', value=settings, inline=False)
        
        await ctx.send(embed=embed)
    
# Command "setprogress" - Sets TT and ascension
@bot.command(aliases=('sp','setpr','setp',))
@commands.bot_has_permissions(send_messages=True)
async def setprogress(ctx):
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    try:
        await ctx.send(f'**{ctx.author.name}**, what **TT** are you currently in? `[0-999]` (type `abort` to abort).')
        answer_tt = await bot.wait_for('message', check=check, timeout = 30)
        answer = answer_tt.content
        answer = answer.lower()
        if (answer == 'abort') or (answer == 'cancel'):
            await ctx.send(f'Aborting.')
            return
        new_tt = answer_tt.content
        if new_tt.isnumeric():
            new_tt = int(answer_tt.content)            
            if 0 <= new_tt <= 999:
                await ctx.send(f'**{ctx.author.name}**, are you **ascended**? `[yes/no]` (type `abort` to abort)')
                answer_ascended = await bot.wait_for('message', check=check, timeout=30)
                answer = answer_ascended.content
                answer = answer.lower()
                if (answer == 'abort') or (answer == 'cancel'):
                    await ctx.send(f'Aborting.')
                    return
                if answer in ['yes','y']:
                    new_ascended = 'ascended'
                    await database.set_progress(bot, ctx, new_tt, new_ascended)
                    current_settings = await database.get_settings(ctx)
                    if current_settings == None:
                        await database.first_time_user(bot, ctx)
                        return
                    await ctx.send(f'Alright **{ctx.author.name}**, your progress is now set to **TT {current_settings[0]}**, **{current_settings[1]}**.')     
                elif answer in ['no','n']:
                    new_ascended = 'not ascended'
                    await database.set_progress(bot, ctx, new_tt, new_ascended)        
                    current_settings = await database.get_settings(ctx)
                    if current_settings == None:
                        await database.first_time_user(bot, ctx)
                        return
                    await ctx.send(f'Alright **{ctx.author.name}**, your progress is now set to **TT {current_settings[0]}**, **{current_settings[1]}**.')     
                else:
                    await ctx.send(f'**{ctx.author.name}**, please answer with `yes` or `no`. Aborting.')
            else:
                await ctx.send(f'**{ctx.author.name}**, please enter a number from 0 to 999. Aborting.')
        else:
            await ctx.send(f'**{ctx.author.name}**, please answer with a valid number. Aborting.')  
    except asyncio.TimeoutError as error:
        await ctx.send(f'**{ctx.author.name}**, you took too long to answer, RIP.')



# --- Main menus ---

# Main menu
@bot.command(name='guide',aliases=('help','g','h',))
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def helpguide(ctx):
    
    prefix = await database.get_prefix(bot, ctx)
    
    progress =  f'{emojis.bp} `{prefix}areas` / `{prefix}a` : Area guides overview\n'\
                f'{emojis.bp} `{prefix}dungeons` / `{prefix}d` : Dungeon guides overview\n'\
                f'{emojis.bp} `{prefix}timetravel` / `{prefix}tt` : Time travel guide\n'\
                f'{emojis.bp} `{prefix}coolness` : Everything known about coolness'
    
    crafting =  f'{emojis.bp} `{prefix}craft` : Recipes mats calculator\n'\
                f'{emojis.bp} `{prefix}dismantle` / `{prefix}dm` : Dismantling calculator\n'\
                f'{emojis.bp} `{prefix}drops` : Monster drops\n'\
                f'{emojis.bp} `{prefix}enchants` / `{prefix}e` : Enchants'
    
    animals =   f'{emojis.bp} `{prefix}horse` : Horse guide\n'\
                f'{emojis.bp} `{prefix}pet` : Pets guide\n'\
    
    trading =   f'{emojis.bp} `{prefix}trading` : Trading guides overview'
                
    professions_value = f'{emojis.bp} `{prefix}professions` / `{prefix}pr` : Professions guide'
    
    guild_overview =    f'{emojis.bp} `{prefix}guild` : Guild guide'
    
    event_overview =    f'{emojis.bp} `{prefix}events` : Event guides overview'
    
    misc =      f'{emojis.bp} `{prefix}codes` : Redeemable codes\n'\
                f'{emojis.bp} `{prefix}duel` : Duelling weapons\n'\
                f'{emojis.bp} `{prefix}tip` : A handy dandy random tip\n'\
                f'{emojis.bp} `{prefix}calc` : A basic calculator'
                
    botlinks =  f'{emojis.bp} `{prefix}invite` : Invite me to your server\n'\
                f'{emojis.bp} `{prefix}support` : Visit the support server\n'\
                f'{emojis.bp} `{prefix}links` : EPIC RPG wiki & support'
                
    settings =  f'{emojis.bp} `{prefix}settings` / `{prefix}me` : Check your user settings\n'\
                f'{emojis.bp} `{prefix}setprogress` / `{prefix}sp` : Change your user settings\n'\
                f'{emojis.bp} `{prefix}prefix` : Check the current prefix'
    
    embed = discord.Embed(
        color = global_data.color,
        title = 'EPIC RPG GUIDE',
        description =   f'Hey **{ctx.author.name}**, what do you want to know?'
    )    
    embed.set_footer(text=f'Tip: If you ever forget the prefix, simply ping me with the command \'prefix\'.')
    embed.add_field(name='PROGRESS', value=progress, inline=False)
    embed.add_field(name='CRAFTING', value=crafting, inline=False)
    embed.add_field(name='HORSE & PETS', value=animals, inline=False)
    embed.add_field(name='TRADING', value=trading, inline=False)
    embed.add_field(name='PROFESSIONS', value=professions_value, inline=False)
    embed.add_field(name='GUILD', value=guild_overview, inline=False)
    embed.add_field(name='EVENTS', value=event_overview, inline=False)
    embed.add_field(name='MISC', value=misc, inline=False)
    embed.add_field(name='LINKS', value=botlinks, inline=False)
    embed.add_field(name='SETTINGS', value=settings, inline=False)
    
    await ctx.send(embed=embed)


# Areas menu
@bot.command(aliases=('areas',))
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def areaguide(ctx):
    
    prefix = await database.get_prefix(bot, ctx)
    
    area_guide =    f'{emojis.bp} `{prefix}area [#]` / `{prefix}a1`-`{prefix}a15` : Guide for area 1~15'
                    
    trading =       f'{emojis.bp} `{prefix}trades [#]` / `{prefix}tr1`-`{prefix}tr15` : Trades in area 1~15\n'\
                    f'{emojis.bp} `{prefix}trades` / `{prefix}tr` : Trades (all areas)\n'\
                    f'{emojis.bp} `{prefix}traderates` / `{prefix}trr` : Trade rates (all areas)'
    
    drops =         f'{emojis.bp} `{prefix}drops` : Monster drops'
    
    embed = discord.Embed(
        color = global_data.color,
        title = 'AREA GUIDES',
        description =   f'Hey **{ctx.author.name}**, what do you want to know?'
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='AREAS', value=area_guide, inline=False)
    embed.add_field(name='TRADING', value=trading, inline=False)
    embed.add_field(name='MONSTER DROPS', value=drops, inline=False)
    
    await ctx.send(embed=embed)
    
# Dungeons menu
@bot.command(aliases=('dungeons',))
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def dungeonguide(ctx):
    
    prefix = await database.get_prefix(bot, ctx)
    
    dungeon_guide = f'{emojis.bp} `{prefix}dungeon [#]` / `{prefix}d1`-`{prefix}d15` : Guide for dungeon 1~15\n'\
                    f'{emojis.bp} `{prefix}dgear` / `{prefix}dg` : Recommended gear (all dungeons)\n'\
                    f'{emojis.bp} `{prefix}dstats` / `{prefix}ds` : Recommended stats (all dungeons)'
    
    statscheck =    f'{emojis.bp} `{prefix}dc1`-`{prefix}dc15` : Dungeon 1~15 stats check\n'\
                    f'{emojis.bp} `{prefix}dcheck` / `{prefix}dc` : Dungeon stats check (all dungeons)'
    
    embed = discord.Embed(
        color = global_data.color,
        title = 'DUNGEON GUIDES',
        description =   f'Hey **{ctx.author.name}**, what do you want to know?'
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='DUNGEONS', value=dungeon_guide, inline=False)
    embed.add_field(name='STATS CHECK', value=statscheck, inline=False)
    
    await ctx.send(embed=embed)

# Trading menu
@commands.bot_has_permissions(send_messages=True, embed_links=True)
@bot.command(aliases=('trading',))
async def tradingguide(ctx):
    
    prefix = await database.get_prefix(bot, ctx)
                    
    trading = (
        f'{emojis.bp} `{prefix}trades [#]` / `{prefix}tr1`-`{prefix}tr15` : Trades in area 1~15\n'
        f'{emojis.bp} `{prefix}trades` / `{prefix}tr` : Trades (all areas)\n'
        f'{emojis.bp} `{prefix}traderates` / `{prefix}trr` : Trade rates\n'
        f'{emojis.bp} `{prefix}tradecalc` / `{prefix}trc` : Trade calculator'
    )
    
    embed = discord.Embed(
        color = global_data.color,
        title = 'TRADING GUIDES',
        description =   f'Hey **{ctx.author.name}**, what do you want to know?'
    )    
    embed.set_footer(text=await global_data.default_footer(prefix))
    embed.add_field(name='TRADING', value=trading, inline=False)
    
    await ctx.send(embed=embed)



# --- Dungeons ---

# Command for dungeons, can be invoked with "dX", "d X", "dungeonX" and "dungeon X"
dungeon_aliases = ['dungeon','dung','dung15-1','d15-1','dungeon15-1','dung15-2','d15-2','dungeon15-2','dung152','d152','dungeon152','dung151','d151','dungeon151',]
for x in range(1,16):
    dungeon_aliases.append(f'd{x}')    
    dungeon_aliases.append(f'dungeon{x}') 
    dungeon_aliases.append(f'dung{x}')

@bot.command(name='d',aliases=(dungeon_aliases))
@commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True, attach_files=True)
async def dungeon(ctx, *args):
    
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
                    dungeon_embed = await dungeons.dungeon(dungeon_data, ctx.prefix)
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
                dungeon_embed = await dungeons.dungeon(dungeon_data, ctx.prefix)
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
@bot.command(aliases=('dstats','ds',))
@commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
async def dungeonstats(ctx):
    
    rec_stats_data = await database.get_rec_stats_data(ctx)
    
    embed = await dungeons.dungeon_rec_stats(rec_stats_data, ctx.prefix)
    
    await ctx.send(embed=embed)
    
# Command "dungeongear" - Returns recommended gear for all dungeons
@bot.command(aliases=('dgear','dg','dg1','dg2',))
@commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
async def dungeongear(ctx, *args):
    
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
                        embed = await dungeons.dungeon_rec_gear(rec_gear_data, ctx.prefix, page)
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
            embed = await dungeons.dungeon_rec_gear(rec_gear_data, ctx.prefix, page)
            await ctx.send(embed=embed)
        else:
            if page == '':
                rec_gear_data = await database.get_rec_gear_data(ctx, 1)
                embed = await dungeons.dungeon_rec_gear(rec_gear_data, ctx.prefix, 1)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f'The command syntax is `{ctx.prefix}{ctx.invoked_with}`, `{ctx.prefix}{ctx.invoked_with} [1-2]` or `{ctx.prefix}dg1`-`{ctx.prefix}dg2`') 
                return

# Command "dungeoncheck" - Checks user stats against recommended stats
@bot.command(aliases=('dcheck','dungcheck','dc','check',))
@commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
async def dungeoncheck(ctx, *args):
    
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
            explanation =   f'This command shows you for which dungeons your stats are high enough.\n'\
                            f'You have the following options:\n'\
                            f'{emojis.bp} `{ctx.prefix}{ctx.invoked_with} auto` to let me read your stats.\n{emojis.blank} This works with default profiles (no background) and `rpg stats`.\n'\
                            f'{emojis.bp} `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` to provide your stats manually'
            await ctx.send(explanation)
        elif len(args) == 1:
            try:
                arg = args[0]
                arg = arg.lower()
                if arg == 'auto':
                    await ctx.send(f'**{ctx.author.name}**, please type:\n{emojis.bp} `rpg stats` if you are an EPIC RPG donor\n{emojis.blank} or\n{emojis.bp} `rpg p` if you are not\n{emojis.blank} or\n{emojis.bp} `abort` to abort\n\nNote: `rpg p` does **not** work with profile backgrounds.\nIf you have a background and are not a donor, please use `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` instead.')
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
                                await ctx.send(f'Whelp, something went wrong here, sorry.\nIf you have a profile background, use `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` to provide your stats manually.')
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
                        await ctx.send(f'Aborting.')
                        return
                    else:
                        await ctx.send(f'Wrong input. Aborting.')
                        return
                    if user_at.isnumeric() and user_def.isnumeric() and user_life.isnumeric():
                        user_at = int(user_at)
                        user_def = int(user_def)
                        user_life = int(user_life)
                    else:
                        await ctx.send(f'Whelp, something went wrong here, sorry. Aborting.')
                        return
                    user_stats = [user_at, user_def, user_life]
                    if dungeon_no == 0:
                        dungeon_check_data = await database.get_dungeon_check_data(ctx)
                        embed = await dungeons.dungeon_check_stats(dungeon_check_data, user_stats, ctx)
                    else:
                        dungeon_check_data = await database.get_dungeon_check_data(ctx, dungeon_no)
                        embed = await dungeons.dungeon_check_stats_dungeon_specific(dungeon_check_data, user_stats, ctx)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f'The command syntax is:\n• `{ctx.prefix}{ctx.invoked_with} auto` if you do **not** have a profile background\nor\n•`{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` if you have a profile background.')
                    return
            except asyncio.TimeoutError as error:
                await ctx.send(f'**{ctx.author.name}**, couldn\'t find your profile, RIP.\nIf you have a profile background: Use `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` instead.')
        elif len(args) == 3:
            user_at = args[0]
            user_def = args[1]
            user_life = args[2]
            if (user_at.find('-') != -1) or (user_def.find('-') != -1) or (user_life.find('-') != -1):
                await ctx.send(f'Did you play backwards? Send a post card from area -5.')
                return
            else:
                if user_at.isnumeric() and user_def.isnumeric() and user_life.isnumeric():
                    user_at = int(args[0])
                    user_def = int(args[1])
                    user_life = int(args[2])
                    if (user_at == 0) or (user_def == 0) or (user_life == 0) or (user_at > 10000) or (user_def > 10000) or (user_life > 10000):
                        await ctx.send(f'NICE STATS. Not gonna buy it though.')
                        return 
                    else:
                        dungeon_check_data = await database.get_dungeon_check_data(ctx)
                        user_stats = [user_at, user_def, user_life]
                        embed = await dungeons.dungeon_check_stats(dungeon_check_data, user_stats, ctx)
                        await ctx.send(embed=embed)
                else:
                    await ctx.send(f'These stats look suspicious. Try actual numbers.')
        else:
            await ctx.send(f'The command syntax is:\n• `{ctx.prefix}{ctx.invoked_with} auto` if you do **not** have a profile background\nor\n•`{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` if you have a profile background.')
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

@bot.command(aliases=dungeon_check_aliases)
@commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
async def dungeoncheck1(ctx, *args):
    
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
        
        dungeon_no = invoked.replace(f'dungeoncheck','').replace(f'dungcheck','').replace(f'dcheck','').replace(f'check','').replace(f'dc','').replace('-','')
        dungeon_no = int(dungeon_no)
    
        if dungeon_no in (10,15,151,152):
            user_stats = (0,0,0)
            if dungeon_no == 151:
                dungeon_no = 15
            elif dungeon_no == 152:
                dungeon_no = 15.2
            dungeon_check_data = await database.get_dungeon_check_data(ctx, dungeon_no)
            embed = await dungeons.dungeon_check_stats_dungeon_specific(dungeon_check_data, user_stats, ctx)
            await ctx.send(embed=embed)
        else:
            if len(args) == 0:
                explanation =   f'This command shows you if your stats are high enough for dungeon **{dungeon_no}**.\n'\
                                f'You have the following options:\n'\
                                f'{emojis.bp} `{ctx.prefix}{ctx.invoked_with} auto` to let me read your stats.\n{emojis.blank} This works with default profiles (no background) and `rpg stats`.\n'\
                                f'{emojis.bp} `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` to provide your stats manually'
                await ctx.send(explanation)
            elif len(args) == 1:
                arg = args[0]
                arg = arg.lower()
                if arg == 'auto':
                    try:
                        await ctx.send(f'**{ctx.author.name}**, please type:\n{emojis.bp} `rpg stats` if you are an EPIC RPG donor\n{emojis.blank} or\n{emojis.bp} `rpg p` if you are not\n{emojis.blank} or\n{emojis.bp} `abort` to abort\n\nNote: `rpg p` does **not** work with profile backgrounds.\nIf you have a background and are not a donor, please use `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` instead.')
                        answer_user_at = await bot.wait_for('message', check=check, timeout = 30)
                        answer = answer_user_at.content
                        answer = answer.lower()
                        if (answer == 'rpg p') or (answer == 'rpg profile') or (answer == 'rpg stats'):
                            answer_bot_at = await bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                            try:
                                profile = str(answer_bot_at.embeds[0].fields[1])
                            except:
                                try:
                                    profile = str(answer_bot_at.embeds[0].fields[0])
                                except:
                                    await ctx.send(f'Whelp, something went wrong here, sorry.\nIf you have a profile background, use `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` to provide your stats manually.')
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
                            await ctx.send(f'Aborting.')
                            return
                        else:
                            await ctx.send(f'Wrong input. Aborting.')
                            return
                        if user_at.isnumeric() and user_def.isnumeric() and user_life.isnumeric():
                            user_at = int(user_at)
                            user_def = int(user_def)
                            user_life = int(user_life)
                        else:
                            await ctx.send(f'Whelp, something went wrong here, sorry. Aborting.')
                            return
                        dungeon_check_data = await database.get_dungeon_check_data(ctx, dungeon_no)
                        user_stats = [user_at, user_def, user_life]
                        embed = await dungeons.dungeon_check_stats_dungeon_specific(dungeon_check_data, user_stats, ctx)
                        await ctx.send(embed=embed)
                    except asyncio.TimeoutError as error:
                        await ctx.send(f'**{ctx.author.name}**, couldn\'t find your profile, RIP.\nIf you have a profile background: Use `{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` instead.')
                else:
                    await ctx.send(f'The command syntax is:\n• `{ctx.prefix}{ctx.invoked_with} auto` if you do **not** have a profile background\nor\n•`{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` if you have a profile background.')
                    return
            elif len(args) == 3:
                user_at = args[0]
                user_def = args[1]
                user_life = args[2]
                if (user_at.find('-') != -1) or (user_def.find('-') != -1) or (user_life.find('-') != -1):
                    await ctx.send(f'Did you play backwards? Send a post card from area -5.')
                    return
                else:
                    if user_at.isnumeric() and user_def.isnumeric() and user_life.isnumeric():
                        user_at = int(args[0])
                        user_def = int(args[1])
                        user_life = int(args[2])
                        if (user_at == 0) or (user_def == 0) or (user_life == 0) or (user_at > 10000) or (user_def > 10000) or (user_life > 10000):
                            await ctx.send(f'NICE STATS. Not gonna buy it though.')
                            return 
                        else:
                            dungeon_check_data = await database.get_dungeon_check_data(ctx, dungeon_no)
                            user_stats = [user_at, user_def, user_life]
                            embed = await dungeons.dungeon_check_stats_dungeon_specific(dungeon_check_data, user_stats, ctx)
                            await ctx.send(embed=embed)
                    else:
                        await ctx.send(f'These stats look suspicious. Try actual numbers.')
            else:
                await ctx.send(f'The command syntax is:\n• `{ctx.prefix}{ctx.invoked_with} auto` if you do **not** have a profile background\nor\n•`{ctx.prefix}{ctx.invoked_with} [AT] [DEF] [LIFE]` if you have a profile background.')
    except:
        raise            



# --- Areas ---

# Command for areas, can be invoked with "aX", "a X", "areaX" and "area X", optional parameter "full" to override the tt setting
area_aliases = ['area',]
for x in range(1,16):
    area_aliases.append(f'a{x}')    
    area_aliases.append(f'area{x}') 

@bot.command(name='a',aliases=(area_aliases))
@commands.bot_has_permissions(external_emojis=True, send_messages=True, embed_links=True)
async def area(ctx, *args):
    
    invoked = ctx.message.content
    invoked = invoked.lower()
    prefix = ctx.prefix
    prefix = prefix.lower()
    if args:
        if len(args) > 2:
            await ctx.send(f'The command syntax is `{prefix}area [#]` or `{prefix}a1`-`{prefix}a15`')           
        elif len(args) == 2:
            try:
                args_full = str(args[1])
                args_full = args_full.lower()
                if args_full == 'full':
                    area_no = invoked.replace(args_full,'').replace(f' ','').replace(f'{prefix}area','').replace(f'{prefix}a','')
                    if area_no.isnumeric():
                        area_no = int(area_no)
                        if 1<= area_no <= 15:
                            area_data = await database.get_area_data(ctx, area_no)
                            user_settings = await database.get_settings(ctx)
                            if user_settings == None:
                                await database.first_time_user(bot, ctx)
                                return
                            traderate_data = await database.get_traderate_data(ctx, area_no)
                            if area_no < 15:
                                traderate_data_next = await database.get_traderate_data(ctx, area_no+1)
                            else:
                                traderate_data_next = ''
                            user_settings_override = (25, user_settings[1],'override',)
                            if area_no in (3,5):
                                mats_data = await database.get_mats_data(ctx, user_settings_override[0])
                            else:
                                mats_data = ''
                            area_embed = await areas.area(area_data, mats_data, traderate_data, traderate_data_next, user_settings_override, ctx.author.name, ctx.prefix)   
                            await ctx.send(embed=area_embed)   
                        else:
                            await ctx.send(f'There is no area {area_no}, lol.')           
            except:
                return
        else:
            try:
                area_no = args[0]
                if area_no.isnumeric():
                    area_no = int(area_no)
                    if 1 <= area_no <= 15:
                        area_data = await database.get_area_data(ctx, area_no)
                        user_settings = await database.get_settings(ctx)
                        if user_settings == None:
                            await database.first_time_user(bot, ctx)
                            return
                        traderate_data = await database.get_traderate_data(ctx, area_no)
                        if area_no < 15:
                            traderate_data_next = await database.get_traderate_data(ctx, area_no+1)
                        else:
                            traderate_data_next = ''
                        if area_no in (3,5):
                            if user_settings[0] <= 25:
                                mats_data = await database.get_mats_data(ctx, user_settings[0])
                            else:
                                mats_data = await database.get_mats_data(ctx, 25)
                        else:
                            mats_data = ''
                        area_embed = await areas.area(area_data, mats_data, traderate_data, traderate_data_next, user_settings, ctx.author.name, ctx.prefix)
                        await ctx.send(embed=area_embed)
                    else:
                        await ctx.send(f'There is no area {area_no}, lol.')
                else:
                    args_full = str(args[0])
                    args_full = args_full.lower()
                    if args_full == 'full':
                        area_no = invoked.replace(args_full,'').replace(f' ','').replace(f'{prefix}area','').replace(f'{prefix}a','')
                        if area_no.isnumeric():
                            area_no = int(area_no)
                            if 1 <= area_no <= 15:
                                area_data = await database.get_area_data(ctx, int(area_no))
                                user_settings = await database.get_settings(ctx)
                                if user_settings == None:
                                    await database.first_time_user(bot, ctx)
                                    return
                                traderate_data = await database.get_traderate_data(ctx, area_no)
                                if area_no < 15:
                                    traderate_data_next = await database.get_traderate_data(ctx, area_no+1)
                                else:
                                    traderate_data_next = ''
                                user_settings_override = (25, user_settings[1],'override',)
                                if area_no in (3,5):
                                    mats_data = await database.get_mats_data(ctx, user_settings_override[0])
                                else:
                                    mats_data = ''
                                area_embed = await areas.area(area_data, mats_data, traderate_data, traderate_data_next, user_settings_override, ctx.author.name, ctx.prefix)   
                                await ctx.send(embed=area_embed)
                            else:
                                await ctx.send(f'There is no area {area_no}, lol.')
                    else:
                        await ctx.send(f'The command syntax is `{prefix}area [#]` or `{prefix}a1`-`{prefix}a15`')           
            except:
                await ctx.send(f'The command syntax is `{prefix}area [#]` or `{prefix}a1`-`{prefix}a15`')           
    else:
        area_no = invoked.replace(f'{prefix}areas','').replace(f'{prefix}area','').replace(f'{prefix}a','')
        if area_no.isnumeric():
            area_no = int(area_no)
            if not area_no == 0:
                area_data = await database.get_area_data(ctx, area_no)
                user_settings = await database.get_settings(ctx)
                if user_settings == None:
                    await database.first_time_user(bot, ctx)
                    return
                traderate_data = await database.get_traderate_data(ctx, area_no)
                if area_no < 15:
                    traderate_data_next = await database.get_traderate_data(ctx, area_no+1)
                else:
                    traderate_data_next = ''
                if area_no in (3,5):
                    if user_settings[0] <= 25:
                        mats_data = await database.get_mats_data(ctx, user_settings[0])
                    else:
                        mats_data = await database.get_mats_data(ctx, 25)
                else:
                    mats_data = ''
                area_embed = await areas.area(area_data, mats_data, traderate_data, traderate_data_next, user_settings, ctx.author.name, ctx.prefix)
        else:
            if area_no == '':
                await areaguide(ctx)
                return
            else:
                await ctx.send(f'Uhm, what.')           
                return
        await ctx.send(embed=area_embed)



# --- Statisticts ---

# Statistics command
@bot.command(aliases=('statistic','statistics,','devstat','ping','about','info','stats'))
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def devstats(ctx):

    guilds = len(list(bot.guilds))
    user_number = await database.get_user_number(ctx)
    latency = bot.latency
    shard_latency = ''
    for x in range(0,len(bot.shards)):
        if bot.shards[x].is_closed() == True:
            shard_active = '**Inactive**'
        else:
            shard_active = 'Active'
        shard_latency = f'{shard_latency}\n{emojis.bp} Shard {x}: {shard_active}, {round(bot.shards[x].latency*1000)} ms latency'
        
    shard_latency = shard_latency.strip()
    
    general = (
        f'{emojis.bp} {guilds:,} servers\n'
        f'{emojis.bp} {len(bot.shards):,} shards\n'
        f'{emojis.bp} {user_number[0]:,} users\n'
        f'{emojis.bp} {round(latency*1000):,} ms average latency'
    )
    
    
    embed = discord.Embed(
        color = global_data.color,
        title = 'BOT STATISTICS'
    )
        
    embed.add_field(name='BOT', value=general, inline=False)
    embed.add_field(name='SHARDS', value=shard_latency, inline=False)
    
    await ctx.send(embed=embed)
    
    

# --- Links --- 

# Command "invite"
@bot.command(aliases=('inv',))
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def invite(ctx):
       
    embed = discord.Embed(
    color = global_data.color,
    title = 'NEED A GUIDE?',
    description = (
        f'I\'d be flattered to visit your server, **{ctx.author.name}**.\n'
        f'You can invite me [here](https://discord.com/api/oauth2/authorize?client_id=770199669141536768&permissions=313344&scope=bot).'
    )
    )    
    
    embed.set_footer(text=await global_data.default_footer(ctx.prefix))
    
    await ctx.send(embed=embed)

# Command "support"
@bot.command(aliases=('supportserver','server',))
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def support(ctx):
       
    embed = discord.Embed(
    color = global_data.color,
    title = f'NEED BOT SUPPORT?',
    description =   f'You can visit the support server [here](https://discord.gg/v7WbhnhbgN).'         
    )    
    
    embed.set_footer(text=await global_data.default_footer(ctx.prefix))
    
    await ctx.send(embed=embed)
    
# Command "links"
@bot.command(aliases=('link','wiki',))
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def links(ctx):
    
    epicrpgguide = (
        f'{emojis.bp} [Support Server](https://discord.gg/v7WbhnhbgN)\n'
        f'{emojis.bp} [Bot Invite](https://discord.com/api/oauth2/authorize?client_id=770199669141536768&permissions=313344&scope=bot)\n'
        f'{emojis.bp} [Vote](https://top.gg/bot/770199669141536768/vote)'  
    )
    
    epicrpg = (
        f'{emojis.bp} [Official Wiki](https://epic-rpg.fandom.com/wiki/EPIC_RPG_Wiki)\n'
        f'{emojis.bp} [Official Server](https://discord.gg/w5dej5m)'
    )
    
    others = (
        f'{emojis.bp} [MY EPIC RPG ROOM](https://discord.gg/myepicrpgroom)\n'
        f'{emojis.bp} [My Epic RPG Reminder](https://discord.gg/kc3GcK44pJ)\n'
    )
    
    embed = discord.Embed(
    color = global_data.color,
    title = 'SOME HELPFUL LINKS',
    description = 'There\'s a whole world out there.'
    )    
    
    embed.set_footer(text=await global_data.default_footer(ctx.prefix))
    embed.add_field(name=f'EPIC RPG', value=epicrpg, inline=False)
    embed.add_field(name=f'EPIC RPG GUIDE', value=epicrpgguide, inline=False)
    
    await ctx.send(embed=embed)

# Command "vote"
@bot.command()
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def vote(ctx):
       
    embed = discord.Embed(
    color = global_data.color,
    title = 'FEEL LIKE VOTING?',
    description = (
        f'That\'s nice of you, **{ctx.author.name}**, thanks!\n'
        f'You can vote for me [here](https://top.gg/bot/770199669141536768/vote).'
    )
    )    
    
    embed.set_footer(text=await global_data.default_footer(ctx.prefix))
    
    await ctx.send(embed=embed)

# Command "donate"
@bot.command()
@commands.bot_has_permissions(send_messages=True)
async def donate(ctx):
    
    await ctx.send(
        f'Aw that\'s nice of you but this is a free bot, you know.\n'
        f'Thanks though :heart:'
    )



# --- Silly Stuff ---

# Command "Panda" - because Panda
@bot.command()
@commands.bot_has_permissions(send_messages=True)
async def panda(ctx):
        
    await ctx.send('All hail Panda! :panda_face:')
    
# Command "Brandon" - because Panda
@bot.command()
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def brandon(ctx):
        
    embed = discord.Embed(
        color = global_data.color,
        title = f'WHAT TO DO WITH BRANDON',
        description = 'Don\'t even _think_ about dismantling him. You monster.'
    )    
    
    await ctx.send(embed=embed)



# --- Owner Commands ---
# Hey there
@bot.command(aliases=('hey','yo'))
@commands.is_owner()
@commands.bot_has_permissions(send_messages=True)
async def test(ctx):
    
    await ctx.send('Hey hey. Oh it\'s you, Miri! Yes I\'m online, thanks for asking.')


# Shutdown command (only I can use it obviously)
@bot.command()
@commands.is_owner()
@commands.bot_has_permissions(send_messages=True)
async def shutdown(ctx):

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    await ctx.send(f'**{ctx.author.name}**, are you **SURE**? `[yes/no]`')
    answer = await bot.wait_for('message', check=check, timeout=30)
    if answer.content.lower() in ['yes','y']:
        await ctx.send(f'Shutting down.')
        await ctx.bot.logout()
    else:
        await ctx.send(f'Phew, was afraid there for a second.')

bot.run(TOKEN)