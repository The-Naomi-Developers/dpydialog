import discord

from ..data import StageComponents


class DialogController:
    def __init__(self, interaction: discord.Interaction) -> None:
        self._interaction = interaction
        self._message_sent = False  # True after sending the first Stage

    def get_interaction(self) -> discord.Interaction:
        return self._interaction

    async def render(
        self, interaction: discord.Interaction, components: StageComponents
    ) -> None:
        if not self._message_sent:
            await self._interaction.response.send_message(
                content=components.content,
                embeds=components.embeds,
                view=components.view,
            )
            self._message_sent = True
        else:
            await interaction.response.edit_message(
                content=components.content,
                embeds=components.embeds,
                view=components.view,
            )

    async def close(self, interaction: discord.Interaction) -> None:
        await interaction.message.delete()
