from typing import Optional, Sequence, Union

import discord
from discord.abc import MISSING

from ..data import StageComponents


class DialogController:
    def __init__(self, interaction: discord.Interaction) -> None:
        self._interaction = interaction
        self._message_sent = False  # True after sending the first Stage

    def get_interaction(self) -> discord.Interaction:
        return self._interaction

    async def render(
        self,
        interaction: discord.Interaction,
        components: StageComponents,
        allowed_mentions: Optional[discord.AllowedMentions] = MISSING,
        delete_after: Optional[float] = None,
        suppress_embeds: bool = False,
        files: Sequence[discord.File] = MISSING,
        ephemeral: bool = False,
    ) -> None:
        if not self._message_sent:
            await self._interaction.response.send_message(
                content=components.content,
                embeds=components.embeds,
                view=components.view,
                allowed_mentions=allowed_mentions,
                delete_after=delete_after,
                suppress_embeds=suppress_embeds,
                files=files,
                ephemeral=ephemeral,
            )
            self._message_sent = True
        else:
            await interaction.response.edit_message(
                content=components.content,
                embeds=components.embeds,
                view=components.view,
                allowed_mentions=allowed_mentions,
                delete_after=delete_after,
                suppress_embeds=suppress_embeds or MISSING,
                attachments=files,
            )

    async def close(self, interaction: discord.Interaction) -> None:
        await interaction.message.delete()
