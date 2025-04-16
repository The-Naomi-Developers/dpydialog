import inspect
from typing import Any, Awaitable, Callable, Dict, List, Optional, Sequence, Union

import discord

from dpydialog.errors import (
    DialogException,
    NotAllowedToInteract,
    ShouldBeCoroutine,
    StageActionOutsideDialog,
)

from .component import BaseComponent
from ...data import StageAction

CallbackType = Callable[[discord.Interaction, "DRoleSelect"], Awaitable[None]]


class DRoleSelect(BaseComponent, discord.ui.RoleSelect):
    """A RoleSelect component class that extends both BaseComponent and discord.ui.RoleSelect.

    This class provides functionality for creating role select menus in Discord with callback actions.

    Args:
        custom_id (Optional[str], optional): The custom identifier for the select menu. Defaults to discord.utils.MISSING.
        placeholder (Optional[str], optional): Placeholder text shown when no role is selected. Defaults to None.
        min_values (int, optional): Minimum number of roles that must be selected. Defaults to 1.
        max_values (int, optional): Maximum number of roles that can be selected. Defaults to 1.
        disabled (bool, optional): Whether the select menu is disabled. Defaults to False.
        row (Optional[int], optional): The row this select menu belongs to. Defaults to None.
        default_values (Optional[Sequence[Union[discord.SelectDefaultValue, discord.Role]]], optional):
            Pre-selected roles when the menu is shown. Defaults to None.
        action (Optional[Union[StageAction, CallbackType]], optional):
            Callback function or stage action to execute when a selection is made. Defaults to None.
        extras (Optional[Dict[str, Any]], optional): Additional data to store with the component. Defaults to None.
        operator_ids: (List[int], optional):
            IDs of users allowed to use this component. If None, then everyone can use it. Default to None.

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
        default_values: Optional[
            Sequence[Union[discord.SelectDefaultValue, discord.Role]]
        ] = None,
        action: Optional[Union[StageAction, CallbackType]] = None,
        extras: Optional[Dict[str, Any]] = None,
        operator_ids: Optional[List[int]] = None,
        on_error_callback: Callable[[discord.Interaction, DialogException], Awaitable[None]] = None,
    ):
        self._action = action
        self._extras = extras
        self._operator_ids = operator_ids
        self._on_error = on_error_callback

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

    async def callback(self, interaction: discord.Interaction) -> None:
        if isinstance(self._action, StageAction):
            raise StageActionOutsideDialog(
                f"You should not use the `StageAction` as "
                "`action` outside of the `Stage` class.",
                stage_keyname=self._parent_keyname,
            )

        if not inspect.iscoroutinefunction(self._action):
            raise ShouldBeCoroutine(stage_keyname=self._parent_keyname)

        if interaction.user.id not in self._operator_ids:
            err = NotAllowedToInteract(
                "The current user is not allowed to interact with the component.",
                allowed_ids=self._operator_ids,
                user_id=interaction.user.id,
                stage_keyname=self._parent_keyname,
            )
            if self._on_error:
                await self._on_error(interaction, err)
                return
            raise err

        await self._action(interaction, self)
