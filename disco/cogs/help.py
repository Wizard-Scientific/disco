import discord
from discord.ext import commands

from ..cog import BaseCog

class HelpMenus(BaseCog):
    def __init__(self, help_messages):
        super().__init__()
        self.help_messages = help_messages

    @commands.command()
    async def help(self, ctx, submenu="main"):
        if submenu.lower() in self.help_messages.keys():
            help_str = self.help_messages[submenu.lower()]
        else:
            help_str = self.help_messages["main"]
            submenu = "main"

        embed = discord.Embed(
            title=f"Help: {submenu}",
            description=help_str,
            colour=discord.Color.blue()
        )
        embed.set_thumbnail(url=self.config["profile_icon_url"])

        msg = await ctx.send(embed=embed)
