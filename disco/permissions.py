import logging
import datetime

import discord
from discord.ext import commands

from .utils.state import State
from .utils.logger import init_logger
from .utils.config import init_config


class PermissionsHelper(object):
    def __init__(self):
        super().__init__()

        if "config" not in self.__dict__:
            self.config = init_config()

        if "logger" not in self.__dict__:
            self.logger = init_logger()

        self.bot_name = self.config["bot_name"]
        self.allowed_channels = self.config["allowed_channels"]
        self.not_allowed_message = "Not available in this channel"

        if "state" not in self.__dict__:
            self.state = State(
                self.__class__.__name__,
                state_path=self.config["state_path"],
                default={'count': 0, 'spam': 0, 'last': None}
            )

        # delete invocation messages no matter what?
        self.delete_invocation = False

        # delete invocation messages if they are rate limited?
        self.delete_spam = False
        self.delete_spam_delay = 5 # seconds

        # delete own messages after cooldown?
        self.delete_own = False
        self.delete_own_delay = 60 # seconds

        # randomly troll spammers?
        self.troll_spammers = False

        # apply global rate limit to all users?
        self.global_rate_limit = False
        # apply per-user rate limit?
        self.user_rate_limit = True
        # how long is the cooldown for the rate limit?
        self.cooldown = 300 # seconds

    async def is_allowed(self, message:discord.Message=None, ctx:commands.Context=None):
        """
        Check for server, channel, and rate limit
        """
        if ctx:
            message = ctx.message

        if await self.is_server_allowed(message) and await self.is_channel_allowed(message):
            return not await self.is_rate_limited(message)
        else:
            if self.not_allowed_message:
                msg = await message.channel.send(self.not_allowed_message)
                await msg.delete(delay=3)
            return False

    async def is_server_allowed(self, message:discord.Message=None, ctx:commands.Context=None):
        """
        Checks whether the message is in an allowed server
        """
        if ctx:
            message = ctx.message

        server_name = message.guild.name
        if server_name in self.allowed_channels.keys():
            return True
        else:
            self.logger.warning(f"is_server_allowed: False '{server_name}'")

    async def is_channel_allowed(self, message:discord.Message=None, ctx:commands.Context=None):
        """
        Checks whether the message is in an allowed channel
        """
        if len(self.allowed_channels) == 0:
            return True
        if ctx:
            message = ctx.message

        server_name = message.guild.name
        channel_name = message.channel.name

        if server_name in self.allowed_channels:
            if len(self.allowed_channels[server_name]) == 0:
                return True
            elif channel_name in self.allowed_channels[server_name]:
                return True
            else:
                self.logger.warning(f"is_channel_allowed: False '{server_name}:{channel_name}'")

    async def is_rate_limited(self, message:discord.Message=None, ctx:commands.Context=None):
        """
        Checks whether the listener is rate limited - either per user or globally
        """
        if ctx:
            message = ctx.message

        cooldown = datetime.timedelta(seconds=self.cooldown)

        if self.global_rate_limit:
            user_id = "__global__"
            user_name = "__global__"
        elif self.user_rate_limit:
            user_id = str(message.author.id)
            user_name = message.author.display_name
        else:
            # not rate limited
            return False

        user_profile = self.state[user_id]

        # if user has no profile, set up the last time
        if user_profile['last'] is None:
            # ensure elapsed is longer than the cooldown period
            last_time = datetime.datetime.now() - cooldown - datetime.timedelta(seconds=1)
        else:
            last_time = datetime.datetime.fromtimestamp(user_profile['last'])

        # enforce cooldown
        if last_time > (datetime.datetime.now() - cooldown):           
            # increment spam counter and save state
            user_profile['spam'] += 1
            self.state[user_id] = user_profile

            # the user is rate limited
            self.logger.info(f"{self.__class__.__name__}: {user_name}, spam: {user_profile['spam']} ")
            return True
        else:
            user_profile['count'] += 1
            user_profile['last'] = datetime.datetime.timestamp(datetime.datetime.now())
            self.state[user_id] = user_profile

            # the user is not rate limited
            self.logger.info(f"{self.__class__.__name__}: {user_name}, count: {user_profile['count']} ")
            return False

    def get_num_spams(self, user_id):
        """
        Returns the number of times a user has been rate limited
        """
        if self.user_rate_limit:
            user_profile = self.state[str(user_id)]
            if user_profile['spam'] is None:
                return 0
            else:
                return user_profile['spam']
        else:
            return 0
