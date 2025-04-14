from typing import Any, Awaitable, Callable, Dict, Optional, Sequence, Union

import discord

from .component import BaseComponent
from ...data import StageAction

CallbackType = Callable[[discord.Interaction, "DUserSelect"], Awaitable[None]]
DefaultValuesType = Sequence[
    discord.SelectDefaultValue | discord.User | discord.Member | discord.ClientUser
]


class DUserSelect(BaseComponent, discord.ui.UserSelect):
    """A UserSelect component class that extends both BaseComponent and discord.ui.UserSelect.

    This class provides functionality for creating user select menus in Discord with callback actions.

    Args:
        custom_id (Optional[str], optional): The custom identifier for the select menu. Defaults to discord.utils.MISSING.
        placeholder (Optional[str], optional): Placeholder text shown when no user is selected. Defaults to None.
        min_values (int, optional): Minimum number of users that must be selected. Defaults to 1.
        max_values (int, optional): Maximum number of users that can be selected. Defaults to 1.
        disabled (bool, optional): Whether the select menu is disabled. Defaults to False.
        row (Optional[int], optional): The row this select menu belongs to. Defaults to None.
        default_values (Optional[DefaultValuesType], optional):
            Pre-selected users when the menu is shown. Defaults to None.
        action (Optional[Union[StageAction, CallbackType]], optional):
            Callback function or stage action to execute when a selection is made. Defaults to None.
        extras (Optional[Dict[str, Any]], optional): Additional data to store with the component. Defaults to None.

    Raises:
        ValueError: If StageAction is used outside of a Stage class context.
    """

    def __init__(
        self,
        custom_id: Optional[str] = discord.utils.MISSING,
        placeholder: Optional[str] = None,
        min_values: int = 1,
        max_values: int = 1,
        disabled: bool = False,
        row: Optional[int] = None,
        default_values: Optional[DefaultValuesType] = None,
        action: Optional[Union[StageAction, CallbackType]] = None,
        extras: Optional[Dict[str, Any]] = None,
    ):
        self._action = action
        self._extras = extras

        super().__init__(
            custom_id=custom_id,
            placeholder=placeholder,
            min_values=min_values,
            max_values=max_values,
            disabled=disabled,
            row=row,
            default_values=default_values,
        )

    def get_action(self) -> Union[StageAction, CallbackType]:
        return self._action

    def _replace_function(self, function: CallbackType) -> None:
        self._action = function

    async def callback(self, interaction) -> None:
        if callable(self._action):
            await self._action(interaction, self)
        else:
            raise ValueError(
                f"You should not use the {self._action.__class__.__name__} as "
                "`action` outside of the Stage-class."
            )
