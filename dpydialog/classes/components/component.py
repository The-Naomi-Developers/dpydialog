from typing import Any, Awaitable, Callable, Dict, Optional, Sequence

import discord

from ...interfaces.icomponent import IComponent


class BaseComponent(IComponent):
    _extras: Optional[Dict[str, Any]] = None
    _parent_keyname: Optional[str] = None
    _operator_ids: Optional[Sequence[int]] = None
    _on_error: Callable[[discord.Interaction, Any], Awaitable[None]] = None

    def get_extras(self) -> Optional[Dict[str, Any]]:
        return self._extras

    def set_extras(self, extras: Dict[str, Any]) -> None:
        self._extras = extras

    def _set_keyname(self, keyname: str) -> None:
        self._parent_keyname = keyname

    def get_keyname(self) -> Optional[str]:
        return self._parent_keyname

    def set_operator_ids(self, ids: Sequence[int]) -> None:
        self._operator_ids = ids

    def get_operator_ids(self) -> Optional[Sequence[int]]:
        return self._operator_ids

    def set_error_callback(
        self, callback: Callable[[discord.Interaction, Any], Awaitable[None]]
    ) -> None:
        self._on_error = callback
