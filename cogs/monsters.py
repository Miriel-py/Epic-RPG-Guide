# monsters.py

import asyncio

import discord
from discord.ext import commands
# from discord_components import Button, ButtonStyle, InteractionType

import database
import emojis
import global_data


# monsters commands (cog)
class monstersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Mobs list
    @commands.command(aliases=('monster','monsters','mob','monsterlist','monsterslist','moblist','mobslist',))
    @commands.bot_has_permissions(send_messages=True, embed_links=True, external_emojis=True)
    async def mobs(self, ctx, *args):

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        prefix = ctx.prefix
        error_area = f'This is not a valid area. The syntax is `{prefix}mobs [area]`. The area has to be between 1 and 20.'
        info_area_16 = (
            f'Area 16 (aka The TOP) does not have its own monsters.\n'
            f'Instead the EPIC NPC poses as a random monster which can be any monster from areas 1~20.'
        )
        error_syntax = ( #Temporary solution because buttons use a shit ton of cpu for some reason
            f'This command shows all mobs in an area.\n'
            f'The syntax is `{prefix}mobs [area]`. The area has to be between 1 and 20.'
        )

        if args:
            area = args[0].lower().replace('a','')
            if area.isnumeric():
                try:
                    area = int(area)
                except:
                    await ctx.send(error_area)
                    return
                if not 1 <= area <= 20:
                    await ctx.send(error_area)
                    return
            else:
                if 'top' in area:
                    await ctx.send(info_area_16)
                    return
                else:
                    await ctx.send(error_area)
                    return
        else:
            await ctx.send(error_syntax)
            return
            # area = 1

        mobs_data = await database.get_mob_data(ctx, (1,20))
        embed = await embed_mobs(prefix, mobs_data, area)
        await ctx.send(embed=embed)

    # Daily mob lookup
    @commands.command(aliases=('mobdaily','daily',))
    @commands.bot_has_permissions(external_emojis=True, send_messages=True)
    async def dailymob(self, ctx, *args):

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        def epic_rpg_check(m):
            correct_embed = False
            try:
                if (str(m.embeds[0].fields).find('Daily monster') > 1):
                    correct_embed = True
                else:
                    correct_embed = False
            except:
                correct_embed = False

            return m.author.id == 555955826880413696 and m.channel == ctx.channel and correct_embed

        try:
            await ctx.send(f'**{ctx.author.name}**, please type `rpg world` (or `abort` to abort)')
            answer_message = await self.bot.wait_for('message', check=check, timeout = 30)
            answer = answer_message.content
            answer = answer.lower()
            if answer == 'rpg world':
                answer_bot_at = await self.bot.wait_for('message', check=epic_rpg_check, timeout = 5)
                try:
                    embed_world = str(answer_bot_at.embeds[0].fields)
                except:
                    await ctx.send('Whelp, something went wrong here, sorry.')
                    return
                end_daily = embed_world.find('**\\nThis monster')
                start_daily = embed_world.rfind('**',0,end_daily) + 2
                daily_mob = embed_world[start_daily:end_daily]
            elif answer in ('abort','cancel'):
                await ctx.send('Aborting.')
                return
            else:
                await ctx.send(f'Wrong input. Aborting.')
                return

            mob = await database.get_mob_by_name(ctx, daily_mob)

            if mob:
                mob_name = mob[0]
                mob_emoji = getattr(emojis, mob[1])
                mob_area_from = mob[2]
                mob_area_until = mob[3]
                mob_activity = mob[4]

                if mob_area_from == mob_area_until:
                    await ctx.send(f'{mob_emoji} **{mob_name}** can be found in **area {mob_area_from}** by using `rpg {mob_activity}`.')
                else:
                    await ctx.send(f'{mob_emoji} **{mob_name}** can be found in **areas {mob_area_from}-{mob_area_until}** by using `rpg {mob_activity}`.')
            else:
                await ctx.send(f'Couldn\'t find the mob **{daily_mob}**, sorry.')
                global_data.logger.info(f'Daily mob detection: Could not find daily mob "{daily_mob}" in the database.')
        except asyncio.TimeoutError as error:
            await ctx.send(f'**{ctx.author.name}**, couldn\'t find the daily monster, RIP.')
            return

# Initialization
def setup(bot):
    bot.add_cog(monstersCog(bot))



# --- Redundancies ---
# Guides
guide_mobs_all = '`{prefix}mobs` : List of all monsters'
guide_mobs_area = '`{prefix}mobs [area]` : List of monsters in area [area]'
guide_mob_daily = '`{prefix}dailymob` : Where to find the daily monster'



# --- Embeds ---
# Mobs list
async def embed_mobs(prefix, mobs_data, area):

    guides = (
        #f'{emojis.BP} {guide_mobs_all.format(prefix=prefix)}\n'
        #f'{emojis.BP} {guide_mobs_area.format(prefix=prefix)}\n'
        f'{emojis.BP} {guide_mob_daily.format(prefix=prefix)}'
    )

    embed = discord.Embed(
        color = global_data.EMBED_COLOR,
        title = f'MONSTERS IN AREA {area}'
    )

    embed.set_footer(text=await global_data.default_footer(prefix))

    mobs_hunt = ''
    mobs_adventure = ''

    for mob in mobs_data:
        mob_area_from = mob[2]
        mob_area_until = mob[3]

        if mob_area_from <= area <= mob_area_until:
            mob_name = mob[0]
            mob_emoji = getattr(emojis, mob[1])
            mob_activity = mob[4]
            if mob[5]:
                mob_drop_emoji = getattr(emojis, mob[5])
            else:
                mob_drop_emoji = None
            if mob_activity == 'hunt':
                mobs_hunt = f'{mobs_hunt}\n{emojis.BP} {mob_emoji} **{mob_name}**'
                if mob_drop_emoji:
                    mobs_hunt = f'{mobs_hunt} (drops {mob_drop_emoji})'
            if mob_activity == 'adventure':
                mobs_adventure = f'{mobs_adventure}\n{emojis.BP} {mob_emoji} **{mob_name}**'

    if not mobs_hunt == '':
        embed.add_field(name='HUNT', value=mobs_hunt, inline=False)
    if not mobs_adventure == '':
        embed.add_field(name='ADVENTURE', value=mobs_adventure, inline=False)

    embed.add_field(name='ADDITIONAL GUIDES', value=guides, inline=False)

    return embed