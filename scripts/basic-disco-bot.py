#!/usr/bin/env python3

import time

import discord
from dotenv import load_dotenv

from disco.bot import DiscoBot
from disco.cogs.help import HelpMenus
from disco.cogs.dexscreener import DexScreener
from disco.listener.wen import WenHandler
from disco.listener.hello import HelloHandler
from disco.listener.gm import GmHandler
from disco.listener.gn import GnHandler
from disco.listener.thankyou import ThankYouHandler
from disco.listener.bad import BadHandler


class Basic(DiscoBot):
    def run(self):
        self.create_bot(command_prefix=['b.', 'B.'])

        # disco cogs
        self.add_cog(HelpMenus(help_messages))
        self.add_cog(DexScreener())

        # disco listeners
        self.add_listener(WenHandler())
        self.add_listener(HelloHandler())
        self.add_listener(GmHandler())
        self.add_listener(GnHandler())
        self.add_listener(ThankYouHandler())
        self.add_listener(BadHandler())

        self.connect()

    async def handle_ready(self):
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="b.help for help")
            )

        self.logger.info(f'{self.bot.user.name} has connected')
        print("Ready to go!")


help_messages = {
    "main": """
The following commands are available:

- `b.help about    `: About This Bot
- `t [symbol]      `: spot price for `symbol` (tsuki style)
""",
    "about": """
**BasicBot**. Help is available with the command `b.help`.
""",
}


if __name__ == "__main__":

    load_dotenv()

    while True:
        try:
            Basic().run()
        except Exception as e:
            print(e)
            time.sleep(5)
