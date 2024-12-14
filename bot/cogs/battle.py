import discord
from discord import app_commands
from discord.ext import commands

from bot import presets


class BattleStart(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name='battle start', description="Attack a chosen user with your countryballs!")
    @app_commands.describe(
        user="Select a user you wish to attack.",
    )
    async def battle_start(self, interaction: discord.Interaction, defender: discord.User):
        attacker_id = str(interaction.user.id)
        defender_id = str(defender.id)

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
            await presets.send_response("error", "You can't start a battle if"
                                                 " you are already inside a one.", interaction)

        res = await presets.make_api_request("battle", "POST", {
            "attacker_id": attacker_id,
            "defender_id": defender_id,
            "attacker_countryballs": "{}",
            "defender_countryballs": "{}",
            "channel_id": interaction.channel.id,
        })

        if not res:
            return presets.send_response("success", "Battle has been started!", interaction)

        return presets.send_response("error", "There was an error while starting your battle...", interaction)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(BattleStart(client))
