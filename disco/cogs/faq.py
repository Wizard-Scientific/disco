import os
import re
import json
import random
import logging

import discord

from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()
FAQ_FILENAME = os.getenv('FAQ_FILE')

class FaqHelper:
    def __init__(self):
        self.faq = {}

    def load_faq(self):
        with open(FAQ_FILENAME) as f:
            self.faq = json.load(f)
            logging.info(f"loaded FAQ from {FAQ_FILENAME}")

    @commands.command(name="faq")
    async def do_faq_menu(self, ctx):
        try:
            await ctx.message.delete(delay=5)
        except AttributeError:
            # ignore if the message was already deleted
            pass

        self.load_faq()

        msg = await ctx.channel.send(f"Available FAQ commands: !faq, {', '.join(self.faq.keys())}")
        await msg.delete(delay=30)

    async def do_faq_response(self, message):
        await message.delete(delay=5)

        if self.faq[message.content.lower()]['embed'] is True:
            embed = discord.Embed(
                title=self.faq[message.content.lower()]['title'],
                description=self.faq[message.content.lower()]['description'],
                colour=discord.Color.green()
            )
            embed.add_field(name="FAQ command", value=f"`{message.content.lower()}`")

            embed.set_thumbnail(url=MORPHEUS_LOGO_URL)
            msg = await message.channel.send(embed=embed)
        else:
            msg = await message.channel.send(self.faq[message.content.lower()]['description'])
