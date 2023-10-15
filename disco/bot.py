import random
import logging
import traceback

import discord
from discord.ext import commands

from .utils.config import init_config
from .utils.logger import init_logger


class DiscoBot(object):
    def __init__(self):
        self.bot = None
        self.config = init_config()
        self.handlers = []

        self.logger = init_logger(
            filename=self.config["log_filename"],
            level=logging.INFO
        )
        self.logger.info("Logging started")

    def create_bot(self, command_prefix):
        bot = commands.Bot(
            command_prefix=command_prefix,
            intents=discord.Intents(
                messages=True,
                guilds=True,
                members=True,
                reactions=True,
                presences=True
            )
        )

        self.bot = bot
        self.bot.remove_command('help')
        self.bot.config = self.config

        @bot.event
        async def on_member_join(member):
            await self.handle_member_join(member)

        @bot.event
        async def on_error(event, *args, **kwargs):
            await self.handle_error(event, *args, **kwargs)

        @bot.event
        async def on_ready():
            await self.handle_ready()

        @bot.event
        async def on_command_error(ctx, error):
            await self.handle_command_error(ctx, error)

        @bot.event
        async def on_message(message):
            await self.handle_message(message)

    async def handle_member_join(self, member):
        pass

    async def handle_error(self, event, *args, **kwargs):
        self.logger.warning(traceback.format_exc()) #logs the error

    async def handle_ready(self):
        self.logger.info(f'{self.bot.user.name} has connected')

        # if not DEBUG:
        #     await count_users_loop(self.bot)

    async def handle_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            logging.info(f"Command not found: {ctx.message.author.display_name} said '{ctx.message.content}'")

            msg = await ctx.message.reply(f"Not a command.")
            await ctx.message.delete(delay=2)
            await msg.delete(delay=1)

        else:
            self.logger.error(f"command {ctx.message.content} generated error: {error}")
            raise error

    async def handle_message(self, message):
        if message.author == self.bot.user:
            return

        for handler in self.handlers:
            if await handler.check(message):
                if await handler.is_allowed(message):
                    msg = await handler.respond(message)

                    # clean up if configured
                    if handler.delete_own:
                        self.logger.info("deleting own message")
                        await msg.delete(delay=handler.delete_own_delay)

                    if handler.delete_invocation:
                        self.logger.info("deleting invocation")
                        await message.delete(delay=handler.delete_spam_delay)
                else:
                    # message was not allowed; remove spam invocation
                    if handler.delete_spam:
                        self.logger.info("deleting spam invocation")
                        await message.delete(delay=handler.delete_spam_delay)

                    if handler.user_rate_limit and handler.troll_spammers and random.randint(0, 10) == 0:
                        self.logger.info(f"trolling {message.author.display_name} for spamming")
                        num_spams = handler.get_num_spams(message.author.id)
                        msg = await message.reply(f"({message.author.display_name} has spammed this {num_spams} times)")
                        await msg.delete(delay=handler.delete_spam_delay)


        # continue to process messages when not handled
        await self.bot.process_commands(message)

    def add_cog(self, cog):
        self.bot.add_cog(cog)

    def add_listener(self, listener):
        self.handlers.append(listener)

    def connect(self):
        self.logger.info(f"Connecting to discord")
        self.bot.run(self.config['discord_token'])
