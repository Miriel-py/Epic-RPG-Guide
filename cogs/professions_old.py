# professions.py

import asyncio
from math import ceil

import discord
from discord.ext import commands

import database
from resources import emojis
from resources import settings
from resources import functions


# profession commands (cog)
class ProfessionsOldCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    pr_aliases = (
        'pr','professions','prof','profs',
        'ascension','asc','prasc','prascension','ascended','ascend','prascend','prascended',
        'prlevel','prlvl','professionslevel','professionslevels','professionlevels','professionsleveling','professionleveling','prlevels','prleveling','proflevel','proflevels','profslevel','profslevels',
        'worker','enchanter','crafter','lootboxer','merchant','prworker','prenchanter','prcrafter','prlootboxer','prmerchant'
    )

    # Command "professions"
    @commands.command(aliases=pr_aliases)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def profession(self, ctx, *args):

        invoked = ctx.invoked_with
        invoked = invoked.lower()

        if args:
            arg = args[0]

            if arg.find('level') > -1:
                embed = await embed_professions_leveling(ctx.prefix)
                await ctx.send(embed=embed)
            elif arg.find('asc') > -1:
                embed = await embed_ascension(ctx.prefix)
                await ctx.send(embed=embed)
            elif arg.find('work') > -1:
                embed = await embed_professions_worker(ctx.prefix)
                await ctx.send(embed=embed)
            elif arg.find('craft') > -1:
                embed = await embed_professions_crafter(ctx.prefix)
                await ctx.send(embed=embed)
            elif arg.find('enchant') > -1:
                embed = await embed_professions_enchanter(ctx.prefix)
                await ctx.send(embed=embed)
            elif arg.find('merchant') > -1:
                embed = await embed_professions_merchant(ctx.prefix)
                await ctx.send(embed=embed)
            elif arg.find('lootbox') > -1:
                embed = await embed_professions_lootboxer(ctx.prefix)
                await ctx.send(embed=embed)
            else:
                embed = await embed_professions_overview(ctx.prefix)
                await ctx.send(embed=embed)
        else:
            if (invoked.find('level') > -1) or (invoked.find('lvl') > -1):
                embed = await embed_professions_leveling(ctx.prefix)
                await ctx.send(embed=embed)
            elif (invoked.find('asc') > -1):
                embed = await embed_ascension(ctx.prefix)
                await ctx.send(embed=embed)
            elif (invoked.find('work') > -1):
                embed = await embed_professions_worker(ctx.prefix)
                await ctx.send(embed=embed)
            elif (invoked.find('craft') > -1):
                embed = await embed_professions_crafter(ctx.prefix)
                await ctx.send(embed=embed)
            elif (invoked.find('enchant') > -1):
                embed = await embed_professions_enchanter(ctx.prefix)
                await ctx.send(embed=embed)
            elif (invoked.find('merchant') > -1):
                embed = await embed_professions_merchant(ctx.prefix)
                await ctx.send(embed=embed)
            elif (invoked.find('lootbox') > -1):
                embed = await embed_professions_lootboxer(ctx.prefix)
                await ctx.send(embed=embed)
            else:
                embed = await embed_professions_overview(ctx.prefix)
                await ctx.send(embed=embed)

    # Command "prc" - Info about crafting
    @commands.command(aliases=('prctotal',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def prc(self, ctx):

        await ctx.send(
            f'To level up crafter, repeatedly craft {emojis.LOG_EPIC} EPIC logs in batches of 500.\n'
            f'See `{ctx.prefix}pr level` for more information.'
        )

    # Command "pre" - Calculate ice cream to craft
    @commands.command()
    @commands.bot_has_permissions(send_messages=True, external_emojis=True)
    async def pre(self, ctx, *args):

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        def epic_rpg_check(m):
            correct_embed = False
            try:
                ctx_author = str(ctx.author.name).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                embed_author = str(m.embeds[0].author).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                if (embed_author.find(f'{ctx_author} u2014 professions') > 1) and (str(m.embeds[0].fields[0]).find(f'Enchanter') > 1):
                    correct_embed = True
                else:
                    correct_embed = False
            except:
                correct_embed = False

            return m.author.id == 555955826880413696 and m.channel == ctx.channel and correct_embed

        if args:
            arg = args[0]
            if arg == 'total':
                if len(args) == 2:
                    arg2 = args[1]
                    await self.pretotal(ctx, arg2)
                    return
                else:
                    await self.pretotal(ctx)
                    return

        try:
            await ctx.send(f'**{ctx.author.name}**, please type `rpg pr enchanter` (or `abort` to abort)')
            answer_user_enchanter = await self.bot.wait_for('message', check=check, timeout = 30)
            answer = answer_user_enchanter.content
            answer = answer.lower()
            if answer in ('rpg pr enchanter','rpg profession enchanter', 'rpg professions enchanter'):
                answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                try:
                    pr_worker = str(answer_bot_at.embeds[0].fields[0])
                except:
                    await ctx.send('Whelp, something went wrong here, sorry.')
                    return
                start_level = pr_worker.find('**Level**') + 11
                end_level = pr_worker.find('(', start_level) - 1
                if end_level == -2:
                    end_level = pr_worker.find('\\n', start_level)
                pr_level = pr_worker[start_level:end_level]
                start_current_xp = pr_worker.find('**XP**') + 8
                end_current_xp = pr_worker.find('/', start_current_xp)
                pr_current_xp = pr_worker[start_current_xp:end_current_xp]
                pr_current_xp = pr_current_xp.replace(',','')
                start_needed_xp = pr_worker.find('/', start_current_xp) + 1
                end_needed_xp = pr_worker.find(f'\'', start_needed_xp)
                pr_needed_xp = pr_worker[start_needed_xp:end_needed_xp]
                pr_needed_xp = pr_needed_xp.replace(',','')
            elif (answer == 'abort') or (answer == 'cancel'):
                await ctx.send('Aborting.')
                return
            else:
                await ctx.send('Wrong input. Aborting.')
                return
            if pr_level.isnumeric():
                pr_level = int(pr_level)
                if pr_current_xp.isnumeric() and pr_needed_xp.isnumeric():
                    pr_current_xp = int(pr_current_xp)
                    pr_needed_xp = int(pr_needed_xp)
                    xp = pr_needed_xp - pr_current_xp
                    ice_cream = ceil(xp / 100)
                    ice_cream_wb = ceil(xp / 110)
                    xp_rest = 100 - (xp % 100)
                    xp_rest_wb = 110 - (xp % 110)
                    if xp_rest == 100:
                        xp_rest = 0
                    if xp_rest_wb == 110:
                        xp_rest_wb = 0

                    profession_data: database.Profession = await database.get_profession('enchanter')

                    output = (
                        f'You need to cook the following amounts of {emojis.FOOD_FRUIT_ICE_CREAM} fruit ice cream:\n'
                        f'{emojis.BP} Level {pr_level} to {pr_level+1}: **{ice_cream:,}** (if world buff: **{ice_cream_wb:,}**)'
                    )

                    next_level = pr_level + 1
                    if profession_data.xp[next_level] is None: await profession_data.update_level(next_level, pr_needed_xp)

                    enchanter_level_no = pr_level + 1
                    for x in range(6):
                        enchanter_level_no += 1
                        enchanter_level_xp = profession_data.xp[enchanter_level_no]
                        if enchanter_level_xp is None:
                            output = (
                                f'{output}\n{emojis.BP} Level {enchanter_level_no}+: No data yet'
                            )
                            break
                        actual_xp = enchanter_level_xp - xp_rest
                        actual_xp_wb = enchanter_level_xp - xp_rest_wb
                        ice_cream = ceil(actual_xp / 100)
                        ice_cream_wb = ceil(actual_xp_wb / 110)
                        xp_rest = 100 - (actual_xp % 100)
                        xp_rest_wb = 110 - (actual_xp_wb % 110)
                        if xp_rest == 100:
                            xp_rest = 0
                        if xp_rest_wb == 110:
                            xp_rest_wb = 0
                        output = (
                            f'{output}\n{emojis.BP} Level {enchanter_level_no-1} to {enchanter_level_no}: '
                            f'**{ice_cream:,}** (if world buff: **{ice_cream_wb:,}**)'
                        )

                    await ctx.send(f'{output}\n\nUse `{ctx.prefix}craft [amount] ice cream` to see what materials you need to craft fruit ice cream.')
                else:
                    await ctx.send('Whelp, something went wrong here, sorry.')
                    return
            else:
                await ctx.send('Whelp, something went wrong here, sorry.')
                return
        except asyncio.TimeoutError as error:
                    await ctx.send(f'**{ctx.author.name}**, couldn\'t find your profession information, RIP.')

    # Command "prl" - Calculate lootboxes to craft
    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def prl(self, ctx, *args):

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        def epic_rpg_check(m):
            correct_embed = False
            try:
                ctx_author = str(ctx.author.name).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                embed_author = str(m.embeds[0].author).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                if (embed_author.find(f'{ctx_author} u2014 professions') > 1) and (str(m.embeds[0].fields[0]).find(f'Lootboxer') > 1):
                    correct_embed = True
                else:
                    correct_embed = False
            except:
                correct_embed = False

            return m.author.id == 555955826880413696 and m.channel == ctx.channel and correct_embed

        if args:
            arg = args[0]
            if arg == 'total':
                if len(args) == 2:
                    arg2 = args[1]
                    await self.prltotal(ctx, arg2)
                    return
                else:
                    await self.prltotal(ctx)
                    return

        try:
            await ctx.send(f'**{ctx.author.name}**, please type `rpg pr lootboxer` (or `abort` to abort)')
            answer_user_lootboxer = await self.bot.wait_for('message', check=check, timeout = 30)
            answer = answer_user_lootboxer.content
            answer = answer.lower()
            if answer in ('rpg pr lootboxer','rpg profession lootboxer', 'rpg professions lootboxer'):
                answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                try:
                    pr_lootboxer = str(answer_bot_at.embeds[0].fields[0])
                except:
                    await ctx.send('Whelp, something went wrong here, sorry.')
                    return
                start_level = pr_lootboxer.find('**Level**') + 11
                end_level = pr_lootboxer.find('(', start_level) - 1
                if end_level == -2:
                    end_level = pr_lootboxer.find('\\n', start_level)
                pr_level = pr_lootboxer[start_level:end_level]
                start_current_xp = pr_lootboxer.find('**XP**') + 8
                end_current_xp = pr_lootboxer.find('/', start_current_xp)
                pr_current_xp = pr_lootboxer[start_current_xp:end_current_xp]
                pr_current_xp = pr_current_xp.replace(',','')
                start_needed_xp = pr_lootboxer.find('/', start_current_xp) + 1
                end_needed_xp = pr_lootboxer.find(f'\'', start_needed_xp)
                pr_needed_xp = pr_lootboxer[start_needed_xp:end_needed_xp]
                pr_needed_xp = pr_needed_xp.replace(',','')
            elif (answer == 'abort') or (answer == 'cancel'):
                await ctx.send('Aborting.')
                return
            else:
                await ctx.send('Wrong input. Aborting.')
                return
            if pr_level.isnumeric():
                pr_level = int(pr_level)
                if pr_current_xp.isnumeric() and pr_needed_xp.isnumeric():
                    pr_level = int(pr_level)
                    pr_current_xp = int(pr_current_xp)
                    pr_needed_xp = int(pr_needed_xp)
                    xp = pr_needed_xp - pr_current_xp
                    lootboxes = ceil(xp / 100)
                    lootboxes_wb = ceil(xp / 110)
                    xp_rest = 100 - (xp % 100)
                    xp_rest_wb = 110 - (xp % 110)
                    if xp_rest == 100:
                        xp_rest = 0
                    if xp_rest_wb == 110:
                        xp_rest_wb = 0

                    profession_data: database.Profession = await database.get_profession('lootboxer')

                    output = (
                        f'You need to cook the following amounts of {emojis.FOOD_FILLED_LOOTBOX} filled lootboxes:\n'\
                        f'{emojis.BP} Level {pr_level} to {pr_level+1}: **{lootboxes:,}** (if world buff: **{lootboxes_wb:,}**)'
                    )

                    next_level = pr_level + 1
                    if profession_data.xp[next_level] is None: await profession_data.update_level(next_level, pr_needed_xp)

                    worker_level_no = pr_level + 1
                    for x in range(6):
                        worker_level_no += 1
                        worker_level_xp = profession_data.xp[worker_level_no]
                        if worker_level_xp is None:
                            output = (
                                f'{output}\n{emojis.BP} Level {worker_level_no}+: No data yet'
                            )
                            break
                        actual_xp = worker_level_xp - xp_rest
                        actual_xp_wb = worker_level_xp - xp_rest_wb
                        lootboxes = ceil(actual_xp / 100)
                        lootboxes_wb = ceil(actual_xp_wb / 110)
                        xp_rest = 100 - (actual_xp % 100)
                        xp_rest_wb = 110 - (actual_xp_wb % 110)
                        if xp_rest == 100:
                            xp_rest = 0
                        if xp_rest_wb == 110:
                            xp_rest_wb = 0
                        output = (
                            f'{output}\n{emojis.BP} Level {worker_level_no-1} to {worker_level_no}: '
                            f'**{lootboxes:,}** (if world buff: **{lootboxes_wb:,}**)'
                        )

                    await ctx.send(f'{output}\n\nUse `{ctx.prefix}craft [amount] lootboxes` to see what materials you need to craft filled lootboxes.')
                else:
                    await ctx.send('Whelp, something went wrong here, sorry.')
                    return
            else:
                await ctx.send('Whelp, something went wrong here, sorry.')
                return
        except asyncio.TimeoutError as error:
                await ctx.send(f'**{ctx.author.name}**, couldn\'t find your profession information, RIP.')

    # Command "prm" - Calculate logs to sell
    @commands.command()
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def prm(self, ctx, *args):

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        def epic_rpg_check(m):
            correct_embed = False
            try:
                ctx_author = str(ctx.author.name).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                embed_author = str(m.embeds[0].author).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                if (embed_author.find(f'{ctx_author} u2014 professions') > 1) and (str(m.embeds[0].fields[0]).find('Merchant') > 1):
                    correct_embed = True
                else:
                    correct_embed = False
            except:
                correct_embed = False

            return m.author.id == 555955826880413696 and m.channel == ctx.channel and correct_embed

        if args:
            arg = args[0]
            if arg == 'total':
                if len(args) == 2:
                    arg2 = args[1]
                    await self.prmtotal(ctx, arg2)
                    return
                else:
                    await self.prmtotal(ctx)
                    return

        try:
            await ctx.send(f'**{ctx.author.name}**, please type `rpg pr merchant` (or `abort` to abort)')
            answer_user_merchant = await self.bot.wait_for('message', check=check, timeout = 30)
            answer = answer_user_merchant.content
            answer = answer.lower()
            if answer in ('rpg pr merchant','rpg profession merchant', 'rpg professions merchant'):
                answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                try:
                    pr_merchant = str(answer_bot_at.embeds[0].fields[0])
                except:
                    await ctx.send('Whelp, something went wrong here, sorry.')
                    return
                start_level = pr_merchant.find('**Level**') + 11
                end_level = pr_merchant.find('(', start_level) - 1
                if end_level == -2:
                        end_level = pr_merchant.find('\\n', start_level)
                pr_level = pr_merchant[start_level:end_level]
                start_current_xp = pr_merchant.find('**XP**') + 8
                end_current_xp = pr_merchant.find('/', start_current_xp)
                pr_current_xp = pr_merchant[start_current_xp:end_current_xp]
                pr_current_xp = pr_current_xp.replace(',','')
                start_needed_xp = pr_merchant.find('/', start_current_xp) + 1
                end_needed_xp = pr_merchant.find(f'\'', start_needed_xp)
                pr_needed_xp = pr_merchant[start_needed_xp:end_needed_xp]
                pr_needed_xp = pr_needed_xp.replace(',','')
            elif (answer == 'abort') or (answer == 'cancel'):
                await ctx.send('Aborting.')
                return
            else:
                await ctx.send('Wrong input. Aborting.')
                return
            if pr_level.isnumeric():
                pr_level = int(pr_level)
                if pr_current_xp.isnumeric() and pr_needed_xp.isnumeric():
                    pr_level = int(pr_level)
                    pr_current_xp = int(pr_current_xp)
                    pr_needed_xp = int(pr_needed_xp)
                    xp = pr_needed_xp - pr_current_xp
                    logs = xp * 5
                    logs_wb = 5 * ceil((logs/1.1) / 5)

                    profession_data: database.Profession = await database.get_profession('merchant')

                    output = f'You need to sell the following amounts of {emojis.LOG} wooden logs:\n'\
                            f'{emojis.BP} Level {pr_level} to {pr_level+1}: **{logs:,}** (if world buff: **{logs_wb:,}**)'

                    next_level = pr_level + 1
                    if profession_data.xp[next_level] is None: await profession_data.update_level(next_level, pr_needed_xp)

                    merchant_level_no = pr_level + 1
                    for x in range(6):
                        merchant_level_no += 1
                        merchant_level_xp = profession_data.xp[merchant_level_no]
                        if merchant_level_xp is None:
                            output = (
                                f'{output}\n{emojis.BP} Level {merchant_level_no}+: No data yet'
                            )
                            break
                        logs = merchant_level_xp * 5
                        logs_wb = 5 * ceil((logs / 1.1) / 5)
                        output = (
                            f'{output}\n{emojis.BP} Level {merchant_level_no-1} to {merchant_level_no}: '
                            f'**{logs:,}** (if world buff: **{logs_wb:,}**)'
                        )
                    await ctx.send(output)
                else:
                    await ctx.send('Whelp, something went wrong here, sorry.')
                    return
            else:
                await ctx.send('Whelp, something went wrong here, sorry.')
                return
        except asyncio.TimeoutError as error:
            await ctx.send(f'**{ctx.author.name}**, couldn\'t find your profession information, RIP.')

    # Command "prw" - Calculate pickaxes to craft
    @commands.command()
    @commands.bot_has_permissions(send_messages=True, external_emojis=True)
    async def prw(self, ctx, *args):

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        def epic_rpg_check(m):
            correct_embed = False
            try:
                ctx_author = str(ctx.author.name).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                embed_author = str(m.embeds[0].author).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                if (embed_author.find(f'{ctx_author} u2014 professions') > 1) and (str(m.embeds[0].fields[0]).find(f'Worker') > 1):
                    correct_embed = True
                else:
                    correct_embed = False
            except:
                correct_embed = False

            return m.author.id == 555955826880413696 and m.channel == ctx.channel and correct_embed

        if args:
            arg = args[0]
            if arg == 'total':
                if len(args) == 2:
                    arg2 = args[1]
                    await self.prwtotal(ctx, arg2)
                    return
                else:
                    await self.prwtotal(ctx)
                    return

        try:
            await ctx.send(f'**{ctx.author.name}**, please type `rpg pr worker` (or `abort` to abort)')
            answer_user_worker = await self.bot.wait_for('message', check=check, timeout = 30)
            answer = answer_user_worker.content
            answer = answer.lower()
            if answer in ('rpg pr worker','rpg profession worker', 'rpg professions worker'):
                answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                try:
                    pr_worker = str(answer_bot_at.embeds[0].fields[0])
                except:
                    await ctx.send('Whelp, something went wrong here, sorry.')
                    return
                start_level = pr_worker.find('**Level**') + 11
                end_level = pr_worker.find('(', start_level) - 1
                if end_level == -2:
                        end_level = pr_worker.find('\\n', start_level)
                pr_level = pr_worker[start_level:end_level]
                start_current_xp = pr_worker.find('**XP**') + 8
                end_current_xp = pr_worker.find('/', start_current_xp)
                pr_current_xp = pr_worker[start_current_xp:end_current_xp]
                pr_current_xp = pr_current_xp.replace(',','')
                start_needed_xp = pr_worker.find('/', start_current_xp) + 1
                end_needed_xp = pr_worker.find(f'\'', start_needed_xp)
                pr_needed_xp = pr_worker[start_needed_xp:end_needed_xp]
                pr_needed_xp = pr_needed_xp.replace(',','')
            elif (answer == 'abort') or (answer == 'cancel'):
                await ctx.send('Aborting.')
                return
            else:
                await ctx.send('Wrong input. Aborting.')
                return
            if pr_level.isnumeric():
                pr_level = int(pr_level)
                if pr_current_xp.isnumeric() and pr_needed_xp.isnumeric():
                    pr_level = int(pr_level)
                    pr_current_xp = int(pr_current_xp)
                    pr_needed_xp = int(pr_needed_xp)
                    xp = pr_needed_xp - pr_current_xp
                    pickaxes = ceil(xp / 100)
                    pickaxes_wb = ceil(xp / 110)
                    xp_rest = 100 - (xp % 100)
                    xp_rest_wb = 110 - (xp % 110)
                    if xp_rest == 100:
                        xp_rest = 0
                    if xp_rest_wb == 110:
                        xp_rest_wb = 0

                    profession_data: database.Profession = await database.get_profession('worker')

                    output = (
                        f'You need to cook the following amounts of {emojis.FOOD_BANANA_PICKAXE} banana pickaxes:\n'
                        f'{emojis.BP} Level {pr_level} to {pr_level+1}: **{pickaxes:,}** (if world buff: **{pickaxes_wb:,}**)'
                    )

                    next_level = pr_level + 1
                    if profession_data.xp[next_level] is None: await profession_data.update_level(next_level, pr_needed_xp)

                    worker_level_no = pr_level + 1
                    for x in range(6):
                        worker_level_no += 1
                        worker_level_xp = profession_data.xp[worker_level_no]
                        if worker_level_xp is None:
                            output = (
                                f'{output}\n{emojis.BP} Level {worker_level_no}+: No data yet'
                            )
                            break
                        actual_xp = worker_level_xp - xp_rest
                        actual_xp_wb = worker_level_xp - xp_rest_wb
                        pickaxes = ceil(actual_xp / 100)
                        pickaxes_wb = ceil(actual_xp_wb / 110)
                        xp_rest = 100 - (actual_xp % 100)
                        xp_rest_wb = 110 - (actual_xp_wb % 110)
                        if xp_rest == 100:
                            xp_rest = 0
                        if xp_rest_wb == 110:
                            xp_rest_wb = 0

                        output = (
                            f'{output}\n{emojis.BP} Level {worker_level_no-1} to {worker_level_no}: '
                            f'**{pickaxes:,}** (if world buff: **{pickaxes_wb:,}**)'
                        )

                    await ctx.send(f'{output}\n\nUse `{ctx.prefix}craft [amount] pickaxe` to see what materials you need to craft banana pickaxes.')
                else:
                    await ctx.send('Whelp, something went wrong here, sorry.')
                    return
            else:
                await ctx.send('Whelp, something went wrong here, sorry.')
                return
        except asyncio.TimeoutError as error:
            await ctx.send(f'**{ctx.author.name}**, couldn\'t find your profession information, RIP.')

    # Command "pretotal" - Calculate total ice cream to craft until level x
    @commands.command()
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def pretotal(self, ctx, *args):

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        def epic_rpg_check(m):
            correct_embed = False
            try:
                ctx_author = str(ctx.author.name).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                embed_author = str(m.embeds[0].author).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                if (embed_author.find(f'{ctx_author} u2014 professions') > 1) and (str(m.embeds[0].fields[0]).find(f'Enchanter') > 1):
                    correct_embed = True
                else:
                    correct_embed = False
            except:
                correct_embed = False

            return m.author.id == 555955826880413696 and m.channel == ctx.channel and correct_embed

        if len(args) == 0:
            try:
                await ctx.send(f'**{ctx.author.name}**, please type `rpg pr enchanter` (or `abort` to abort)')
                answer_user_enchanter = await self.bot.wait_for('message', check=check, timeout = 30)
                answer = answer_user_enchanter.content
                answer = answer.lower()
                if answer in ('rpg pr enchanter','rpg profession enchanter', 'rpg professions enchanter'):
                    answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                    try:
                        pr_enchanter = str(answer_bot_at.embeds[0].fields[0])
                    except:
                        await ctx.send('Whelp, something went wrong here, sorry.')
                        return
                    start_level = pr_enchanter.find('**Level**') + 11
                    end_level = pr_enchanter.find('(', start_level) - 1
                    if end_level == -2:
                        end_level = pr_enchanter.find('\\n', start_level)
                    pr_level = pr_enchanter[start_level:end_level]
                    start_current_xp = pr_enchanter.find('**XP**') + 8
                    end_current_xp = pr_enchanter.find('/', start_current_xp)
                    pr_current_xp = pr_enchanter[start_current_xp:end_current_xp]
                    pr_current_xp = pr_current_xp.replace(',','')
                    start_needed_xp = pr_enchanter.find('/', start_current_xp) + 1
                    end_needed_xp = pr_enchanter.find(f'\'', start_needed_xp)
                    pr_needed_xp = pr_enchanter[start_needed_xp:end_needed_xp]
                    pr_needed_xp = pr_needed_xp.replace(',','')
                elif (answer == 'abort') or (answer == 'cancel'):
                    await ctx.send('Aborting.')
                    return
                else:
                    await ctx.send('Wrong input. Aborting.')
                    return
                if not pr_level.isnumeric() or not pr_current_xp.isnumeric() or not pr_needed_xp.isnumeric():
                    await ctx.send('Whelp, something went wrong here, sorry.')
                    return
                pr_level = int(pr_level)
                profession_data: database.Profession = await database.get_profession('enchanter')
                next_level = pr_level + 1
                if profession_data.xp[next_level] is None: await profession_data.update_level(next_level, pr_needed_xp)
                if pr_level >= 100:
                    await ctx.send(
                        f'Yo hey, I noticed you are over level 100. You have to let me know where to calculate to.\n'
                        f'Use `{ctx.prefix}pretotal [level]` to set a target level.'
                    )
                    return
                pr_current_xp = int(pr_current_xp)
                pr_needed_xp = int(pr_needed_xp)
                xp = pr_needed_xp - pr_current_xp
                ice_cream = ceil(xp / 100)
                ice_cream_wb = ceil(xp / 110)
                xp_rest = 100 - (xp % 100)
                xp_rest_wb = 110 - (xp % 110)
                if xp_rest == 100:
                    xp_rest = 0
                if xp_rest_wb == 110:
                    xp_rest_wb = 0
                ice_cream_total = ice_cream
                ice_cream_total_wb = ice_cream_wb

                for current_level in range(pr_level + 2, 101):
                    enchanter_level_xp = profession_data.xp[current_level]
                    actual_xp = enchanter_level_xp - xp_rest
                    actual_xp_wb = enchanter_level_xp - xp_rest_wb
                    ice_cream = ceil(actual_xp / 100)
                    ice_cream_wb = ceil(actual_xp_wb / 110)
                    ice_cream_total = ice_cream_total + ice_cream
                    ice_cream_total_wb = ice_cream_total_wb + ice_cream_wb
                    xp_rest = 100 - (actual_xp % 100)
                    xp_rest_wb = 110 - (actual_xp_wb % 110)
                    if xp_rest == 100:
                        xp_rest = 0
                    if xp_rest_wb == 110:
                        xp_rest_wb = 0

                await ctx.send(
                    f'You need to cook the following amount of {emojis.FOOD_FRUIT_ICE_CREAM} fruit ice cream to '
                    f'reach level 100:\n'
                    f'{emojis.BP} **{ice_cream_total:,}** without world buff\n'
                    f'{emojis.BP} **{ice_cream_total_wb:,}** with world buff\n\n'
                    f'Use `{ctx.prefix}craft [amount] ice cream` to see how much you need for that.'
                )
            except asyncio.TimeoutError as error:
                await ctx.send(f'**{ctx.author.name}**, couldn\'t find your profession information, RIP.')
                return

        elif len(args) == 1:
            arg = args[0]

            if arg.replace('-','').isnumeric():
                try:
                    level = int(arg)
                except:
                    await ctx.send(
                        f'`{arg}` is not a valid target level. Please enter the level you want me to calculate to.\n'
                        f'Example: `{ctx.prefix}pretotal 80`. If you want me to calculate to level 100, you can omit the level.'
                    )
                    return

                if not 2 <= level <= 200:
                    await ctx.send('You want to reach level what now?')
                    return

                try:
                    await ctx.send(f'**{ctx.author.name}**, please type `rpg pr enchanter` (or `abort` to abort)')
                    answer_user_enchanter = await self.bot.wait_for('message', check=check, timeout = 30)
                    answer = answer_user_enchanter.content
                    answer = answer.lower()
                    if answer in ('rpg pr enchanter','rpg profession enchanter', 'rpg professions enchanter'):
                        answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                        try:
                            pr_enchanter = str(answer_bot_at.embeds[0].fields[0])
                        except:
                            await ctx.send('Whelp, something went wrong here, sorry.')
                            return
                        start_level = pr_enchanter.find('**Level**') + 11
                        end_level = pr_enchanter.find('(', start_level) - 1
                        if end_level == -2:
                            end_level = pr_enchanter.find('\\n', start_level)
                        pr_level = pr_enchanter[start_level:end_level]
                        start_current_xp = pr_enchanter.find('**XP**') + 8
                        end_current_xp = pr_enchanter.find('/', start_current_xp)
                        pr_current_xp = pr_enchanter[start_current_xp:end_current_xp]
                        pr_current_xp = pr_current_xp.replace(',','')
                        start_needed_xp = pr_enchanter.find('/', start_current_xp) + 1
                        end_needed_xp = pr_enchanter.find(f'\'', start_needed_xp)
                        pr_needed_xp = pr_enchanter[start_needed_xp:end_needed_xp]
                        pr_needed_xp = pr_needed_xp.replace(',','')
                    elif (answer_user_enchanter.content == 'abort') or (answer_user_enchanter.content == 'cancel'):
                        await ctx.send(f'Aborting.')
                        return
                    else:
                        await ctx.send(f'Wrong input. Aborting.')
                        return

                    if not pr_level.isnumeric() or not pr_current_xp.isnumeric() or not pr_needed_xp.isnumeric():
                        await ctx.send('Whelp, something went wrong here, sorry.')
                        return
                    pr_level = int(pr_level)
                    profession_data: database.Profession = await database.get_profession('enchanter')
                    next_level = pr_level + 1
                    if profession_data.xp[next_level] is None: await profession_data.update_level(next_level, pr_needed_xp)
                    pr_current_xp = int(pr_current_xp)
                    pr_needed_xp = int(pr_needed_xp)
                    xp = pr_needed_xp - pr_current_xp
                    ice_cream = ceil(xp / 100)
                    ice_cream_wb = ceil(xp / 110)
                    xp_rest = 100 - (xp % 100)
                    xp_rest_wb = 110 - (xp % 110)
                    if xp_rest == 100:
                        xp_rest = 0
                    if xp_rest_wb == 110:
                        xp_rest_wb = 0
                    ice_cream_total = ice_cream
                    ice_cream_total_wb = ice_cream_wb

                    if pr_level >= level:
                        await ctx.send(
                            f'So.\nYou are level {pr_level} and you want to get to level {level}.\n{emojis.WAIT_WHAT}'
                        )
                        return

                    for current_level in range(pr_level + 2, level + 1):
                        if profession_data.xp[current_level] is None:
                            await ctx.send(
                                f'Sorry, I don\'t have enough data yet to calculate the total for up to '
                                f'level {level}. I currently have data up to level **{current_level - 1}**.\n'
                                f'You can use `{ctx.prefix}pre` to calculate the ice cream needed to reach the '
                                f'next level(s) though.'
                            )
                            return
                        enchanter_level_xp = profession_data.xp[current_level]
                        actual_xp = enchanter_level_xp - xp_rest
                        actual_xp_wb = enchanter_level_xp - xp_rest_wb
                        ice_cream = ceil(actual_xp / 100)
                        ice_cream_wb = ceil(actual_xp_wb / 110)
                        ice_cream_total = ice_cream_total + ice_cream
                        ice_cream_total_wb = ice_cream_total_wb + ice_cream_wb
                        xp_rest = 100 - (actual_xp % 100)
                        xp_rest_wb = 110 - (actual_xp_wb % 110)
                        if xp_rest == 100:
                            xp_rest = 0
                        if xp_rest_wb == 110:
                            xp_rest_wb = 0

                    await ctx.send(
                        f'You need to cook the following amount of {emojis.FOOD_FRUIT_ICE_CREAM} fruit ice cream to reach level **{level}**:\n'
                        f'{emojis.BP} **{ice_cream_total:,}** without world buff\n'
                        f'{emojis.BP} **{ice_cream_total_wb:,}** with world buff\n\n'
                        f'Use `{ctx.prefix}craft [amount] ice cream` to see how much you need for that.'
                    )
                except asyncio.TimeoutError as error:
                    await ctx.send(f'**{ctx.author.name}**, couldn\'t find your profession information, RIP.')
                    return
            else:
                await ctx.send('Sir, that is not a valid number.')
                return

        else:
            await ctx.send(
                f'The command syntax is `{ctx.prefix}pretotal [level]`.\n'
                f'If you omit the level, I will calculate the ice cream you need to reach level 100.'
            )
            return

    # Command "prltotal" - Calculate total lootboxes to craft until level x
    @commands.command()
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def prltotal(self, ctx, *args):

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        def epic_rpg_check(m):
            correct_embed = False
            try:
                ctx_author = str(ctx.author.name).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                embed_author = str(m.embeds[0].author).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                if (embed_author.find(f'{ctx_author} u2014 professions') > 1) and (str(m.embeds[0].fields[0]).find(f'Lootboxer') > 1):
                    correct_embed = True
                else:
                    correct_embed = False
            except:
                correct_embed = False

            return m.author.id == 555955826880413696 and m.channel == ctx.channel and correct_embed

        if len(args) == 0:
            try:
                await ctx.send(f'**{ctx.author.name}**, please type `rpg pr lootboxer` (or `abort` to abort)')
                answer_user_lootboxer = await self.bot.wait_for('message', check=check, timeout = 30)
                answer = answer_user_lootboxer.content
                answer = answer.lower()
                if answer in ('rpg pr lootboxer','rpg profession lootboxer', 'rpg professions lootboxer'):
                    answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                    try:
                        pr_lootboxer = str(answer_bot_at.embeds[0].fields[0])
                    except:
                        await ctx.send('Whelp, something went wrong here, sorry.')
                        return
                    start_level = pr_lootboxer.find('**Level**') + 11
                    end_level = pr_lootboxer.find('(', start_level) - 1
                    if end_level == -2:
                        end_level = pr_lootboxer.find('\\n', start_level)
                    pr_level = pr_lootboxer[start_level:end_level]
                    start_current_xp = pr_lootboxer.find('**XP**') + 8
                    end_current_xp = pr_lootboxer.find('/', start_current_xp)
                    pr_current_xp = pr_lootboxer[start_current_xp:end_current_xp]
                    pr_current_xp = pr_current_xp.replace(',','')
                    start_needed_xp = pr_lootboxer.find('/', start_current_xp) + 1
                    end_needed_xp = pr_lootboxer.find(f'\'', start_needed_xp)
                    pr_needed_xp = pr_lootboxer[start_needed_xp:end_needed_xp]
                    pr_needed_xp = pr_needed_xp.replace(',','')
                elif (answer == 'abort') or (answer == 'cancel'):
                    await ctx.send('Aborting.')
                    return
                else:
                    await ctx.send('Wrong input. Aborting.')
                    return
                if not pr_level.isnumeric() or not pr_current_xp.isnumeric() or not pr_needed_xp.isnumeric():
                    await ctx.send('Whelp, something went wrong here, sorry.')
                    return
                pr_level = int(pr_level)
                profession_data: database.Profession = await database.get_profession('lootboxer')
                next_level = pr_level + 1
                if profession_data.xp[next_level] is None: await profession_data.update_level(next_level, pr_needed_xp)
                if pr_level >= 100:
                    await ctx.send(
                        f'Yo hey, I noticed you are over level 100. You have to let me know where to calculate to.\n'
                        f'Use `{ctx.prefix}prltotal [level]` to set a target level.'
                    )
                    return
                pr_current_xp = int(pr_current_xp)
                pr_needed_xp = int(pr_needed_xp)
                xp = pr_needed_xp - pr_current_xp
                lootboxes = ceil(xp / 100)
                lootboxes_wb = ceil(xp / 110)
                xp_rest = 100 - (xp % 100)
                xp_rest_wb = 110 - (xp % 110)
                if xp_rest == 100:
                    xp_rest = 0
                if xp_rest_wb == 110:
                    xp_rest_wb = 0
                lootboxes_total = lootboxes
                lootboxes_total_wb = lootboxes_wb

                for current_level in range(pr_level + 2, 101):
                    lootboxer_level_xp = profession_data.xp[current_level]
                    actual_xp = lootboxer_level_xp - xp_rest
                    actual_xp_wb = lootboxer_level_xp - xp_rest_wb
                    lootboxes = ceil(actual_xp / 100)
                    lootboxes_wb = ceil(actual_xp_wb / 110)
                    lootboxes_total = lootboxes_total + lootboxes
                    lootboxes_total_wb = lootboxes_total_wb + lootboxes_wb
                    xp_rest = 100 - (actual_xp % 100)
                    xp_rest_wb = 110 - (actual_xp_wb % 110)
                    if xp_rest == 100:
                        xp_rest = 0
                    if xp_rest_wb == 110:
                        xp_rest_wb = 0

                await ctx.send(
                    f'You need to cook the following amount of {emojis.FOOD_FILLED_LOOTBOX} filled lootboxes '
                    f'to reach level **100**:\n'
                    f'{emojis.BP} **{lootboxes_total:,}** without world buff\n'
                    f'{emojis.BP} **{lootboxes_total_wb:,}** with world buff\n\n'
                    f'Use `{ctx.prefix}craft [amount] lootboxes` to see how much you need for that.'
                )
            except asyncio.TimeoutError as error:
                await ctx.send(f'**{ctx.author.name}**, couldn\'t find your profession information, RIP.')
                return

        elif len(args) == 1:
            arg = args[0]

            if arg.replace('-','').isnumeric():
                try:
                    level = int(arg)
                except:
                    await ctx.send(
                        f'`{arg}` is not a valid target level. Please enter the level you want me to calculate to.\n'
                        f'Example: `{ctx.prefix}prltotal 80`. If you want me to calculate to level 100, you can omit the level.'
                    )
                    return

                if not 2 <= level <= 200:
                    await ctx.send('You want to reach level what now?')
                    return

                try:
                    await ctx.send(f'**{ctx.author.name}**, please type `rpg pr lootboxer` (or `abort` to abort)')
                    answer_user_lootboxer = await self.bot.wait_for('message', check=check, timeout = 30)
                    answer = answer_user_lootboxer.content
                    answer = answer.lower()
                    if answer in ('rpg pr lootboxer','rpg profession lootboxer', 'rpg professions lootboxer'):
                        answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                        try:
                            pr_lootboxer = str(answer_bot_at.embeds[0].fields[0])
                        except:
                            await ctx.send('Whelp, something went wrong here, sorry.')
                            return
                        start_level = pr_lootboxer.find('**Level**') + 11
                        end_level = pr_lootboxer.find('(', start_level) - 1
                        if end_level == -2:
                            end_level = pr_lootboxer.find('\\n', start_level)
                        pr_level = pr_lootboxer[start_level:end_level]
                        start_current_xp = pr_lootboxer.find('**XP**') + 8
                        end_current_xp = pr_lootboxer.find('/', start_current_xp)
                        pr_current_xp = pr_lootboxer[start_current_xp:end_current_xp]
                        pr_current_xp = pr_current_xp.replace(',','')
                        start_needed_xp = pr_lootboxer.find('/', start_current_xp) + 1
                        end_needed_xp = pr_lootboxer.find(f'\'', start_needed_xp)
                        pr_needed_xp = pr_lootboxer[start_needed_xp:end_needed_xp]
                        pr_needed_xp = pr_needed_xp.replace(',','')
                    elif (answer_user_lootboxer.content == 'abort') or (answer_user_lootboxer.content == 'cancel'):
                        await ctx.send('Aborting.')
                        return
                    else:
                        await ctx.send('Wrong input. Aborting.')
                        return

                    if not pr_level.isnumeric() or not pr_current_xp.isnumeric() or not pr_needed_xp.isnumeric():
                        await ctx.send('Whelp, something went wrong here, sorry.')
                        return
                    pr_level = int(pr_level)
                    profession_data: database.Profession = await database.get_profession('lootboxer')
                    next_level = pr_level + 1
                    if profession_data.xp[next_level] is None: await profession_data.update_level(next_level, pr_needed_xp)
                    pr_current_xp = int(pr_current_xp)
                    pr_needed_xp = int(pr_needed_xp)
                    xp = pr_needed_xp - pr_current_xp
                    lootboxes = ceil(xp / 100)
                    lootboxes_wb = ceil(xp / 110)
                    xp_rest = 100 - (xp % 100)
                    xp_rest_wb = 110 - (xp % 110)
                    if xp_rest == 100:
                        xp_rest = 0
                    if xp_rest_wb == 110:
                        xp_rest_wb = 0
                    lootboxes_total = lootboxes
                    lootboxes_total_wb = lootboxes_wb

                    if pr_level >= level:
                        await ctx.send(
                            f'So.\nYou are level {pr_level} and you want to get to level {level}.\n{emojis.WAIT_WHAT}'
                        )
                        return

                    for current_level in range(pr_level + 2, level + 1):
                        if profession_data.xp[current_level] is None:
                            await ctx.send(
                                f'Sorry, I don\'t have enough data yet to calculate the total for up to '
                                f'level {level}. I currently have data up to level **{current_level - 1}**.\n'
                                f'You can use `{ctx.prefix}prl` to calculate the lootboxes needed to reach the '
                                f'next level(s) though.'
                            )
                            return
                        lootboxer_level_xp = profession_data.xp[current_level]
                        actual_xp = lootboxer_level_xp - xp_rest
                        actual_xp_wb = lootboxer_level_xp - xp_rest_wb
                        lootboxes = ceil(actual_xp / 100)
                        lootboxes_wb = ceil(actual_xp_wb / 110)
                        lootboxes_total = lootboxes_total + lootboxes
                        lootboxes_total_wb = lootboxes_total_wb + lootboxes_wb
                        xp_rest = 100 - (actual_xp % 100)
                        xp_rest_wb = 110 - (actual_xp_wb % 110)
                        if xp_rest == 100:
                            xp_rest = 0
                        if xp_rest_wb == 110:
                            xp_rest_wb = 0

                    await ctx.send(
                        f'You need to cook the following amount of {emojis.FOOD_FILLED_LOOTBOX} filled lootboxes '
                        f'to reach level **{level}**:\n'
                        f'{emojis.BP} **{lootboxes_total:,}** without world buff\n'
                        f'{emojis.BP} **{lootboxes_total_wb:,}** with world buff\n\n'
                        f'Use `{ctx.prefix}craft [amount] lootboxes` to see how much you need for that.'
                    )
                except asyncio.TimeoutError as error:
                    await ctx.send(f'**{ctx.author.name}**, couldn\'t find your profession information, RIP.')
                    return
            else:
                await ctx.send('Sir, that is not a valid number.')
                return

        else:
            await ctx.send(
                f'The command syntax is `{ctx.prefix}prltotal [level]`.\n'
                f'If you omit the level, I will calculate the filled lootboxes you need to reach level 100.'
            )
            return

    # Command "prmtotal" - Calculate total logs to sell until level x
    @commands.command()
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def prmtotal(self, ctx, *args):

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        def epic_rpg_check(m):
            correct_embed = False
            try:
                ctx_author = str(ctx.author.name).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                embed_author = str(m.embeds[0].author).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                if (embed_author.find(f'{ctx_author} u2014 professions') > 1) and (str(m.embeds[0].fields[0]).find(f'Merchant') > 1):
                    correct_embed = True
                else:
                    correct_embed = False
            except:
                correct_embed = False

            return m.author.id == 555955826880413696 and m.channel == ctx.channel and correct_embed

        if len(args) == 0:
            try:
                await ctx.send(f'**{ctx.author.name}**, please type `rpg pr merchant` (or `abort` to abort)')
                answer_user_merchant = await self.bot.wait_for('message', check=check, timeout = 30)
                answer = answer_user_merchant.content
                answer = answer.lower()
                if answer in ('rpg pr merchant','rpg profession merchant', 'rpg professions merchant'):
                    answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                    try:
                        pr_merchant = str(answer_bot_at.embeds[0].fields[0])
                    except:
                        await ctx.send('Whelp, something went wrong here, sorry.')
                        return
                    start_level = pr_merchant.find('**Level**') + 11
                    end_level = pr_merchant.find('(', start_level) - 1
                    if end_level == -2:
                        end_level = pr_merchant.find('\\n', start_level)
                    pr_level = pr_merchant[start_level:end_level]
                    start_current_xp = pr_merchant.find('**XP**') + 8
                    end_current_xp = pr_merchant.find('/', start_current_xp)
                    pr_current_xp = pr_merchant[start_current_xp:end_current_xp]
                    pr_current_xp = pr_current_xp.replace(',','')
                    start_needed_xp = pr_merchant.find('/', start_current_xp) + 1
                    end_needed_xp = pr_merchant.find(f'\'', start_needed_xp)
                    pr_needed_xp = pr_merchant[start_needed_xp:end_needed_xp]
                    pr_needed_xp = pr_needed_xp.replace(',','')
                elif (answer == 'abort') or (answer == 'cancel'):
                    await ctx.send('Aborting.')
                    return
                else:
                    await ctx.send('Wrong input. Aborting.')
                    return
                if not pr_level.isnumeric() or not pr_current_xp.isnumeric() or not pr_needed_xp.isnumeric():
                    await ctx.send('Whelp, something went wrong here, sorry.')
                    return
                pr_level = int(pr_level)
                profession_data: database.Profession = await database.get_profession('merchant')
                next_level = pr_level + 1
                if profession_data.xp[next_level] is None: await profession_data.update_level(next_level, pr_needed_xp)
                if pr_level >= 100:
                    await ctx.send(
                        f'Yo hey, I noticed you are over level 100. You have to let me know where to calculate to.\n'
                        f'Use `{ctx.prefix}prmtotal [level]` to set a target level.'
                    )
                    return
                pr_current_xp = int(pr_current_xp)
                pr_needed_xp = int(pr_needed_xp)
                xp = pr_needed_xp - pr_current_xp
                logs_total = xp * 5

                for current_level in range(pr_level + 2, 101):
                    merchant_level_xp = profession_data.xp[current_level]
                    logs_total = logs_total + (merchant_level_xp * 5)

                logs_total_wb = 5 * ceil((logs_total/1.1) / 5)

                await ctx.send(
                    f'You need to sell the following amount of {emojis.LOG} wooden logs to reach level **100**:\n'
                    f'{emojis.BP} ~**{logs_total:,}** without world buff\n'
                    f'{emojis.BP} ~**{logs_total_wb:,}** with world buff'
                )
            except asyncio.TimeoutError as error:
                await ctx.send(f'**{ctx.author.name}**, couldn\'t find your profession information, RIP.')
                return

        elif len(args) == 1:
            arg = args[0]

            if arg.replace('-','').isnumeric():
                try:
                    level = int(arg)
                except:
                    await ctx.send(
                        f'`{arg}` is not a valid target level. Please enter the level you want me to calculate to.\n'
                        f'Example: `{ctx.prefix}prmtotal 80`. If you want me to calculate to level 100, you can omit the level.'
                    )
                    return

                if not 2 <= level <= 200:
                    await ctx.send('You want to reach level what now?')
                    return

                try:
                    await ctx.send(f'**{ctx.author.name}**, please type `rpg pr merchant` (or `abort` to abort)')
                    answer_user_merchant = await self.bot.wait_for('message', check=check, timeout = 30)
                    answer = answer_user_merchant.content
                    answer = answer.lower()
                    if answer in ('rpg pr merchant','rpg profession merchant', 'rpg professions merchant'):
                        answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                        try:
                            pr_merchant = str(answer_bot_at.embeds[0].fields[0])
                        except:
                            await ctx.send('Whelp, something went wrong here, sorry.')
                            return
                        start_level = pr_merchant.find('**Level**') + 11
                        end_level = pr_merchant.find('(', start_level) - 1
                        if end_level == -2:
                            end_level = pr_merchant.find('\\n', start_level)
                        pr_level = pr_merchant[start_level:end_level]
                        start_current_xp = pr_merchant.find('**XP**') + 8
                        end_current_xp = pr_merchant.find('/', start_current_xp)
                        pr_current_xp = pr_merchant[start_current_xp:end_current_xp]
                        pr_current_xp = pr_current_xp.replace(',','')
                        start_needed_xp = pr_merchant.find('/', start_current_xp) + 1
                        end_needed_xp = pr_merchant.find(f'\'', start_needed_xp)
                        pr_needed_xp = pr_merchant[start_needed_xp:end_needed_xp]
                        pr_needed_xp = pr_needed_xp.replace(',','')
                    elif (answer_user_merchant.content == 'abort') or (answer_user_merchant.content == 'cancel'):
                        await ctx.send('Aborting.')
                        return
                    else:
                        await ctx.send('Wrong input. Aborting.')
                        return

                    if not pr_level.isnumeric() or not pr_current_xp.isnumeric() or not pr_needed_xp.isnumeric():
                        await ctx.send('Whelp, something went wrong here, sorry.')
                        return
                    pr_level = int(pr_level)
                    profession_data: database.Profession = await database.get_profession('merchant')
                    next_level = pr_level + 1
                    if profession_data.xp[next_level] is None: await profession_data.update_level(next_level, pr_needed_xp)
                    pr_current_xp = int(pr_current_xp)
                    pr_needed_xp = int(pr_needed_xp)
                    xp = pr_needed_xp - pr_current_xp
                    logs_total = xp * 5

                    if pr_level >= level:
                        await ctx.send(f'So.\nYou are level {pr_level} and you want to get to level {level}.\n{emojis.WAIT_WHAT}')
                        return

                    for current_level in range(pr_level + 2, level + 1):
                        if profession_data.xp[current_level] is None:
                            await ctx.send(
                                f'Sorry, I don\'t have enough data yet to calculate the total for up to '
                                f'level {level}. I currently have data up to level **{current_level - 1}**.\n'
                                f'You can use `{ctx.prefix}prm` to calculate the logs needed to reach the '
                                f'next level(s) though.'
                            )
                            return
                        merchant_level_xp = profession_data.xp[current_level]
                        logs_total = logs_total + (merchant_level_xp * 5)

                    logs_total_wb = 5 * ceil((logs_total/1.1) / 5)

                    await ctx.send(
                        f'You need to sell the following amount of {emojis.LOG} wooden logs to reach level **{level}**:\n'
                        f'{emojis.BP} ~**{logs_total:,}** without world buff\n'
                        f'{emojis.BP} ~**{logs_total_wb:,}** with world buff'
                    )
                except asyncio.TimeoutError as error:
                    await ctx.send(f'**{ctx.author.name}**, couldn\'t find your profession information, RIP.')
                    return
            else:
                await ctx.send('Sir, that is not a valid number.')
                return

        else:
            await ctx.send(
                f'The command syntax is `{ctx.prefix}prmtotal [level]`.\n'
                f'If you omit the level, I will calculate the logs you need to reach level 100.'
            )
            return

    # Command "prwtotal" - Calculate total pickaxes to craft until level x
    @commands.command()
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def prwtotal(self, ctx, *args):

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        def epic_rpg_check(m):
            correct_embed = False
            try:
                ctx_author = str(ctx.author.name).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                embed_author = str(m.embeds[0].author).encode('unicode-escape',errors='ignore').decode('ASCII').replace('\\','')
                if (embed_author.find(f'{ctx_author} u2014 professions') > 1) and (str(m.embeds[0].fields[0]).find(f'Worker') > 1):
                    correct_embed = True
                else:
                    correct_embed = False
            except:
                correct_embed = False

            return m.author.id == 555955826880413696 and m.channel == ctx.channel and correct_embed

        if len(args) == 0:
            try:
                await ctx.send(f'**{ctx.author.name}**, please type `rpg pr worker` (or `abort` to abort)')
                answer_user_worker = await self.bot.wait_for('message', check=check, timeout = 30)
                answer = answer_user_worker.content
                answer = answer.lower()
                if answer in ('rpg pr worker','rpg profession worker', 'rpg professions worker'):
                    answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                    try:
                        pr_worker = str(answer_bot_at.embeds[0].fields[0])
                    except:
                        await ctx.send('Whelp, something went wrong here, sorry.')
                        return
                    start_level = pr_worker.find('**Level**') + 11
                    end_level = pr_worker.find('(', start_level) - 1
                    if end_level == -2:
                        end_level = pr_worker.find('\\n', start_level)
                    pr_level = pr_worker[start_level:end_level]
                    start_current_xp = pr_worker.find('**XP**') + 8
                    end_current_xp = pr_worker.find('/', start_current_xp)
                    pr_current_xp = pr_worker[start_current_xp:end_current_xp]
                    pr_current_xp = pr_current_xp.replace(',','')
                    start_needed_xp = pr_worker.find('/', start_current_xp) + 1
                    end_needed_xp = pr_worker.find(f'\'', start_needed_xp)
                    pr_needed_xp = pr_worker[start_needed_xp:end_needed_xp]
                    pr_needed_xp = pr_needed_xp.replace(',','')
                elif (answer == 'abort') or (answer == 'cancel'):
                    await ctx.send('Aborting.')
                    return
                else:
                    await ctx.send('Wrong input. Aborting.')
                    return
                if not pr_level.isnumeric() or not pr_current_xp.isnumeric() or not pr_needed_xp.isnumeric():
                    await ctx.send('Whelp, something went wrong here, sorry.')
                    return
                pr_level = int(pr_level)
                profession_data: database.Profession = await database.get_profession('worker')
                next_level = pr_level + 1
                if profession_data.xp[next_level] is None: await profession_data.update_level(next_level, pr_needed_xp)
                if pr_level >= 100:
                    await ctx.send(
                        f'Yo hey, I noticed you are over level 100. You have to let me know where to calculate to.\n'
                        f'Use `{ctx.prefix}prwtotal [level]` to set a target level.'
                    )
                    return
                pr_current_xp = int(pr_current_xp)
                pr_needed_xp = int(pr_needed_xp)
                xp = pr_needed_xp - pr_current_xp
                pickaxes = ceil(xp / 100)
                pickaxes_wb = ceil(xp / 110)
                xp_rest = 100 - (xp % 100)
                xp_rest_wb = 110 - (xp % 110)
                if xp_rest == 100:
                    xp_rest = 0
                if xp_rest_wb == 110:
                    xp_rest_wb = 0
                pickaxes_total = pickaxes
                pickaxes_total_wb = pickaxes_wb

                for current_level in range(pr_level + 2, 101):
                    worker_level_xp = profession_data.xp[current_level]
                    actual_xp = worker_level_xp - xp_rest
                    actual_xp_wb = worker_level_xp - xp_rest_wb
                    pickaxes = ceil(actual_xp / 100)
                    pickaxes_wb = ceil(actual_xp_wb / 110)
                    pickaxes_total = pickaxes_total + pickaxes
                    pickaxes_total_wb = pickaxes_total_wb + pickaxes_wb
                    xp_rest = 100 - (actual_xp % 100)
                    xp_rest_wb = 110 - (actual_xp_wb % 110)
                    if xp_rest == 100:
                        xp_rest = 0
                    if xp_rest_wb == 110:
                        xp_rest_wb = 0

                await ctx.send(
                    f'You need to cook the following amount of {emojis.FOOD_BANANA_PICKAXE} banana pickaxes '
                    f'to reach level **100**:\n'
                    f'{emojis.BP} **{pickaxes_total:,}** without world buff\n'
                    f'{emojis.BP} **{pickaxes_total_wb:,}** with world buff\n\n'
                    f'Use `{ctx.prefix}craft [amount] pickaxes` to see how much you need for that.'
                )
            except asyncio.TimeoutError as error:
                await ctx.send(f'**{ctx.author.name}**, couldn\'t find your profession information, RIP.')
                return

        elif len(args) == 1:
            arg = args[0]

            if arg.replace('-','').isnumeric():
                try:
                    level = int(arg)
                except:
                    await ctx.send(
                        f'`{arg}` is not a valid target level. Please enter the level you want me to calculate to.\n'
                        f'Example: `{ctx.prefix}prwtotal 80`. If you want me to calculate to level 100, you can omit the level.'
                    )
                    return

                if not 2 <= level <= 200:
                    await ctx.send('You want to reach level what now?')
                    return

                try:
                    await ctx.send(f'**{ctx.author.name}**, please type `rpg pr worker` (or `abort` to abort)')
                    answer_user_worker = await self.bot.wait_for('message', check=check, timeout = 30)
                    answer = answer_user_worker.content
                    answer = answer.lower()
                    if answer in ('rpg pr worker','rpg profession worker', 'rpg professions worker'):
                        answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                        try:
                            pr_worker = str(answer_bot_at.embeds[0].fields[0])
                        except:
                            await ctx.send('Whelp, something went wrong here, sorry.')
                            return
                        start_level = pr_worker.find('**Level**') + 11
                        end_level = pr_worker.find('(', start_level) - 1
                        if end_level == -2:
                            end_level = pr_worker.find('\\n', start_level)
                        pr_level = pr_worker[start_level:end_level]
                        start_current_xp = pr_worker.find('**XP**') + 8
                        end_current_xp = pr_worker.find('/', start_current_xp)
                        pr_current_xp = pr_worker[start_current_xp:end_current_xp]
                        pr_current_xp = pr_current_xp.replace(',','')
                        start_needed_xp = pr_worker.find('/', start_current_xp) + 1
                        end_needed_xp = pr_worker.find(f'\'', start_needed_xp)
                        pr_needed_xp = pr_worker[start_needed_xp:end_needed_xp]
                        pr_needed_xp = pr_needed_xp.replace(',','')
                    elif (answer_user_worker.content == 'abort') or (answer_user_worker.content == 'cancel'):
                        await ctx.send('Aborting.')
                        return
                    else:
                        await ctx.send('Wrong input. Aborting.')
                        return

                    if not pr_level.isnumeric() or not pr_current_xp.isnumeric() or not pr_needed_xp.isnumeric():
                        await ctx.send('Whelp, something went wrong here, sorry.')
                        return
                    pr_level = int(pr_level)
                    profession_data: database.Profession = await database.get_profession('worker')
                    next_level = pr_level + 1
                    if profession_data.xp[next_level] is None: await profession_data.update_level(next_level, pr_needed_xp)
                    pr_current_xp = int(pr_current_xp)
                    pr_needed_xp = int(pr_needed_xp)
                    xp = pr_needed_xp - pr_current_xp
                    pickaxes = ceil(xp / 100)
                    pickaxes_wb = ceil(xp / 110)
                    xp_rest = 100 - (xp % 100)
                    xp_rest_wb = 110 - (xp % 110)
                    if xp_rest == 100:
                        xp_rest = 0
                    if xp_rest_wb == 110:
                        xp_rest_wb = 0
                    pickaxes_total = pickaxes
                    pickaxes_total_wb = pickaxes_wb

                    if pr_level >= level:
                        await ctx.send(
                            f'So.\nYou are level {pr_level} and you want to get to level {level}.\n{emojis.WAIT_WHAT}'
                        )
                        return

                    for current_level in range(pr_level + 2, level + 1):
                        if profession_data.xp[current_level] is None:
                            await ctx.send(
                                f'Sorry, I don\'t have enough data yet to calculate the total for up to '
                                f'level {level}. I currently have data up to level **{current_level - 1}**.\n'
                                f'You can use `{ctx.prefix}prw` to calculate the pickaxes needed to reach the '
                                f'next level(s) though.'
                            )
                            return
                        worker_level_xp = profession_data.xp[current_level]
                        actual_xp = worker_level_xp - xp_rest
                        actual_xp_wb = worker_level_xp - xp_rest_wb
                        pickaxes = ceil(actual_xp / 100)
                        pickaxes_wb = ceil(actual_xp_wb / 110)
                        pickaxes_total = pickaxes_total + pickaxes
                        pickaxes_total_wb = pickaxes_total_wb + pickaxes_wb
                        xp_rest = 100 - (actual_xp % 100)
                        xp_rest_wb = 110 - (actual_xp_wb % 110)
                        if xp_rest == 100:
                            xp_rest = 0
                        if xp_rest_wb == 110:
                            xp_rest_wb = 0

                    await ctx.send(
                        f'You need to cook the following amount of {emojis.FOOD_BANANA_PICKAXE} banana pickaxes '
                        f'to reach level **{level}**:\n'
                        f'{emojis.BP} **{pickaxes_total:,}** without world buff\n'
                        f'{emojis.BP} **{pickaxes_total_wb:,}** with world buff\n\n'
                        f'Use `{ctx.prefix}craft [amount] pickaxes` to see how much you need for that.'
                    )
                except asyncio.TimeoutError as error:
                    await ctx.send(f'**{ctx.author.name}**, couldn\'t find your profession information, RIP.')
                    return
            else:
                await ctx.send('Sir, that is not a valid number.')
                return
        else:
            await ctx.send(
                f'The command syntax is `{ctx.prefix}prwtotal [level]`.\n'
                f'If you omit the level, I will calculate the banana pickaxes you need to reach level 100.'
            )
            return


# Initialization
def setup(bot):
    bot.add_cog(ProfessionsOldCog(bot))



# --- Redundancies ---
# Guides
guide_overview = '`{prefix}pr` : Professions overview'
guide_ascension = '`{prefix}pr ascension` : Details about ascension'
guide_crafter = '`{prefix}pr crafter` : Details about crafter'
guide_enchanter = '`{prefix}pr enchanter` : Details about enchanter'
guide_level = '`{prefix}pr level` : How and when to level up your professions'
guide_lootboxer = '`{prefix}pr lootboxer` : Details about lootboxer'
guide_merchant = '`{prefix}pr merchant` : Details about merchant'
guide_worker = '`{prefix}pr worker` : Details about worker'

# Calculators
calc_pre = '`{prefix}pre` : Ice cream you need to cook for your next enchanter levels'
calc_prl = '`{prefix}prl` : Lootboxes you need to cook for your next lootboxer levels'
calc_prm = '`{prefix}prm` : Logs you need to sell for your next merchant levels'
calc_prw = '`{prefix}prw` : Pickaxes you need to cook for your next worker levels'
calc_pretotal = '`{prefix}pretotal [level]` : Total ice cream you need to reach `[level]`'
calc_prltotal = '`{prefix}prltotal [level]` : Total lootboxes you need to reach `[level]`'
calc_prmtotal = '`{prefix}prmtotal [level]` : Total logs you need to reach `[level]`'
calc_prwtotal = '`{prefix}prwtotal [level]` : Total pickaxes you need to reach `[level]`'



# --- Embeds ---
# Professions overview
async def embed_professions_overview(prefix):

    worker = (
        f'{emojis.BP} Increases the chance to get better items with work commands\n'
        f'{emojis.BP} Level 101+: Adds a chance to find other items with work commands\n'
        f'{emojis.BP} For more details see `{prefix}pr worker`'
    )

    crafter = (
        f'{emojis.BP} Increases the chance to get 10% materials back when crafting\n'
        f'{emojis.BP} Level 101+: Increases the percentage of items returned\n'
        f'{emojis.BP} For more details see `{prefix}pr crafter`'
    )

    lootboxer = (
        f'{emojis.BP} Increases the bank XP bonus\n'
        f'{emojis.BP} Decreases the cost of horse training\n'
        f'{emojis.BP} Level 101+: Increases the maximum level of your horse\n'
        f'{emojis.BP} For more details see `{prefix}pr lootboxer`'
    )

    merchant = (
        f'{emojis.BP} Increases the amount of coins you get when selling items\n'
        f'{emojis.BP} Level 101+: You get {emojis.DRAGON_SCALE} dragon scales when selling mob drops\n'
        f'{emojis.BP} For more details see `{prefix}pr merchant`'
    )

    enchanter = (
        f'{emojis.BP} Increases the chance to get a better enchant when enchanting\n'\
        f'{emojis.BP} Level 101+: Adds a chance to win the price of the enchant instead of spending it\n'
        f'{emojis.BP} For more details see `{prefix}pr enchanter`'
    )

    guides = (
        f'{emojis.BP} {guide_ascension.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_crafter.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_enchanter.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_level.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_lootboxer.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_merchant.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_worker.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'PROFESSIONS',
        description = (
            f'There are 5 professions you can increase to get increasing bonuses.\n'
            f'Each profession has a bonus that caps at level 100. You can level further but it will take much longer and the bonuses for levels 101+ are different.\n'
            f'If you get all professions to level 100, you can ascend (see `{prefix}pr ascension`).'
        )
    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name=f'WORKER {emojis.PR_WORKER}', value=worker, inline=False)
    embed.add_field(name=f'CRAFTER {emojis.PR_CRAFTER}', value=crafter, inline=False)
    embed.add_field(name=f'LOOTBOXER {emojis.PR_LOOTBOXER}', value=lootboxer, inline=False)
    embed.add_field(name=f'MERCHANT {emojis.PR_MERCHANT}', value=merchant, inline=False)
    embed.add_field(name=f'ENCHANTER {emojis.PR_ENCHANTER}', value=enchanter, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Professions leveling guide
async def embed_professions_leveling(prefix):

    crafter = (
        f'{emojis.BP} This is the first profession you should level up\n'
        f'{emojis.BP} Level **before time traveling** with leftover materials\n'
        f'{emojis.BP} Trade everything to {emojis.LOG} logs and craft/dismantle {emojis.LOG_EPIC} EPIC logs\n'
        f'{emojis.BP} Craft in batches of 500 or 1000 (you can dismantle all at once)\n'
        f'{emojis.BP} Once you reach level 100, switch to leveling merchant'
    )

    merchant = (
        f'{emojis.BP} This is the second profession you should level up\n'
        f'{emojis.BP} Level **before time traveling** with leftover materials\n'
        f'{emojis.BP} Trade everything except {emojis.LOG_ULTRA} ULTRA logs to {emojis.LOG} logs\n'
        f'{emojis.BP} Sell {emojis.LOG_ULTRA} ULTRA logs\n'
        f'{emojis.BP} For each remaining level look up `rpg pr merchant` and calculate the XP you need for the next level\n'
        f'{emojis.BP} Take 5x the XP amount and sell as many {emojis.LOG} logs\n'
        f'{emojis.BP} Tip: You can quickly calculate logs to sell with `{prefix}prm`\n'
        f'{emojis.BP} Once you reach level 100, focus on lootboxer and worker'
    )

    lootboxer = (
        f'{emojis.BP} Level up by opening lootboxes\n'
        f'{emojis.BP} Better lootboxes give more XP (see `{prefix}pr lootboxer`)\n'
        f'{emojis.BP} If lower than worker, consider cooking {emojis.FOOD_FILLED_LOOTBOX} filled lootboxes\n'
        f'{emojis.BP} It\'s usually not necessary to cook {emojis.FOOD_FILLED_LOOTBOX} filled lootboxes\n'
        f'{emojis.BP} Use `hunt hardmode` whenever you have access (unlocks in A13)'
    )

    worker = (
        f'{emojis.BP} Level up by using work commands or cooking {emojis.FOOD_BANANA_PICKAXE} banana pickaxes\n'
        f'{emojis.BP} Higher tier work commands give more XP (see `{prefix}pr worker`)\n'
        f'{emojis.BP} Try to keep the level at about the same as lootboxer\n'
        f'{emojis.BP} If lower than lootboxer, consider cooking {emojis.FOOD_BANANA_PICKAXE} banana pickaxes\n'
        f'{emojis.BP} Tip: You can quickly calculate the pickaxes you need with `{prefix}prw`'
    )

    enchanter = (
        f'{emojis.BP} This is the last profession you should level up (it\'s expensive and you need access to at least `transmute`)\n'
        f'{emojis.BP} Level before time traveling using `transmute` or `transcend`\n'
        f'{emojis.BP} XP gain is based on the quality of the enchant you get (see `{prefix}pr enchanter`)\n'
        f'{emojis.BP} Costs around 3 billion coins without {emojis.HORSE_T8} T8+ horse\n'
        f'{emojis.BP} Costs around 2 billion coins with {emojis.HORSE_T8} T8+ horse'
    )

    ascended = (
        f'{emojis.BP} Increase crafter and merchant to 101, then focus exclusively on worker\n'
    )

    calculators = (
        f'{emojis.BP} {calc_pre.format(prefix=prefix)}\n'
        f'{emojis.BP} {calc_prl.format(prefix=prefix)}\n'
        f'{emojis.BP} {calc_prm.format(prefix=prefix)}\n'
        f'{emojis.BP} {calc_prw.format(prefix=prefix)}\n'
        f'{emojis.BP} {calc_pretotal.format(prefix=prefix)}\n'
        f'{emojis.BP} {calc_prltotal.format(prefix=prefix)}\n'
        f'{emojis.BP} {calc_prmtotal.format(prefix=prefix)}\n'
        f'{emojis.BP} {calc_prwtotal.format(prefix=prefix)}'
    )

    guides = (
        f'{emojis.BP} {guide_overview.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_ascension.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_crafter.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_enchanter.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_level.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_lootboxer.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_merchant.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_worker.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'LEVELING UP PROFESSIONS',
        description = (
            f'This guide shows you how to level up professions to reach ascension (level 100).\n'
            f'Do not overfarm to get ascended as early as possible. It wastes a lot of time you could spend time traveling. TT give high bonuses and ascension makes more sense if you already have access to all commands up to area 15.\n'
            f'Thus, unless you can reach ascension easily, always time travel again instead of staying and farming.'
        )
    )
    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name=f'1. CRAFTER {emojis.PR_CRAFTER}', value=crafter, inline=False)
    embed.add_field(name=f'2. MERCHANT {emojis.PR_MERCHANT}', value=merchant, inline=False)
    embed.add_field(name=f'3. WORKER {emojis.PR_WORKER}', value=worker, inline=False)
    embed.add_field(name=f'4. LOOTBOXER {emojis.PR_LOOTBOXER}', value=lootboxer, inline=False)
    embed.add_field(name=f'5. ENCHANTER {emojis.PR_ENCHANTER}', value=enchanter, inline=False)
    embed.add_field(name='AFTER ASCENSION', value=ascended, inline=False)
    embed.add_field(name='CALCULATORS', value=calculators, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Crafter guide
async def embed_professions_crafter(prefix):

    base_bonus = (
        f'{emojis.BP} Increases the chance to get 10% materials back when crafting\n'
        f'{emojis.BP} The chance at level 100 is 80%'
    )

    level_101 =(
        f'{emojis.BP} Increases the percentage of items returned\n'
        f'{emojis.BP} The percentage increases logarithmically'
    )

    how_to_get_xp = (
        f'{emojis.BP} Craft and dismantle\n'
        f'{emojis.BP} ~~Cook {emojis.FOOD_HEAVY_APPLE} heavy apples (100 XP each)~~ (don\'t do that)'
    )

    xp_gain = (
        f'{emojis.BP} A detailed list of all material and gear XP is available in the [Wiki](https://epic-rpg.fandom.com/wiki/Professions#Crafter)'
    )

    guides = (
        f'{emojis.BP} {guide_overview.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_level.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'CRAFTER PROFESSION'
    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='PROFESSION BONUS', value=base_bonus, inline=False)
    embed.add_field(name='ADDITIONAL BONUS LEVEL 101+', value=level_101, inline=False)
    embed.add_field(name='HOW TO GET XP', value=how_to_get_xp, inline=False)
    embed.add_field(name='XP GAIN', value=xp_gain, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Enchanter guide
async def embed_professions_enchanter(prefix):

    base_bonus = (
        f'{emojis.BP} Increases the chance to get a better enchant when enchanting\n'
        f'{emojis.BP} The exact chance increase is unknown'
    )

    level_101 =(
        f'{emojis.BP} Adds a chance to win the price of the enchant instead of spending it\n'
        f'{emojis.BP} The chance is 2% at level 101 and increases logarithmically with each level'
    )

    how_to_get_xp = (
        f'{emojis.BP} Use enchanting commands\n'
        f'{emojis.BLANK} The XP formula is [tt multiplier] * [command multiplier] * [enchantment xp]\n'
        f'{emojis.BLANK} Ex: If you enchant **Perfect** with `transmute` in TT6, you get `2 * 100 * 7` XP\n'
        f'{emojis.BP} ~~Cook {emojis.FOOD_FRUIT_ICE_CREAM} fruit ice cream (100 XP each)~~ (don\'t do that)'
    )

    xp_gain = (
        f'{emojis.BP} **Normie**: 0 XP\n'
        f'{emojis.BP} **Good**: 1 XP\n'
        f'{emojis.BP} **Great**: 2 XP\n'
        f'{emojis.BP} **Mega**: 3 XP\n'
        f'{emojis.BP} **Epic**: 4 XP\n'
        f'{emojis.BP} **Hyper**: 5 XP\n'
        f'{emojis.BP} **Ultimate**: 6 XP\n'
        f'{emojis.BP} **Perfect**: 7 XP\n'
        f'{emojis.BP} **EDGY**: 8 XP\n'
        f'{emojis.BP} **ULTRA-EDGY**: 9 XP\n'
        f'{emojis.BP} **OMEGA**: 10 XP\n'
        f'{emojis.BP} **ULTRA-OMEGA**: 11 XP\n'
        f'{emojis.BP} **GODLY**: 12 XP\n'
        f'{emojis.BP} **VOID**: 13 XP\n'
    )

    command_multipliers = (
        f'{emojis.BP} `enchant`: 1\n'
        f'{emojis.BP} `refine`: 10\n'
        f'{emojis.BP} `transmute`: 100\n'
        f'{emojis.BP} `transcend`: 1,000'
    )

    tt_multiplier = (
        f'{emojis.BP} Use `rpg time travel` to check your TT multiplier'
    )

    calculators = (
        f'{emojis.BP} {calc_pre.format(prefix=prefix)}\n'
        f'{emojis.BP} {calc_pretotal.format(prefix=prefix)}'
    )

    guides = (
        f'{emojis.BP} {guide_overview.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_level.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'ENCHANTER PROFESSION'
    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='PROFESSION BONUS', value=base_bonus, inline=False)
    embed.add_field(name='ADDITIONAL BONUS LEVEL 101+', value=level_101, inline=False)
    embed.add_field(name='HOW TO GET XP', value=how_to_get_xp, inline=False)
    embed.add_field(name='XP GAIN', value=xp_gain, inline=False)
    embed.add_field(name='COMMAND MULTIPLIERS', value=command_multipliers, inline=False)
    embed.add_field(name='TT MULTIPLIER', value=tt_multiplier, inline=False)
    embed.add_field(name='CALCULATORS', value=calculators, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Lootboxer guide
async def embed_professions_lootboxer(prefix):

    base_bonus = (
        f'{emojis.BP} Increases the bank XP bonus\n'
        f'{emojis.BP} Decreases the cost of horse training\n'
        f'{emojis.BP} Horse training is 50 % cheaper at level 100\n'\
        f'{emojis.BP} The exact buff of the bank bonus unknown'
    )

    level_101 =(
        f'{emojis.BP} Increases the maximum level of your horse\n'
        f'{emojis.BP} The level increases by 1 per level after 100'
    )

    how_to_get_xp = (
        f'{emojis.BP} Open lootboxes\n'
        f'{emojis.BP} ~~Cook {emojis.FOOD_FILLED_LOOTBOX} filled lootboxes (100 XP each)~~ (don\'t do that)\n'
    )

    xp_gain = (
        f'{emojis.BP} {emojis.LB_COMMON} common lootbox: 4 XP\n'
        f'{emojis.BP} {emojis.LB_UNCOMMON} uncommon lootbox: 9 XP\n'
        f'{emojis.BP} {emojis.LB_RARE} rare lootbox: 17 XP\n'
        f'{emojis.BP} {emojis.LB_EPIC} EPIC lootbox: 30 XP\n'
        f'{emojis.BP} {emojis.LB_EDGY} EDGY lootbox: 65 XP\n'
        f'{emojis.BP} {emojis.LB_OMEGA} OMEGA lootbox: 800 XP\n'
        f'{emojis.BP} {emojis.LB_GODLY} GODLY lootbox: 15,000 XP\n'
        f'{emojis.BP} {emojis.LB_VOID} VOID lootbox: -1000 XP\n'
    )

    calculators = (
        f'{emojis.BP} {calc_prl.format(prefix=prefix)}\n'
        f'{emojis.BP} {calc_prltotal.format(prefix=prefix)}'
    )

    guides = (
        f'{emojis.BP} {guide_overview.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_level.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'LOOTBOXER PROFESSION'
    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='PROFESSION BONUS', value=base_bonus, inline=False)
    embed.add_field(name='ADDITIONAL BONUS LEVEL 101+', value=level_101, inline=False)
    embed.add_field(name='HOW TO GET XP', value=how_to_get_xp, inline=False)
    embed.add_field(name='XP GAIN', value=xp_gain, inline=False)
    embed.add_field(name='CALCULATORS', value=calculators, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Merchant guide
async def embed_professions_merchant(prefix):

    base_bonus = (
        f'{emojis.BP} Increases the amount of coins you get when selling items\n'
        f'{emojis.BP} You get 4.929395x more coins at level 100'
    )

    level_101 =(
        f'{emojis.BP} You get {emojis.DRAGON_SCALE} dragon scales when selling mob drops\n'
        f'{emojis.BP} You get 1 dragon scale per 50 mob drops at level 101 (2%)\n'
        f'{emojis.BP} This increases by 2% for every level\n'
    )

    how_to_get_xp = (
        f'{emojis.BP} Sell materials\n'
        f'{emojis.BP} Note that you don\'t get any XP when selling gear and other items\n'
        f'{emojis.BP} ~~Cook {emojis.FOOD_COIN_SANDWICH} coin sandwich (100 XP each)~~ (**DON\'T DO THAT**)\n'
    )

    xp_gain = (
        f'{emojis.BP} A detailed list of XP per amount sold is available in the [Wiki](https://epic-rpg.fandom.com/wiki/Professions#Merchant)'
    )

    calculators = (
        f'{emojis.BP} {calc_prm.format(prefix=prefix)}\n'
        f'{emojis.BP} {calc_prmtotal.format(prefix=prefix)}'
    )

    guides = (
        f'{emojis.BP} {guide_overview.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_level.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'MERCHANT PROFESSION'
    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='PROFESSION BONUS', value=base_bonus, inline=False)
    embed.add_field(name='ADDITIONAL BONUS LEVEL 101+', value=level_101, inline=False)
    embed.add_field(name='HOW TO GET XP', value=how_to_get_xp, inline=False)
    embed.add_field(name='XP GAIN', value=xp_gain, inline=False)
    embed.add_field(name='CALCULATORS', value=calculators, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Worker guide
async def embed_professions_worker(prefix):

    base_bonus = (
        f'{emojis.BP} Increases the chance to get a better item with work commands\n'
        f'{emojis.BP} The chance increase is 50% at level 100'
    )

    level_101 =(
        f'{emojis.BP} Adds an increasing chance to find other items with top tier work commands\n'
        f'{emojis.BP} The chance is 4% at level 101 and increases by 4% for every level\n'
        f'{emojis.BP} `bigboat` gets a chance to drop {emojis.BANANA} bananas\n'
        f'{emojis.BP} `chainsaw` gets a chance to drop {emojis.FISH} normie fish\n'
        f'{emojis.BP} `dynamite` gets a chance to drop {emojis.LOG_SUPER} SUPER logs\n'
        f'{emojis.BP} `greenhouse` gets a chance to drop {emojis.RUBY} rubies'
    )

    how_to_get_xp = (
        f'{emojis.BP} Use work commands\n'
        f'{emojis.BP} Cook {emojis.FOOD_BANANA_PICKAXE} banana pickaxes (100 XP each)\n'
    )

    xp_gain = (
        f'{emojis.BP} `chop` / `fish` / `pickup` / `mine`: 4 XP\n'
        f'{emojis.BP} `axe` / `ladder` / `pickaxe`: 8 XP\n'
        f'{emojis.BP} `net`: 9 XP\n'
        f'{emojis.BP} `bowsaw` / `tractor` / `drill`: 12 XP\n'
        f'{emojis.BP} `boat`: 13 XP\n'
        f'{emojis.BP} `chainsaw`: 16 XP\n'
        f'{emojis.BP} `greenhouse` / `dynamite`: 17 XP\n'
        f'{emojis.BP} `bigboat`: 18 XP'
    )

    calculators = (
        f'{emojis.BP} {calc_prw.format(prefix=prefix)}\n'
        f'{emojis.BP} {calc_prwtotal.format(prefix=prefix)}'
    )

    guides = (
        f'{emojis.BP} {guide_overview.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_level.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'WORKER PROFESSION'
    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='PROFESSION BONUS', value=base_bonus, inline=False)
    embed.add_field(name='ADDITIONAL BONUS LEVEL 101+', value=level_101, inline=False)
    embed.add_field(name='HOW TO GET XP', value=how_to_get_xp, inline=False)
    embed.add_field(name='XP GAIN', value=xp_gain, inline=False)
    embed.add_field(name='CALCULATORS', value=calculators, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed

# Ascension
async def embed_ascension(prefix):

    requirements = (
        f'{emojis.BP} All 5 professions at level 100+ (see `{prefix}pr level`)\n'
        f'{emojis.BP} {emojis.TIME_TRAVEL} TT 1+'
    )

    benefits =(
        f'{emojis.BP} Get more materials by using high tier work commands early\n'
        f'{emojis.BP} Get more XP by using `hunt hardmode` and `adventure hardmode` early\n'
        f'{emojis.BP} Get higher enchants easier by using `transcend` and `transmute` early\n'
        f'{emojis.BP} {emojis.RUBY} rubies and {emojis.BANANA} bananas are obtainable in area 1+'
    )

    notes = (
        f'{emojis.BP} Trade rates are still area locked\n'
        f'{emojis.BP} Higher tier logs and fish remain area locked. Use `rpg h [material]` to see the area they unlock in.'
    )

    guides = (
        f'{emojis.BP} {guide_overview.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_level.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'ASCENSION',
        description = (
            f'Ascension allows you to use **all** game commands you ever unlocked in **every** area.\n'
            f'This makes it much easier to get XP, materials and high enchants early.'
        )
    )

    embed.set_footer(text=await functions.default_footer(prefix))
    embed.add_field(name='REQUIREMENTS', value=requirements, inline=False)
    embed.add_field(name='BENEFITS', value=benefits, inline=False)
    embed.add_field(name='NOTES', value=notes, inline=False)
    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed