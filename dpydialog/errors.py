from typing import Optional, Sequence


class DialogException(Exception):
    """The base class of the DPyDialogue library."""
    def __init__(self, *args, stage_keyname: Optional[str] = None):
        super().__init__(*args)
        self._stage_keyname: Optional[str] = stage_keyname

    def get_keyname(self) -> Optional[str]:
        return self._stage_keyname

class StageActionOutsideDialog(DialogException):
    """Raised when the component action is set to `StageAction` outside a `Dialog` class."""

class ShouldBeCoroutine(DialogException):
    """Raised when the `action` field is not a coroutine."""

class NotAllowedToInteract(DialogException):
    """Raised when a current user is not allowed to interact with the component."""
    def __init__(self, *args, allowed_ids: Sequence[int], user_id: int, stage_keyname: Optional[str] = None):
        self._stage_keyname = stage_keyname
        self._allowed_ids = allowed_ids
        self._uid = user_id
    
    def get_allowed_users(self) -> Sequence[int]:
        return self._allowed_ids

    def get_user_id(self) -> int:
        return self.uid

class DialogHasNoStages(DialogException):
    """Raised when a `Dialog` is sent without `Stage` classes."""

class ValidationError(DialogException):
    """Raised when the validation function response isn't `True`."""
