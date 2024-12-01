import discord
from discord.ext import commands
from discord import app_commands
import presets


class Propose(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name='propose', description="Creates a Council Proposal for MPs to vote!")
    @app_commands.choices(voting_type=[
        app_commands.Choice(name="⚖️ Legislation", value="legislation"),
        app_commands.Choice(name="🔵 Amendment", value="amendment"),
        app_commands.Choice(name="📜 Impeachment", value="impeachment"),
        app_commands.Choice(name="⚠️ Confidence Vote", value="confidence_vote"),
        app_commands.Choice(name="🛑 Decree", value="decree"),
        app_commands.Choice(name="🗳️ Other", value="other"),
    ])
    async def propose(self, interaction: discord.Interaction, title: str, description: str,
                               voting_type: app_commands.Choice[str]):
        eligible = await presets.is_eligible(interaction.user, interaction.guild, "councillor")

        if not eligible:
            await interaction.response.send_message(ephemeral=True, content="❌ You are not a Councillor of this server.")
            return

        await presets.create_new_voting(self.client, title, description, interaction.user, interaction.guild,
                                        voting_type.value, "voting")
        await interaction.response.send_message("✅ Proposal successfully posted!")


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Propose(client))
