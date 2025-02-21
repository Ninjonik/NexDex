import builtins
import datetime
import json
import os
import traceback
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


def join_array_into_string(arr):
    str_arr = [str(element) for element in arr]

    result = '\n'.join(str_arr)

    return result


def datetime_now():
    return datetime.datetime.now(datetime.UTC)


async def send_response(status: Literal["success", "error", "loading"], message: str, interaction: discord.Interaction,
                        response=False, ephemeral=True):
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
    return await interaction.response.send_message(emoji + " " + message, ephemeral=ephemeral)


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


def format_countryball_string(countryball):
    return f"- #{countryball['id']} {countryball['countryball']['name']} | ⚔️ {countryball['countryball']['attack']} ATK | ❤️ {countryball['countryball']['hp']} HP\n"


async def get_countryballs_string(battle_id: int):
    countryballs_data = await make_api_request(f"countryballs/{battle_id}", "GET")
    attacker_countryballs = json.loads(countryballs_data["battle"]["attacker_countryballs"])
    defender_countryballs = json.loads(countryballs_data["battle"]["defender_countryballs"])
    attacker_countryballs = [countryballs_data["countryballs"][str(countryball_id)] for countryball_id in
                             attacker_countryballs]
    defender_countryballs = [countryballs_data["countryballs"][str(countryball_id)] for countryball_id in
                             defender_countryballs]
    print("CB STRING DATA:", attacker_countryballs, defender_countryballs)

    return "".join([format_countryball_string(cb) for cb in attacker_countryballs]), "".join(
        [format_countryball_string(cb) for cb in defender_countryballs])


async def make_battle_embed(attacker: discord.User, defender: discord.User, battle_id: int):
    attacker_string, defender_string = ["", ""]
    if battle_id:
        attacker_string, defender_string = await get_countryballs_string(battle_id)
    print("DEF STR, ATT STR: ", defender_string, attacker_string)

    embed = discord.Embed(
        title="Countryballs Battle Plan",
        description="Add or remove countryballs using:\n/battle add\n/battle remove\n\n🔒 Lock your formation when ready!\n\nRemember: Once locked, you can't change your plan! 🔗\n\nClick \"Lock\" to begin the battle! 💥",
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
                    print(response)
                    print(await response.json())
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


class SelectCountryball(discord.ui.Select):
    def __init__(self, options):
        """
        options=[
            discord.SelectOption(label="Option 1",emoji="👌",description="This is option 1!"),
            discord.SelectOption(label="Option 2",emoji="✨",description="This is option 2!"),
            discord.SelectOption(label="Option 3",emoji="🎭",description="This is option 3!")
        ]
        """
        super().__init__(placeholder="Select an option", max_values=1, min_values=1, options=options)


class LockInDialog(discord.ui.View):
    def __init__(self, client):
        super().__init__(timeout=None)
        self.client = client

    @discord.ui.button(label="Lock in", style=discord.ButtonStyle.success, custom_id="ld_lockin", emoji="✔️")
    async def ld_lockin(self, interaction: discord.Interaction, button: discord.Button):
        await send_response("loading", "Gathering your fellow Countryball allies...", interaction)
        user_id = str(interaction.user.id)

        await check_user(interaction.user)

        check = await make_api_request("battle", "GET", {
            "where": [
                [
                    "id",
                    str(interaction.message.id)
                ],
                [
                    "attacker_id",
                    user_id,
                ]
            ],
            "orWhere": [
                [
                    "id",
                    str(interaction.message.id)
                ],
                [
                    "defender_id",
                    user_id
                ]
            ]
        })
        if not check or len(check) < 1:
            return await send_response("error", "Battle wasn't found..",
                                       interaction, True)

        battle_data = check[-1]
        user_type = "attacker" if battle_data["attacker_id"] == str(interaction.user.id) else "defender"
        if user_type == "attacker" and battle_data["status"] == 1 or user_type == "defender" and battle_data[
            "status"] == 2 or battle_data["status"] > 2:
            return await send_response("error",
                                       "You are already locked in this battle or the battle has already been started.",
                                       interaction, True)

        new_status = -1

        if user_type == "attacker":
            new_status = 1
            if battle_data["status"] == 2:
                new_status = 3

        if user_type == "defender":
            new_status = 2
            if battle_data["status"] == 1:
                new_status = 3

        res = await make_api_request(f"battle/{battle_data['id']}", "POST", {"status": new_status})
        if not res:
            return await send_response("error", "There was an error while locking you up...", interaction,
                                       True)
        # Start the battle
        if new_status == 3:
            await send_response("loading", "Successfully locked you in, starting the battle now.", interaction, True,
                                False)
            # Get countryballs data
            attacker_countryballs = json.loads(battle_data["attacker_countryballs"])
            defender_countryballs = json.loads(battle_data["defender_countryballs"])
            print(attacker_countryballs)
            attacker_countryballs = [int(countryball_id) for countryball_id in attacker_countryballs]
            print(attacker_countryballs)
            defender_countryballs = [int(countryball_id) for countryball_id in defender_countryballs]
            countryballs_list = attacker_countryballs + defender_countryballs
            countryballs_data = await make_api_request("countryballs", "GET",
                                                       {"list": countryballs_list})
            print(countryballs_data)
            if not countryballs_data:
                return await send_response("error", "There was an error while getting the countryballs data...",
                                           interaction,
                                           True)
            countryballs_data = countryballs_data["countryballs"]
            attacker_countryballs = [countryballs_data[str(countryball_id)] for countryball_id in attacker_countryballs]
            defender_countryballs = [countryballs_data[str(countryball_id)] for countryball_id in defender_countryballs]
            print(attacker_countryballs, defender_countryballs)

            # Get user data
            attacker = await interaction.guild.fetch_member(int(battle_data["attacker_id"]))
            defender = await interaction.guild.fetch_member(int(battle_data["defender_id"]))

            battle_log = []
            att_cb_left = attacker_countryballs
            def_cb_left = defender_countryballs

            for index, first_cb in enumerate(attacker_countryballs):
                first_cb = first_cb["countryball"]
                battle_log.append(f"{attacker.mention}'s Countryball {first_cb['name']}#{first_cb['id']} has joined "
                                  f"the battle.")
                for index2, second_cb in enumerate(defender_countryballs):
                    second_cb = second_cb["countryball"]
                    if second_cb["hp"] < 0:
                        continue

                    battle_log.append(
                        f"{defender.mention}'s Countryball {second_cb['name']}#{second_cb['id']} has joined "
                        f"the battle against {attacker.mention}'s Countryball {first_cb['name']}#{first_cb['id']}.")

                    second_cb["hp"] -= first_cb["attack"]
                    battle_log.append(
                        f"{attacker.mention}'s Countryball {first_cb['name']}#{first_cb['id']} has dealt "
                        f"{first_cb['attack']} damage to {defender.mention}'s {second_cb['name']}#{second_cb['id']}."
                        f" resulting in {second_cb['hp']} HP left.")
                    if second_cb["hp"] < 0:
                        battle_log.append(
                            f"{defender.mention}'s Countryball {second_cb['name']}#{second_cb['id']} has died.")
                        def_cb_left.pop(index2)
                        continue

                    first_cb["hp"] -= second_cb["attack"]
                    battle_log.append(
                        f"{defender.mention}'s Countryball {second_cb['name']}#{second_cb['id']} has dealt "
                        f"{second_cb['attack']} damage to {defender.mention}'s {first_cb['name']}#{first_cb['id']}"
                        f" resulting in {first_cb['hp']} HP left.")
                    if first_cb["hp"] < 0:
                        battle_log.append(
                            f"{attacker.mention}'s Countryball {first_cb['name']}#{first_cb['id']} has died.")
                        att_cb_left.pop(index)
                        # TODO This breaks up for some reason or osmething, second iteration doesnt go on -- WORKS FOR NOW
                        break

            print(battle_log)
            print(att_cb_left, def_cb_left)
            print(len(att_cb_left), len(def_cb_left))

            attacker_winner = len(att_cb_left) > len(def_cb_left)
            if attacker_winner:
                battle_log.append(f"{attacker.mention}'s Countryballs have emerged victorious in "
                                  f"their offense against {defender.mention}'s Countryballs!")
            else:
                battle_log.append(f"{defender.mention}'s Countryballs have emerged victorious in "
                                  f"their defense against {attacker.mention}'s Countryballs!")

            battle_log.append(f"{attacker.mention} countryballs left: {att_cb_left}")
            battle_log.append(f"{defender.mention} countryballs left: {def_cb_left}")

            await send_response("success", "Battle has ended.", interaction, True)

            embed = discord.Embed(
                title=f"Battle #{battle_data["id"]} between {attacker.mention} and {defender.mention} has ended!",
                description=f"Battle has resulted in the {f"attacking victory of {attacker.mention}" if attacker_winner else f"defending victory of {defender.mention}"}",
                colour=0x00ff00 if attacker_winner else 0xff0000,
                timestamp=datetime_now()
            )
            await interaction.channel.send(embed=embed, content=join_array_into_string(battle_log))
            await make_api_request(f"battle/{battle_data['id']}", "POST", {"status": 4, "winner": str(
                attacker.id) if attacker_winner else str(defender.id)})
        else:
            await send_response("success", "Successfully locked in, waiting for the other player to lock in...",
                                interaction, True, False)


class ClaimCountryball(discord.ui.View):
    def __init__(self, client, drop):
        super().__init__(timeout=None)
        self.drop = drop

    @discord.ui.button(style=discord.ButtonStyle.primary,
                       custom_id="cc_claim", label="Guess & Claim!")
    async def cc_claim(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ClaimCountryballDialog(self.drop))


class ClaimCountryballDialog(discord.ui.Modal, title='Claim a countryball!'):
    name = discord.ui.TextInput(label='Name of the countryball')

    def __init__(self, drop):
        super().__init__(timeout=None)
        self.drop = drop

    async def on_submit(self, interaction: discord.Interaction):
        name = self.name.value
        print("Name:", name, interaction.message.id)
        print("DROP:", self.drop)
        print("CB Name:", self.drop["countryball"]["name"])
        if name.lower() == self.drop["countryball"]["name"].lower():
            res = await make_api_request(f"dropped/{interaction.message.id}", "POST",
                                         {"owner_id": str(interaction.user.id)})
            print(res)
            if not res or res.get("error", False):
                return await interaction.response.send_message("😭 This countryball has already been claimed.")
            else:
                return await interaction.response.send_message(
                    f"🎉 Countryball successfully claimed by {interaction.user.mention}.")
        else:
            return await interaction.response.send_message(
                f"😠 {interaction.user.mention}, that is not a correct name of this Countryball!")

    async def on_error(self, interaction: discord.Interaction, error):
        print(error)
        print(traceback.format_exc())
        await interaction.response.send_message('There was an error while processing the request.', ephemeral=True)
