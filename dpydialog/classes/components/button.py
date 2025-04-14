from typing import Any, Awaitable, Callable, Dict, Optional, Union

import discord

from .component import BaseComponent
from ...data import StageAction


CallbackType = Callable[[discord.Interaction, "DButton"], Awaitable[None]]


class DButton(BaseComponent, discord.ui.Button):
    """A Button component class that extends both BaseComponent and discord.ui.Button.

    This class extends both BaseComponent and discord.ui.Button to create a customizable button
    that can be used within Stage-based UIs. It supports both direct callback functions and
    StageAction objects for handling interactions.

    Args:
        style (discord.ButtonStyle, optional): The style of the button. Defaults to ButtonStyle.secondary.
        label (str, optional): The text label of the button. Defaults to None.
        custom_id (str, optional): A developer-defined custom ID. Defaults to None.
        disabled (bool, optional): Whether the button is disabled. Defaults to False.
        url (str, optional): URL for link buttons. Defaults to None.
        emoji (Union[str, discord.Emoji, discord.PartialEmoji], optional): Button emoji. Defaults to None.
        row (int, optional): The row this button belongs to. Defaults to None.
        sku_id (int, optional): SKU ID for the button. Defaults to None.
        action (Union[StageAction, CallbackType], optional): The action to execute when clicked. Defaults to None.
        extras (Dict[str, Any], optional): Additional data to store with the button. Defaults to None.

    Raises:
        ValueError: When attempting to use a StageAction outside of a Stage class context.
    """

    def __init__(
        self,
        style: discord.ButtonStyle = discord.ButtonStyle.secondary,
        label: Optional[str] = None,
        custom_id: Optional[str] = None,
        disabled: bool = False,
        url: Optional[str] = None,
        emoji: Optional[Union[str, discord.Emoji, discord.PartialEmoji]] = None,
        row: Optional[int] = None,
        sku_id: Optional[int] = None,
        action: Optional[Union[StageAction, CallbackType]] = None,
        extras: Optional[Dict[str, Any]] = None,
    ):
        self._action = action
        self._extras = extras

        super().__init__(
            style=style,
            label=label,
            disabled=disabled,
            custom_id=custom_id,
            url=url,
            emoji=emoji,
            row=row,
            sku_id=sku_id,
        )

    def get_action(self) -> Union[StageAction, CallbackType]:
        return self._action

    def _replace_function(self, function: CallbackType):
        self._action = function

    async def callback(self, interaction: discord.Interaction) -> None:
        if callable(self._action):
            await self._action(interaction, self)
        else:
            raise ValueError(
                f"You should not use the {self._action.__class__.__name__} as "
                "`action` outside of the Stage-class."
            )
