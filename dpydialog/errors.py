from typing import Optional


class DialogException(Exception):
    """The base class of the DPyDialogue library."""
    def __init__(self, *args, stage_keyname: str = None):
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

class DialogHasNoStages(DialogException):
    """Raised when a `Dialog` is sent without `Stage` classes."""

class ValidationError(DialogException):
    """Raised when the validation function response isn't `True`."""
