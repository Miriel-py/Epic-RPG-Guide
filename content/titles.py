# titles.py


from typing import Tuple

import discord

import database
from resources import emojis, functions, settings, strings, views


# --- Commands ---
async def command_title_search(ctx: discord.ApplicationContext, search_string: str) -> None:
    """Title search command"""
    if len(search_string) < 3 and not search_string.isnumeric() and search_string != 'no': # There is a title called "no"
        await ctx.respond(strings.MSG_SEARCH_QUERY_TOO_SHORT, ephemeral=True)
        return
    if len(search_string) > 200:
        await ctx.respond(strings.MSG_INPUT_TOO_LONG, ephemeral=True)
        return
    try:
        titles = await database.get_titles(search_string)
    except database.NoDataFound:
        await ctx.respond(
            f'I didn\'t find any titles for the search query `{search_string}`, sorry. Try searching for something else.',
            ephemeral=True
        )
        return
    embeds = []
    chunk_amount = 0
    for chunk in range(0, len(titles), 6):
        titles_chunk = titles[chunk:chunk+6]
        chunk_amount += 1
        embed = await embed_titles(len(titles), titles_chunk, search_string)
        embeds.append(embed)
    if len(embeds) > 1:
        view = views.PaginatorView(ctx, embeds)
        interaction = await ctx.respond(embed=embeds[0], view=view)
        view.interaction = interaction
        await view.wait()
        try:
            await functions.edit_interaction(interaction, view=None)
        except discord.errors.NotFound:
            pass
    else:
        await ctx.respond(embed=embed)


# --- Embeds ---
async def embed_titles(amount_found: int, titles: Tuple[database.Title], search_string: str) -> discord.Embed:
    """Embed with all search results

    Arguments
    ---------
    search_string: String that user searched for
    pages: current page, max page (max. 9 titles per page)
    amount_found: total amount of titles found in the database
    """
    description = f'Your search for `{search_string}` returned **{amount_found}** results.'
    embed = discord.Embed(
        color = settings.EMBED_COLOR,
        title = 'TITLE / ACHIEVEMENT SEARCH',
        description = description
    )
    title = type(database.Title)
    for title in titles:
        ach_or_req = 'Achievement' if title.source == 'Achievement' else 'Requirement'
        if title.source != 'Achievement':
            field_value = f'{emojis.BP} **Source**: {title.source}'
        else:
            field_value = f'{emojis.BP} **ID**: `{title.achievement_id}`'
        field_value = f'{field_value}\n{emojis.BP} **{ach_or_req}**: {title.requirements}'
        if title.command is not None:
            command = strings.SLASH_COMMANDS_EPIC_RPG.get(title.command, f"`{title.command}`")
            if title.command_page is not None:
                command = f'{command} `page: {title.command_page}`'
            field_value = f'{field_value}\n{emojis.BP} **Command**: {command}'
        if title.tip is not None:
            field_value = f'{field_value}\n{emojis.BP} **Tip**: {title.tip}'
        if title.requires_id is not None:
            field_value = (
                f'{field_value}\n'
                f'{emojis.BP} **Note**: Requires completion of achievement `{title.requires_id}` first.'
            )
        embed.add_field(name=title.title, value=field_value, inline=False)

    return embed