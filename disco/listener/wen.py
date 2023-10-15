import re
import random

import discord

from disco.handler import BaseHandler

class WenHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.troll_spammers = True
        self.delete_spam = True

    async def check(self, message:discord.Message):
        return re.search(r'^wen\s.+', message.content.lower())

    async def respond(self, message:discord.Message):
        response_idx = random.randint(0, len(soon_responses)-1)
        return await message.reply(soon_responses[response_idx])


soon_responses = \
    ["soon"] * 25 + \
    ["**soon**"] * 25 + \
    ["SOON"] * 20 + \
    ["**SOON**"] * 15 + \
    ["s00n"] * 10 + \
    ["S00N"] * 10 + \
    ["sOOOOOOOOn"] * 5 + \
    ["s00000000n"] * 5 + \
    ["S-O-O-N"] * 4 + \
    ["S O O N"] * 4 + \
    ["**S O O N**"] * 2 + \
    ["E V E N T U A L L Y\nP R O B A B L Y"] * 1 + \
    ["not sure, tbh"] * 1 + \
    ["well, when you think? I'm just starting a conversation..."] * 1
