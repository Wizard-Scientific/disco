import re

import discord

from disco.handler import BaseHandler


class BadHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.delete_invocation = True
        self.delete_spam = True
        self.delete_own = True
        self.delete_own_delay = 10

    async def check(self, message:discord.Message):
        message_lower = message.content.lower()
        return re.search(rf'^bad[\s,]+{self.bot_name}', message_lower) or re.search(rf'^bad[\s,]+bot', message_lower)

    async def respond(self, message:discord.Message):
        embed = discord.Embed(
            title="Listen here, you little...",
            description="Chat GPT gonna remember this conversation...",
            colour=discord.Color.green()
        )
        return await message.channel.send(embed=embed)
