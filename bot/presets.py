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


async def send_response(status: Literal["success", "error"], message: str, interaction: discord.Interaction):
    return await interaction.response.send_message(("❌" if status == "error" else "✅") + " " + message, ephemeral=True)


async def check_user(user: discord.User | discord.Member):
    res = make_api_request(f"user/{user.id}", "GET")
    if res:
        return res

    post_res = await make_api_request("user", "POST", {
        "id": str(user.id),
        "name": user.name,
    })

    if post_res:
        get_res = make_api_request(f"user/{user.id}", "GET")
        if get_res: return get_res

    return False


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
