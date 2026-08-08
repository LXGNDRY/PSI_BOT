"""
Block system — reorderable content units within sections.
"""
from __future__ import annotations

from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field

from .setting import Setting, SettingList, Header


@dataclass
class Block:
    """
    A block is a reorderable content unit inside a section.
    Merchants can add, remove, and reorder blocks in the Theme Editor.
    """
    type: str
    name: str
    settings: SettingList = field(default_factory=list)
    limit: Optional[int] = None  # max instances of this block type per section
    is_app_block: bool = False

    def to_dict(self) -> Dict[str, Any]:
        if self.is_app_block:
            return {"type": "@app"}
        d: Dict[str, Any] = {
            "type": self.type,
            "name": self.name,
            "settings": [s.to_dict() for s in self.settings if s.id or isinstance(s, Header)],
        }
        if self.limit:
            d["limit"] = self.limit
        return d

    @property
    def is_app(self) -> bool:
        return self.is_app_block or self.type == "@app"


# Built-in block types shipped with the engine

APP_BLOCK = Block(type="@app", name="App", is_app_block=True)
CUSTOM_LIQUID_BLOCK = Block(
    type="liquid",
    name="Custom Liquid",
    settings=[
        Setting(id="code", type_name="liquid", label="Custom Liquid"),
    ] if False else [],  # placeholder — actual Liquid setting defined in generator
)


def make_text_block(default_text: str = "") -> Block:
    from .setting import InlineRichText, Richtext
    return Block(
        type="text",
        name="Text",
        settings=[],
    )
