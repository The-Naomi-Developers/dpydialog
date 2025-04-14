from typing import Any, Awaitable, Callable, List, Optional, Union

import discord

from ..components.select import DSelect
from ..components.user_select import DUserSelect
from ..components.role_select import DRoleSelect
from ...errors import ValidationError
from ...data import StageAction, StageComponents
from ...interfaces.icomponent import IComponent
from ...interfaces.istage import IStage


CallbackType = Callable[[discord.Interaction, Any], Awaitable[None]]
ValidationCallbackType = Callable[[Any], bool]


class Stage(IStage):
    """A class representing a stage in a dialog system.

    This class implements the IStage interface and manages a collection of components,
    content, and callbacks for a single dialog stage.

    Args:
        keyname (str): Unique identifier for the stage
        components (List[IComponent]): List of UI components for this stage
        content (Optional[str], optional): Text content to display. Defaults to None.
        embeds (Optional[List[discord.Embed]], optional): List of embeds to display. Defaults to [].
        validation_func (ValidationCallbackType, optional): Function to validate stage input. Defaults to None.
        timeout (float, optional): Timeout duration in seconds. Defaults to 180.0.

    Methods:
        set_back_callback(callback: CallbackType) -> None:
            Sets the callback function for when user navigates back.

        set_close_callback(callback: CallbackType) -> None:
            Sets the callback function for when dialog is closed.

        set_next_callback(callback: CallbackType) -> None:
            Sets the callback function for when user proceeds to next stage.

        get_keyname() -> str:
            Returns the stage's unique identifier.

        get_components() -> StageComponents:
            Returns a StageComponents object containing all UI elements.

    Raises:
        ValidationError: When validation of stage input fails.
    """

    def __init__(
        self,
        keyname: str,
        components: List[IComponent],
        content: Optional[str] = None,
        embeds: Optional[List[discord.Embed]] = [],
        validation_func: ValidationCallbackType = None,
        timeout: float = 180.0,
    ):
        self._keyname = keyname
        self._content = content
        self._embeds = embeds

        self._timeout = timeout

        self._components: List[IComponent] = components

        self._validation_func = validation_func

        self._back_callback: CallbackType = None
        self._next_callback: CallbackType = None
        self._close_callback: CallbackType = None

    def set_back_callback(self, callback: CallbackType) -> None:
        self._back_callback = callback

    def set_close_callback(self, callback: CallbackType) -> None:
        self._close_callback = callback

    def set_next_callback(self, callback: CallbackType) -> None:
        self._next_callback = callback

    async def _process_select_component(
        self,
        interaction: discord.Interaction,
        select: Union[DRoleSelect, DSelect, DUserSelect],
    ) -> None:
        value = select.values
        if callable(self._validation_func):
            if self._validation_func(value):
                await self._next_callback(interaction, value)
            else:
                raise ValidationError(
                    f"The '{self._keyname}' stage result validation not passed.",
                    stage_keyname=self._keyname,
                )
        await self._next_callback(interaction, value)

    def get_keyname(self) -> str:
        return self._keyname

    def _process_components_actions(self) -> None:
        for component in self._components:
            action = component.get_action()
            if isinstance(action, StageAction):
                if action == StageAction.BACK:
                    component._replace_function(self._back_callback)
                if action == StageAction.CLOSE:
                    component._replace_function(self._close_callback)
                if action == StageAction.NEXT:
                    component._replace_function(self._process_select_component)

    def get_components(self) -> StageComponents:
        self._process_components_actions()
        view = discord.ui.View(timeout=self._timeout)

        for component in self._components:
            view.add_item(component)

        return StageComponents(content=self._content, embeds=self._embeds, view=view)
