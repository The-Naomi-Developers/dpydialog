class DialogException(BaseException):
    """The base class of the DPyDialogue library."""
    def __init__(self, *args, stage_keyname: str):
        super().__init__(*args)
        self._stage_keyname: str = stage_keyname

    def get_keyname(self) -> str:
        return self._stage_keyname

class ValidationError(DialogException):
    """Raised when the validation function response isn't `True`."""
