from typing import Any, Awaitable, Callable, Dict, List, Optional, Sequence

import discord
from discord.ext import commands
from discord.abc import MISSING

from ..errors import DialogException, DialogHasNoStages

from ..data import StageComponents
from .controller import DialogController
from ..interfaces.istage import IStage


class Dialog:
    def __init__(self, controller: DialogController):
        self._on_success: Callable[
            [discord.Interaction, Dict[str, Any]], Awaitable[None]
        ] = None
        self._on_error: Callable[
            [discord.Interaction, DialogException], Awaitable[None]
        ] = None

        self._controller = controller

        self._stages: List[IStage] = []
        self._result: Dict[str, Any] = {}
        self._current_stage_index = 0
        self._operator_ids: Optional[Sequence[int]] = None

    @classmethod
    def from_interaction(cls, interaction: discord.Interaction) -> "Dialog":
        return cls(DialogController(interaction))

    @classmethod
    def from_legacy_ctx(cls, ctx: commands.Context) -> "Dialog":
        raise NotImplementedError("This method requires an Interaction Adapter.")

    def set_operator_ids(self, ids: Sequence[int]) -> "Dialog":
        self._operator_ids = ids

    def set_success_callback(
        self, function: Callable[[discord.Interaction, Dict[str, Any]], Awaitable[None]]
    ) -> "Dialog":
        self._on_success = function

    def set_error_callback(
        self,
        function: Callable[[discord.Interaction, DialogException], Awaitable[None]],
    ) -> "Dialog":
        self._on_error = function

    def add_stage(self, stage: IStage) -> "Dialog":
        if not isinstance(stage, IStage):
            raise ValueError("Stage class must derive from `IStage`.")

        stage.set_operator_ids(self._operator_ids)
        stage.set_back_callback(self._to_previous_stage)
        stage.set_next_callback(self._to_next_stage)
        stage.set_close_callback(self._close_dialogue)

        self._stages.append(stage)
        return self

    async def _to_previous_stage(self, interaction: discord.Interaction, _):
        self._current_stage_index -= 1

        # Can not allow the user to move back from first page, so just close the dialogue
        if self._current_stage_index < 0:
            return await self._close_dialogue(interaction, _)

        components: StageComponents = self._stages[
            self._current_stage_index
        ].get_components()

        await self._controller.render(interaction, components)

    async def _close_dialogue(self, interaction: discord.Interaction, _):
        await self._controller.close(interaction)

    async def _to_next_stage(self, interaction: discord.Interaction, value: Any):
        # Saving the result of the Stage
        current_stage = self._stages[self._current_stage_index]
        self._result[current_stage.get_keyname()] = value

        self._current_stage_index += 1

        # If the next Stage is out-of-borders, then the dialogue is completed
        if self._current_stage_index > len(self._stages) - 1:
            return await self._on_success(interaction, self._result)

        await self._render_current_stage(interaction)

    async def _render_current_stage(
        self,
        interaction: discord.Interaction,
        allowed_mentions: Optional[discord.AllowedMentions] = MISSING,
        delete_after: Optional[float] = None,
        suppress_embeds: bool = MISSING,
        files: Sequence[discord.File] = MISSING,
        ephemeral: bool = False,
    ):
        if len(self._stages) < 1:
            raise DialogHasNoStages()

        components: StageComponents = self._stages[
            self._current_stage_index
        ].get_components()

        await self._controller.render(
            interaction,
            components,
            allowed_mentions=allowed_mentions,
            delete_after=delete_after,
            suppress_embeds=suppress_embeds,
            files=files,
            ephemeral=ephemeral,
        )

    async def send(
        self,
        allowed_mentions: Optional[discord.AllowedMentions] = MISSING,
        delete_after: Optional[float] = None,
        suppress_embeds: bool = MISSING,
        files: Sequence[discord.File] = MISSING,
        ephemeral: bool = False,
    ):
        await self._render_current_stage(
            self._controller.get_interaction(),
            allowed_mentions=allowed_mentions,
            delete_after=delete_after,
            suppress_embeds=suppress_embeds,
            files=files,
            ephemeral=ephemeral,
        )
