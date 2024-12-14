import asyncio
import datetime
import math
import os
import platform
import random

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

spawn_table = {}


def calculate_coefficient(member_count):
    base = max(member_count, 100)  # Ensure a minimum of 10 messages
    coefficient = math.floor(base * 1 - (base / 1.5 + 1)) + random.uniform(-base / 20, base / 5)
    if (coefficient < 0): coefficient = -1 * coefficient
    if (base < 200 and coefficient < base / 5): coefficient = coefficient * 5
    if (base < 100 and coefficient < 100): coefficient = base * random.randint(8, 10)
    return math.floor(coefficient)


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
        self.cogsList = ["cogs.battle"]

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
        print("Initializing guilds spawn table...")
        guilds = await presets.make_api_request("guild", "GET")
        for guild in guilds:
            discord_guild = self.get_guild(int(guild["id"]))
            member_count = discord_guild.member_count
            coefficient = calculate_coefficient(member_count)
            spawn_table[discord_guild.id] = coefficient
        print(spawn_table)

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

    async def on_message(self, message):
        guild_id = str(message.guild.id)
        spawn = spawn_table[guild_id]
        spawn -= 1
        if spawn == 0:
            spawn_table[guild_id] = calculate_coefficient(message.guild.member_count)

            # SPAWN THE COUNTRYBALL
        else:
            spawn_table[guild_id] = spawn


client = Client()

client.run(os.getenv("BOT_TOKEN"))
