import os
import re
import json
import time
import threading

from pycoingecko import CoinGeckoAPI
import discord

from disco.handler import BaseHandler

class TsukiHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.user_rate_limit = False

        self.cg = CoinGeckoAPI()
        self.coins_list = []
        self.coin_symbol_lookup = {}
        self.coins_list_filename = os.path.join(self.config["state_path"], "cg-coin-list.json")

        self.is_refreshing = False
        if self.is_cache_stale():
            self.logger.info("Load tsuki cg coin list from live site")
            self.refresh_cache()
        else:
            self.logger.info("Load tsuki cg coin list from json")
            self.load_cache()

    async def check(self, message:discord.Message):
        return re.search(r'^t [\w\s]+$', message.content.lower())

    async def respond(self, message):
        # await message.delete(delay=2)

        message_lower = message.content.lower()
        m = re.search(r'^t ([\w\s]+)$', message_lower)
        if not m:
            return

        if self.is_refreshing:
            msg = await message.channel.send("Refreshing coin list, please wait...")
            await msg.delete(delay=2)
            return

        id_list = [self.coin_symbol_lookup[coin_symbol] for coin_symbol in m.group(1).lower().split(" ") if coin_symbol in self.coin_symbol_lookup]

        result = self.cg.get_price(
            ",".join(id_list),
            vs_currencies="usd",
            include_market_cap=False,
            include_24hr_vol=False,
            include_24hr_change=True,
            include_last_updated_at=False,
        )

        not_found = []

        response = ""

        for coin_symbol in m.group(1).lower().split(" "):
            if coin_symbol in self.coin_symbol_lookup:
                data = result[self.coin_symbol_lookup[coin_symbol]]
                if not data["usd_24h_change"]:
                    data["usd_24h_change"] = 0
                # msg = await message.channel.send(f"`{coin_symbol.upper():>6}` : `{data['usd']:14.4f} USD` `({data['usd_24h_change']:>7.2f}% 24h)`")
                response += f"`{coin_symbol.upper():>6}` : `{data['usd']:14.4f} USD` `({data['usd_24h_change']:>7.2f}% 24h)`\n"
            else:
                not_found.append(coin_symbol)

        if len(not_found) > 0:
            response += f"Could not find: `{', '.join(not_found)}`"

        if self.is_cache_stale():
            self.refresh_cache()

        return await message.channel.send(response)

    ###
    # Cache stuff

    def load_cache_if_newer(self):
        mtime = os.path.getmtime(self.coins_list_filename)
        if mtime > self.mtime:
            self.logger.info("Load newer tsuki cg coin list from json")
            self.load_cache()

    def load_cache(self):
        "load the coin list from the json file"

        self.mtime = os.path.getmtime(self.coins_list_filename)
        with open(self.coins_list_filename, "r") as f:
            self.coins_list = json.load(f)

        for coin in self.coins_list:
            if coin['symbol'].lower() not in self.coin_symbol_lookup:
                self.coin_symbol_lookup[coin['symbol'].lower()] = coin['id'].lower()

    def refresh_cache(self):
        "load the coin list from the live site"

        def refresh_in_background():
            new_coins_list = []
            self.is_refreshing = True

            # first rank by volume
            for page in range(1, 11):
                new_coins_list += self.cg.get_coins_markets(
                    vs_currency="usd",
                    per_page=250,
                    page=page,
                    sparkline=False,
                    price_change_percentage="24h"
                )
                self.logger.info(f"Load cg page {page}")
                time.sleep(30)

            # first rank by volume
            for page in range(1, 11):
                new_coins_list += self.cg.get_coins_markets(
                    vs_currency="usd",
                    order="volume_desc",
                    per_page=250,
                    page=page,
                    sparkline=False,
                    price_change_percentage="24h"
                )
                self.logger.info(f"Load cg page {page}")
                time.sleep(30)

            # rank by market cap
            for page in range(1, 11):
                new_coins_list += self.cg.get_coins_markets(
                    vs_currency="usd",
                    order="market_cap_desc",
                    per_page=250,
                    page=page,
                    sparkline=False,
                    price_change_percentage="24h"
                )
                self.logger.info(f"Load cg page {page}")
                time.sleep(30)

            with open(self.coins_list_filename, "w") as f:
                json.dump(new_coins_list, f, indent=2)
            self.logger.info(f"wrote {len(new_coins_list)} coins to {self.coins_list_filename}")
            self.load_cache()
            self.is_refreshing = False

        daemon = threading.Thread(
            target=refresh_in_background,
            daemon=True,
            name='Refresh in background'
        )
        daemon.start()

    def is_cache_stale(self):
        "return True if file is more than 24 hours old, does not exist, or is invalid"

        try:
            mtime = os.path.getmtime(self.coins_list_filename)
        except FileNotFoundError:
            return True

        try:
            with open(self.coins_list_filename, "r") as f:
                dummy = json.load(f)
        # return True if file is invalid
        except:
            return True

        # return True if file is more than 3 days old
        return time.time() - mtime > 60*60*24*3
