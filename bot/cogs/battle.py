import json

import discord
from discord import app_commands
from discord.ext import commands

from bot import presets
from bot.presets import make_battle_embed


class Battle(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    group = app_commands.Group(name="battle", description="Attack a chosen user with your countryballs!")

    @group.command(name='start', description="Attack a chosen user with your countryballs!")
    @app_commands.describe(
        defender="Select a user you wish to attack.",
    )
    async def battle_start(self, interaction: discord.Interaction, defender: discord.User):
        attacker_id = str(interaction.user.id)
        defender_id = str(defender.id)

        await presets.send_response("loading", "Gathering your Countryball General Staff...", interaction)

        await presets.check_user(interaction.user)
        await presets.check_user(defender)

        check = await presets.make_api_request("battle", "GET", {
            "where": [
                [
                    "attacker_id",
                    attacker_id,
                ],
                [
                    "status",
                    "<=",
                    1,
                ]
            ],
            "orWhere": [
                [
                    "defender_id",
                    attacker_id
                ],
                [
                    "status",
                    2,
                ]
            ]
        })
        if check and len(check) > 0:
            return await presets.send_response("error", "You can't start a battle if"
                                                        " you are already inside a one.", interaction, True)

        check_defender = await presets.make_api_request("battle", "GET", {
            "where": [
                [
                    "attacker_id",
                    defender_id,
                ],
                [
                    "status",
                    "<=",
                    1,
                ]
            ],
            "orWhere": [
                [
                    "defender_id",
                    defender_id
                ],
                [
                    "status",
                    2,
                ]
            ]
        })

        message = await interaction.channel.send(
            embed=await make_battle_embed(attacker=interaction.user, defender=defender),
            content=f"Hey {defender.mention}, {interaction.user.mention} is attacking you!")

        if check_defender and len(check_defender) > 0:
            await message.delete()
            return await presets.send_response("error", "You can't start a battle if"
                                                        " the defender is already inside a one.", interaction, True)

        res = await presets.make_api_request("battle", "POST", {
            "id": str(message.id),
            "attacker_id": attacker_id,
            "defender_id": defender_id,
            "attacker_countryballs": "[]",
            "defender_countryballs": "[]",
            "channel_id": interaction.channel.id,
        })

        if not res:
            await message.delete()
            return await presets.send_response("error", "There was an error while starting your battle...", interaction,
                                               True)

        return await presets.send_response("success", "Battle has been started!", interaction, True)

    @group.command(name='add', description="Add a chosen countryball to your roster!")
    @app_commands.describe(
        countryball_id="Select a coutryball you wish to use.",
    )
    async def battle_add(self, interaction: discord.Interaction, countryball_id: int):
        await presets.send_response("loading", "Gathering your fellow Countryball allies...", interaction)
        user_id = str(interaction.user.id)

        await presets.check_user(interaction.user)

        check = await presets.make_api_request("battle", "GET", {
            "where": [
                [
                    "attacker_id",
                    user_id,
                ],
                [
                    "status",
                    "<=",
                    1,
                ]
            ],
            "orWhere": [
                [
                    "defender_id",
                    user_id
                ],
                [
                    "status",
                    "<=",
                    2,
                ]
            ]
        })
        if not check or len(check) < 1:
            return await presets.send_response("error", "You are not in any battle at the moment!", interaction, True)

        countryball = await presets.make_api_request(f"countryball/{countryball_id}", "GET")
        if not countryball:
            return await presets.send_response("error", "Countryball couldn't have been found.", interaction,
                                               True)

        is_attacker = check[-1]['attacker_id'] == user_id
        cb_data = check[-1]['attacker_countryballs'] if is_attacker else check[-1][
            'defender_countryballs']
        new_countryballs = json.loads(cb_data) if cb_data else []
        new_countryballs.append(countryball['id'])
        body = {}
        if is_attacker:
            body = {"attacker_countryballs": new_countryballs}
        else:
            body = {"defender_countryballs": new_countryballs}

        res = await presets.make_api_request(f"battle/{check[-1]['id']}", "POST", body)

        if not res:
            return await presets.send_response("error", "There was an error while changing your lineup...", interaction,
                                               True)

        attacker = self.client.get_user(int(check[-1]['attacker_id']))
        defender = self.client.get_user(int(check[-1]['defender_id']))

        attacker_countryballs = new_countryballs if is_attacker else json.loads(check[-1]['attacker_countryballs'])
        defender_countryballs = new_countryballs if not is_attacker else json.loads(check[-1]['defender_countryballs'])

        channel_id = int(check[-1]['channel_id'])
        message_id = int(check[-1]['id'])
        channel = self.client.get_channel(channel_id)
        message = await channel.fetch_message(message_id)

        await message.edit(embed=await make_battle_embed(
            attacker=attacker,
            defender=defender,
            attacker_countryballs=attacker_countryballs,
            defender_countryballs=defender_countryballs,
        ), content=f"Hey {defender.mention}, {attacker.mention} is attacking you!")

        return await presets.send_response("success", "Battle lineup has been changed!", interaction, True)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Battle(client))
