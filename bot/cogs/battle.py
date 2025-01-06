import json
from typing import List

import discord
from discord import app_commands
from discord.ext import commands

from bot import presets
from bot.presets import make_battle_embed


async def countryball_autocomplete(
        interaction: discord.Interaction,
        current: str,
) -> List[app_commands.Choice[str]]:
    countryballs_list = await presets.make_api_request(
        f"userBalls/{interaction.user.id}{'/' + current if current else ''}") or []
    return [
        app_commands.Choice(name=presets.format_countryball_string(option), value=str(option["id"]))
        for option in countryballs_list
    ]


class Battle(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    group = app_commands.Group(name="battle", description="Attack a chosen user with your countryballs!")

    @group.command(name='add', description="Add a chosen countryball to your roster!")
    @app_commands.describe(
        countryball_id="Select a countryball you wish to deploy to the battlefield.",
    )
    @app_commands.autocomplete(countryball_id=countryball_autocomplete)
    # @discord.app_commands.checks.cooldown(1, 10, key=lambda i: (i.channel_id, i.user.id))
    async def battle_add(self, interaction: discord.Interaction, countryball_id: str):
        await presets.send_response("loading", "Gathering your fellow Countryball allies...", interaction)
        countryball_id = int(countryball_id)
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

        countryball = await presets.make_api_request(f"dropped/{countryball_id}", "GET")
        if not countryball:
            return await presets.send_response("error", "Countryball couldn't have been found.", interaction,
                                               True)

        is_attacker = check[-1]['attacker_id'] == user_id
        cb_data = check[-1]['attacker_countryballs'] if is_attacker else check[-1][
            'defender_countryballs']
        new_countryballs = json.loads(cb_data) if cb_data else []
        if countryball['id'] in new_countryballs:
            return await presets.send_response("error",
                                               "You can't attach the same countryball to the same battle twice.",
                                               interaction, True)
        new_countryballs.append(countryball['id'])
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

        channel_id = int(check[-1]['channel_id'])
        message_id = int(check[-1]['id'])
        channel = self.client.get_channel(channel_id)
        message = await channel.fetch_message(message_id)

        await message.edit(embed=await make_battle_embed(
            attacker=attacker,
            defender=defender,
            battle_id=message.id
        ), content=f"Hey {defender.mention}, {attacker.mention} is attacking you!",
                           view=presets.LockInDialog(self.client))

        return await presets.send_response("success", "Battle lineup has been changed!", interaction, True)

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

        message = await interaction.channel.send("Preparing a battle...")

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

        message = await message.edit(
            embed=await make_battle_embed(attacker=interaction.user, defender=defender, battle_id=message.id),
            content=f"Hey {defender.mention}, {interaction.user.mention} is attacking you!",
            view=presets.LockInDialog(self.client))

        if not res:
            await message.delete()
            return await presets.send_response("error", "There was an error while starting your battle...", interaction,
                                               True)

        return await presets.send_response("success", "Battle has been started!", interaction, True)

    async def on_tree_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            cooldown = round(error.retry_after / 60)
            time = "minutes"
            if cooldown > 60:
                cooldown = round(cooldown / 60)
                time = "hours"
            await interaction.response.send_message(
                f"You are currently on cooldown, you can reuse this command in {cooldown} {time}!", ephemeral=True)
        else:
            print(error)
            await interaction.response.send_message("There was an error, please retry the command! :slight_smile:",
                                                    ephemeral=True)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Battle(client))
