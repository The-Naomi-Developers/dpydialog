from typing import Any, Dict, Optional, Sequence

from ...interfaces.icomponent import IComponent


class BaseComponent(IComponent):
    _extras: Optional[Dict[str, Any]] = None
    _parent_keyname: Optional[str] = None
    _operator_ids: Optional[Sequence[int]] = None

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
