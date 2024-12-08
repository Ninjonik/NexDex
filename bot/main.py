import asyncio
import datetime
import os
import platform

import discord
import discord.utils
from colorama import Fore
from discord.ext import tasks, commands
from dotenv import load_dotenv, find_dotenv

import presets
from presets import print

load_dotenv(find_dotenv())

intents = discord.Intents.all()
intents.typing = True
intents.presences = True
intents.members = True
intents.guilds = True


def seconds_until(hours, minutes):
    given_time = datetime.time(hours, minutes)
    given_time.replace(tzinfo=datetime.timezone.utc)
    now = presets.datetime_now()
    future_exec = datetime.datetime.combine(now, given_time)
    if (future_exec - now).days < 0:  # If we are past the execution, it will take place tomorrow
        future_exec = datetime.datetime.combine(now + datetime.timedelta(days=1), given_time)  # days always >= 0

    return (future_exec - now).total_seconds()


@tasks.loop(seconds=30)
async def status_loop():
    await client.wait_until_ready()
    await client.change_presence(status=discord.Status.idle,
                                 activity=discord.Activity(type=discord.ActivityType.watching,
                                                           name=f"{len(client.guilds)} servers. 🧐"))
    await asyncio.sleep(10)
    memberCount = 0
    for guild in client.guilds:
        memberCount += guild.member_count
    await client.change_presence(status=discord.Status.dnd,
                                 activity=discord.Activity(type=discord.ActivityType.listening,
                                                           name=f"{memberCount} people! 😀", ))
    await asyncio.sleep(10)


class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('.'), intents=discord.Intents().all())
        self.cogsList = []

    async def setup_hook(self):
        for ext in self.cogsList:
            await self.load_extension(ext)

    async def on_ready(self):
        print("Logged in as " + Fore.YELLOW + self.user.name)
        print("Bot ID " + Fore.YELLOW + str(self.user.id))
        print("Discord Version " + Fore.YELLOW + discord.__version__)
        print("Python version " + Fore.YELLOW + platform.python_version())
        print("Syncing slash commands...")
        synced = await self.tree.sync()
        print("Slash commands synced " + Fore.YELLOW + str(len(synced)) + " Commands")
        print("Initializing status....")
        if not status_loop.is_running():
            status_loop.start()

    async def on_guild_join(self, guild):
        # Add guild to the database
        await presets.make_api_request("guild", "POST", {
            "id": str(guild.id),
            "name": guild.name,
            "description": guild.description,
        })

    async def on_guild_update(self, before, after):
        await presets.make_api_request(f"guild/{before.id}", "POST", {
            "name": after.name,
            "description": after.description,
        })

    async def on_guild_remove(self, guild):
        await presets.make_api_request(f"guild/{guild.id}", "DELETE")


client = Client()

client.run(os.getenv("BOT_TOKEN"))
