import discord

from discord.ext import commands

from crypto_watcher.models import Quote

from ..cog import BaseCog

class MetricsEcosystem(BaseCog):
    def __init__(self):
        super().__init__()
        self.metrics = self.config['ecosystem']

    @commands.command(name="eco")
    async def on_ecosystem(self, ctx, duration="1h"):
        if not await self.is_allowed(ctx=ctx):
            return

        working_msg = await ctx.send(f"Working...")

        if duration in ["24h", "1d"]:
            duration = "1d"
            pct_key = 'pct_1d'
        else:
            duration = "1h"
            pct_key = 'pct_1h'

        embed = discord.Embed(
            title=f"Ecosystem Dashboard ({duration})",
            colour=discord.Color.green()
        )

        for symbol, pair in self.metrics.items():
            result = Quote.get_pair_metrics_current(pair)
            embed.add_field(
                name=f"{symbol.upper()} ({result[pct_key]*100:>0.1f}%)",
                value=f"{result['price']:0.2f} USD", inline=True)

        embed.add_field(name="command", value=f"`f.eco {duration}`", inline=True)

        await working_msg.delete()
        await ctx.send(embed=embed)
