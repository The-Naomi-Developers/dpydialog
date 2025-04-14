from dataclasses import dataclass
from enum import Enum
from typing import Collection, Optional

import discord


@dataclass
class StageComponents:
    content: str
    embeds: Collection[discord.Embed]
    view: discord.ui.View

class StageAction(Enum):
    BACK = 0
    ENTER_MANUALLY = 1
    NEXT = 2
    CLOSE = 3

@dataclass
class ModalOption:
    varname: str
    label: str
    style: discord.TextStyle = discord.TextStyle.short
    placeholder: Optional[str] = None
    default: Optional[str] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    required: bool = True
    row: Optional[int] = None

    def to_dict(self):
        return {
            'label': self.label,
            'style': self.style,
            'placeholder': self.placeholder,
            'default': self.default,
            'min_length': self.min_length,
            'max_length': self.max_length,
            'required': self.required,
            'row': self.row
        }
