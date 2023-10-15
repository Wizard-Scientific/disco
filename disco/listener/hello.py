import re

import discord

from disco.handler import BaseHandler

class HelloHandler(BaseHandler):
    async def check(self, message:discord.Message):
        message_lower = message.content.lower()
        return re.search(rf'^hi[\s,]+{self.bot_name}', message_lower) or re.search(rf'^hello[\s,]+{self.bot_name}', message_lower)

    async def respond(self, message:discord.Message):
        return await message.reply(f"Hi!")
