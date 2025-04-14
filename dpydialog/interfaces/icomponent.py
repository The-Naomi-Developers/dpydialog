from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable, Dict, Union

import discord

from ..data import StageAction

CallbackType = Callable[[discord.Interaction, Any], Awaitable[None]]
ActionType = Union[StageAction, CallbackType]


class IComponent(ABC):
    @abstractmethod
    def get_extras(self) -> Dict[str, Any]: ...

    @abstractmethod
    def set_extras(self, extras: Dict[str, Any]) -> None: ...

    @abstractmethod
    def get_action(self) -> ActionType: ...

    @abstractmethod
    def _replace_function(self, function: CallbackType): ...
