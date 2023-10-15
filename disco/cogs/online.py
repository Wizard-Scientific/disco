import discord
from discord.ext import commands

from ..models import Guild, ChannelMetrics
from ..cog import BaseCog

class MembersOnline(BaseCog):
    @commands.command()
    async def online(self, ctx, guild_name, duration="1d"):
        await ctx.message.delete(delay=1)

        if duration.lower() not in ['1h', '24h', '1d', '7d', '1w']:
            return

        embed = discord.Embed(
            title=f"Online Total ({duration})",
            description="The number of anons who are actually online.",
            colour=discord.Color.green()
        )

        embed.add_field(name=f"{self.config['bot_name']} command", value=f"`{self.config['bot_prefix']}.online`")

        ts = ChannelMetrics.get_timeseries(Guild.find(name=guild_name), duration=duration)
        fh, fd, filename = self.get_plot("Online Count", ts, duration=duration, yaxis="online_count", downsample=False)
        embed.set_image(url=f"attachment://{filename}")

        await ctx.send(file=fh, embed=embed)

    @commands.command()
    async def members(self, ctx, guild_name, duration="1d"):
        await ctx.message.delete(delay=1)

        if duration.lower() not in ['1h', '24h', '1d', '7d', '1w']:
            return

        embed = discord.Embed(
            title=f"Membership Total ({duration})",
            description="Total number of anons who are members of the discord.  This number includes all anons, whether or not they are currently online.",
            colour=discord.Color.green()
        )

        embed.add_field(name=f"{self.config['bot_name']} command", value=f"`{self.config['bot_prefix']}.members`")

        ts = ChannelMetrics.get_timeseries(Guild.find(name=guild_name), duration=duration)
        fh, fd, filename = self.get_plot("Member Count", ts, duration=duration, yaxis="member_count", downsample=False)
        embed.set_image(url=f"attachment://{filename}")

        await ctx.send(file=fh, embed=embed)
