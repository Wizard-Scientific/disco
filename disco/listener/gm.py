import re

import discord

from disco.handler import BaseHandler

class GmHandler(BaseHandler):
    async def check(self, message:discord.Message):
        return re.search(rf'^gm[\s,]+{self.bot_name}', message.content.lower())

    async def respond(self, message:discord.Message):
        return await message.reply(f"gm")
