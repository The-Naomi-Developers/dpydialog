from typing import Any, Awaitable, Callable, Dict, List, Optional

import discord

from .component import BaseComponent
from ...data import ModalOption


CallbackType = Callable[[discord.Interaction, discord.ui.Modal], Awaitable[None]]


class DModal(BaseComponent, discord.ui.Modal):
    """A Modal component class that extends both BaseComponent and discord.ui.Modal.

    This class represents a modal dialog in Discord that can contain text input fields and
    handle user submissions.

    Args:
        action (CallbackType): A callable that will be executed when the modal is submitted.
            The callback should accept two parameters: interaction and the modal instance.
        title (str): The title of the modal dialog.
        options (List[ModalOption]): A list of ModalOption objects defining the text input fields.
        custom_id (Optional[str], optional): A custom identifier for the modal. Defaults to discord.utils.MISSING.
        timeout (float, optional): The time in seconds before the modal times out. Defaults to 180.0.
        extras (Dict[str, Any], optional): Additional data to be stored with the modal. Defaults to None.

    Raises:
        ValueError: If the provided action is not callable.
    """

    def __init__(
        self,
        action: CallbackType,
        title: str,
        options: List[ModalOption],
        custom_id: Optional[str] = discord.utils.MISSING,
        timeout: float = 180.0,
        extras: Dict[str, Any] = None,
    ):
        self._action = action
        self._extras = extras

        if not callable(self._action):
            raise ValueError(f"The Modal component only support callable action.")

        super().__init__(title=title, timeout=timeout, custom_id=custom_id)

        for option in options:
            text_input = discord.ui.TextInput(**option.to_dict())
            setattr(self, option.varname, text_input)
            self.add_item(text_input)

    def get_action(self) -> CallbackType:
        return self._action

    def _replace_function(self, function: CallbackType) -> None:
        if not callable(self._action):
            raise ValueError(f"The Modal component only support callable action.")

        self._action = function

    async def callback(self, interaction: discord.Interaction) -> None:
        await self._action(interaction, self)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.callback(interaction)
