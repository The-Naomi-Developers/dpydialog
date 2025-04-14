from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable

import discord

from ..data import StageComponents

CallbackType = Callable[[discord.Interaction, Any], Awaitable[None]]


class IStage(ABC):
    @abstractmethod
    def get_components(self) -> StageComponents: ...

    @abstractmethod
    def get_keyname(self) -> str: ...

    @abstractmethod
    def set_next_callback(self, callback: CallbackType) -> None: ...

    @abstractmethod
    def set_back_callback(self, callback: CallbackType) -> None: ...

    @abstractmethod
    def set_close_callback(self, callback: CallbackType) -> None: ...
