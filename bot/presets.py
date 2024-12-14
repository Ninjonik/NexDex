import asyncio
import builtins
import datetime
import os
from typing import Optional, Literal

import aiohttp
import discord
from colorama import Back, Fore, Style
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Get APP_URL and INTERNAL_API_TOKEN from environment variables
app_url = os.getenv("APP_URL")
internal_api_token = os.getenv("INTERNAL_API_TOKEN")


def prefix():
    return (Back.BLACK + Fore.GREEN + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") + Back.RESET + Fore.WHITE +
            Style.BRIGHT)


def print(*args, **kwargs):
    """
    Custom print function that adds a prefix to the start of the output.
    """
    message = prefix() + ' ' + ' '.join(map(str, args))
    # Call the original print function from the builtins module
    builtins.print(message, **kwargs)


async def ban(member, reason):
    await member.ban(reason=reason)


async def kick(member):
    await member.kick()


def log(content):
    print(prefix() + content)


def datetime_now():
    return datetime.datetime.now(datetime.UTC)


async def send_response(status: Literal["success", "error", "loading"], message: str, interaction: discord.Interaction,
                        response=False):
    emoji = ""
    match status:
        case "success":
            emoji = "✅"
        case "error":
            emoji = "❌" if status == "error" else ""
        case "loading":
            emoji = "⏳"
    if response:
        return await interaction.edit_original_response(content=emoji + " " + message)
    return await interaction.response.send_message(emoji + " " + message, ephemeral=True)


async def check_user(user: discord.User | discord.Member):
    res = await make_api_request(f"user/{user.id}", "GET")
    if res:
        return res

    post_res = await make_api_request("user", "POST", {
        "id": str(user.id),
        "name": user.name,
    })

    if post_res:
        get_res = await make_api_request(f"user/{user.id}", "GET")
        if get_res: return get_res

    return False


async def get_countryball_data(countryball_id):
    data = await make_api_request(f"countryball/{countryball_id}", "GET")
    print("RES DATA:", data)
    print("ID DATA:", countryball_id)
    return f"- #{data['id']} {data['name']} | ⚔️ {data['attack']} ATK | ❤️ {data['hp']} HP\n"


async def format_countryballs(countryball_ids):
    tasks = [get_countryball_data(id) for id in countryball_ids]
    return await asyncio.gather(*tasks)


async def process_countryballs(defender_countryballs=None, attacker_countryballs=None):
    defender_tasks = [get_countryball_data(id) for id in defender_countryballs] if defender_countryballs else []
    attacker_tasks = [get_countryball_data(id) for id in attacker_countryballs] if attacker_countryballs else []

    defender_results = await asyncio.gather(*defender_tasks)
    attacker_results = await asyncio.gather(*attacker_tasks)

    return "".join(defender_results), "".join(attacker_results)


async def make_battle_embed(attacker: discord.User, defender: discord.User,
                            attacker_countryballs=None, defender_countryballs=None):
    defender_string, attacker_string = await process_countryballs(defender_countryballs, attacker_countryballs)

    embed = discord.Embed(
        title="Countryballs Battle Plan",
        description="Add or remove countryballs using:\n</battle add>\n</battle remove>\n\n🔒 Lock your formation when ready!\n\nRemember: Once locked, you can't change your plan! 🔗\n\nClick \"Lock\" to begin the battle! 💥",
        colour=0x00b0f4,
        timestamp=datetime_now()
    )

    embed.add_field(name=f"{attacker.name}:", value=attacker_string, inline=True)
    embed.add_field(name=f"{defender.name}:", value=defender_string, inline=True)

    embed.set_footer(text="NexDex", icon_url="https://slate.dan.onl/slate.png")
    return embed


async def make_api_request(endpoint: str, method: str = "GET", body: Optional[dict] = None, headers: dict = None) -> \
        Optional[aiohttp.ClientResponse]:
    if not headers:
        headers = {}

    if not app_url or not internal_api_token:
        print("Error: APP_URL or INTERNAL_API_TOKEN is not set.")
        return None

    # Concatenate APP_URL with "/api/v1/"
    full_url = f"{app_url}/api/v1/{endpoint}"

    # Add Authorization header
    headers["Authorization"] = f"Bearer {internal_api_token}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.request(method, full_url, json=body, headers=headers) as response:
                if response.status != 200:
                    return None
                return await response.json()
    except Exception as e:
        print(f"Error making request: {e}")
        return None


def convert_datetime_from_str(datetime_str: None | str) -> None | datetime.datetime:
    formats = ["%d.%m.%Y %H:%M", "%d-%m-%Y %H:%M", "%d/%m/%Y %H:%M"]
    for fmt in formats:
        try:
            datetime_obj = datetime.datetime.strptime(datetime_str, fmt)
            datetime_obj.replace(tzinfo=datetime.timezone.utc)
            return datetime_obj
        except ValueError:
            pass
    else:
        return None
