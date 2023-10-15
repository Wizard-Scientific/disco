import discord

from .permissions import PermissionsHelper


class BaseHandler(PermissionsHelper):

    async def check(self, message:discord.Message):
        "Abstract method - override in listener"
        return False

    async def respond(self, message:discord.Message):
        "Abstract method - override in listener"
        return False
