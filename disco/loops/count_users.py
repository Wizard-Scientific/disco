import os
import asyncio
import logging
import datetime

from discord import Status

from .models import Guild, ChannelMetrics


async def count_users_loop(client):
    while True:
        guilds = client.get_guild
        for guild in client.guilds:
            online_count = 0
            for member in guild.members:
                if str(member.status) != "offline":
                    online_count += 1

            guild_obj = Guild.find_or_create(name=guild.name)
            c = ChannelMetrics.create(
                timestamp=datetime.datetime.now(),
                guild=guild_obj,
                member_count=guild.member_count,
                online_count=online_count,
            )
            logging.debug(c)

        await asyncio.sleep(600)
