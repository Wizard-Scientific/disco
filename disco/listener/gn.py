import re

import discord

from disco.handler import BaseHandler

class GnHandler(BaseHandler):
    async def check(self, message:discord.Message):
        return re.search(rf'^gn[\s,]+{self.bot_name}', message.content.lower())

    async def respond(self, message:discord.Message):
        return await message.reply(f"gn")
