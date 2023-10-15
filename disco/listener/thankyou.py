import re

import discord

from disco.handler import BaseHandler

class ThankYouHandler(BaseHandler):
    async def check(self, message:discord.Message):
        message_lower = message.content.lower()
        return re.search(rf'^thanks[\s,]+{self.bot_name}', message_lower) or re.search(rf'^thank you[\s,]+{self.bot_name}', message_lower) or re.search(rf'^ty[\s,]+{self.bot_name}', message_lower) or re.search(rf'^thx[\s,]+{self.bot_name}', message_lower)

    async def respond(self, message:discord.Message):
        return await message.reply(f"You're welcome!")
