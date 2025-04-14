from typing import Any, Dict, Optional

from ...interfaces.icomponent import IComponent


class BaseComponent(IComponent):
    _extras: Optional[Dict[str, Any]] = None

    def get_extras(self) -> Optional[Dict[str, Any]]:
        return self._extras

    def set_extras(self, extras: Dict[str, Any]) -> None:
        self._extras = extras
