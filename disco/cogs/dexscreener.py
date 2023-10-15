import random
import datetime

from pprint import pprint

import requests
import discord

from discord.ext import commands

from ..cog import BaseCog

dexscreener_api_url = "https://api.dexscreener.com/latest/dex/search/?q={query}"


class DexScreener(BaseCog):
    def __init__(self):
        super().__init__()
        self.user_rate_limit = False

    @commands.command()
    async def dex(self, ctx, base_token=None, quote_token=None):
        if not await self.is_allowed(ctx=ctx):
            return

        if not base_token:
            await ctx.reply("usage: `f.dex <base_token> [quote_token]`")
            return

        results = get_search(base_token, quote_token)

        if results:
            top_hit = results[0]

            buf = ""
            buf += f"`Top Chain: {top_hit['chain_id'].title():>20s}`\n"
            buf += f"`Top DEX:   {top_hit['dex_id'].title():>20s}`\n"
            buf += f"`Liquidity: {top_hit['liquidity']:16,.0f} USD`\n"
            buf += f"`FDV:       {top_hit['fdv']:16,.0f} USD`\n"
            buf += "`-------------------------------`\n"

            for result in results:
                pct_str = f"{result['pct24']:0.2f}%"
                pair_str = f"{result['base'].upper()}/{result['quote'].upper()}"
                buf += f"[`{pair_str:<10s}`]({result['url']}) `{result['price_usd']:>11.4f} {pct_str:>8s} ({result['dex_id'][:10]})`\n"

            img_url = top_hit['url'].replace("https://dexscreener.com", "https://io.dexscreener.com/screenshot/chart")
            now_ts = int(datetime.datetime.utcnow().timestamp()) * 1000
            img_url = f"{img_url}.png?width=1200&height=600&timestamp={now_ts}"
            # buf += f"{img_url}"

            embed = discord.Embed(
                title=top_hit['name'],
                description=buf,
                colour=discord.Color.green()
            )
            embed.set_image(url=img_url)

            await ctx.send(embed=embed)
            # await ctx.reply(top_hit['url'])
        else:
            await ctx.reply("no results found")


def get_search(base_token, quote_token=None):
    base_token = base_token.lower()
    if quote_token:
        quote_token = quote_token.lower()
        query = f"{base_token}%20{quote_token}"
    else:
        query = base_token

    req = dexscreener_api_url.format(query=query)
    resp = requests.get(req)

    if resp.status_code == 200:
        data = resp.json()
    else:
        data = None

    if data and 'pairs' in data:
        pairs = data['pairs']

        results = []

        for pair in pairs:
            # only keep when a token matches the query
            pair_base_token = pair['baseToken']['symbol'].lower()
            pair_quote_token = pair['quoteToken']['symbol'].lower()
            tokens = [pair_base_token, pair_quote_token]

            # print(pair)
            candidate = {
                "url": pair['url'],
                "base": pair_base_token,
                "quote": pair_quote_token,
                "name": pair['baseToken']['name'],
                "dex_id": pair['dexId'],
                "chain_id": pair['chainId'],
                "liquidity": pair['liquidity']['usd'] if 'liquidity' in pair else 0.0,
                "pct24": pair['priceChange']['h24'] if 'priceChange' in pair else 0.0,
                "price_usd": float(pair['priceUsd']) if 'priceUsd' in pair else 0.0,
                "fdv": pair['fdv'] if 'fdv' in pair else 0.0,
            }

            if quote_token:
                # only keep when both tokens match the query
                if base_token in tokens and quote_token in tokens:
                    results.append(candidate)
                elif base_token in tokens and f"w{quote_token}" in tokens:
                    results.append(candidate)
                elif quote_token in tokens and f"w{base_token}" in tokens:
                    results.append(candidate)                    
                elif f"w{quote_token}" in tokens and f"w{base_token}" in tokens:
                    results.append(candidate)                    
            else:
                if base_token in tokens or f"w{base_token}" in tokens:
                    results.append(candidate)
            
        # sort by liquidity
        results = sorted(results, key=lambda x: x['liquidity'], reverse=True)
        results_top = results.copy()[0:10]
        return results_top
    else:
        return None
