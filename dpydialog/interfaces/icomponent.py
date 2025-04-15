from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable, Dict, Optional, Sequence, Union

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

    @abstractmethod
    def _set_keyname(self, keyname: str) -> None: ...

    @abstractmethod
    def get_keyname(self) -> Optional[str]: ...

    @abstractmethod
    def set_operator_ids(self, ids: Sequence[int]) -> None: ...

    @abstractmethod
    def get_operator_ids(self) -> Optional[Sequence[int]]: ...
