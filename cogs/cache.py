# cache.py
"""Collects messages containing certain rpg and mention commands for the local cache"""

import re

import discord
from discord.ext import commands

from cache import messages
from resources import settings, strings


class CacheCog(commands.Cog):
    """Cog that contains the cache commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """Runs when a message is sent in a channel."""
        if message.author.bot: return
        if message.embeds or message.content is None: return
        inventory_match = re.search(strings.REGEX_COMMAND_QUICK_TRADE, message.content.lower())
        if not inventory_match: return
        correct_mention = False
        if message.content.lower().startswith('rpg '):
            await messages.store_message(message)
            return
        if message.mentions:
            for mentioned_user in message.mentions:
                if mentioned_user.id == settings.EPIC_RPG_ID:
                    correct_mention = True
                    break
            if correct_mention:
                await messages.store_message(message)

# Initialization
def setup(bot):
    bot.add_cog(CacheCog(bot))