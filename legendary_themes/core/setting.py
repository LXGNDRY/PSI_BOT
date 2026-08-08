"""
Setting types — all valid Shopify Theme Editor input and sidebar settings.
Each Setting class renders to the JSON schema entry used by the Theme Editor.
"""
from __future__ import annotations

from typing import Optional, List, Any, Dict, Union
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------------

@dataclass
class Setting:
    """Base class for all settings."""
    id: str
    label: str
    default: Any = None
    info: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = {"type": self._type, "id": self.id, "label": self.label}
        if self.default is not None:
            d["default"] = self.default
        if self.info is not None:
            d["info"] = self.info
        return d

    @property
    def _type(self) -> str:
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Basic input settings
# ---------------------------------------------------------------------------

@dataclass
class Checkbox(Setting):
    default: bool = False

    @property
    def _type(self) -> str:
        return "checkbox"


@dataclass
class Text(Setting):
    default: str = ""
    placeholder: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        if self.placeholder:
            d["placeholder"] = self.placeholder
        return d

    @property
    def _type(self) -> str:
        return "text"


@dataclass
class Textarea(Setting):
    default: str = ""
    placeholder: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        if self.placeholder:
            d["placeholder"] = self.placeholder
        return d

    @property
    def _type(self) -> str:
        return "textarea"


@dataclass
class Number(Setting):
    default: Optional[float] = None
    placeholder: Optional[str] = None

    @property
    def _type(self) -> str:
        return "number"


@dataclass
class Range(Setting):
    min: float = 0
    max: float = 100
    step: float = 1
    unit: Optional[str] = None
    default: float = 0

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d["min"] = self.min
        d["max"] = self.max
        d["step"] = self.step
        if self.unit:
            d["unit"] = self.unit
        return d

    @property
    def _type(self) -> str:
        return "range"


@dataclass
class RadioOption:
    value: str
    label: str


@dataclass
class Radio(Setting):
    options: List[RadioOption] = field(default_factory=list)
    default: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d["options"] = [{"value": o.value, "label": o.label} for o in self.options]
        return d

    @property
    def _type(self) -> str:
        return "radio"


@dataclass
class SelectOption:
    value: str
    label: str
    group: Optional[str] = None


@dataclass
class Select(Setting):
    options: List[SelectOption] = field(default_factory=list)
    default: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        opts = []
        for o in self.options:
            opt = {"value": o.value, "label": o.label}
            if o.group:
                opt["group"] = o.group
            opts.append(opt)
        d["options"] = opts
        return d

    @property
    def _type(self) -> str:
        return "select"


# ---------------------------------------------------------------------------
# Specialized input settings
# ---------------------------------------------------------------------------

@dataclass
class Color(Setting):
    default: str = "#000000"
    placeholder: Optional[str] = None

    @property
    def _type(self) -> str:
        return "color"


@dataclass
class ColorBackground(Setting):
    default: str = "#ffffff"

    @property
    def _type(self) -> str:
        return "color_background"


@dataclass
class FontPicker(Setting):
    default: str = "helvetica_n4"

    @property
    def _type(self) -> str:
        return "font_picker"


@dataclass
class ImagePicker(Setting):
    default: Optional[str] = None

    @property
    def _type(self) -> str:
        return "image_picker"


@dataclass
class Url(Setting):
    default: str = ""

    @property
    def _type(self) -> str:
        return "url"


@dataclass
class RichText(Setting):
    default: str = "<p></p>"

    @property
    def _type(self) -> str:
        return "richtext"


@dataclass
class InlineRichText(Setting):
    default: str = ""

    @property
    def _type(self) -> str:
        return "inline_richtext"


@dataclass
class Html(Setting):
    default: str = ""

    @property
    def _type(self) -> str:
        return "html"


@dataclass
class Liquid(Setting):
    default: str = ""

    @property
    def _type(self) -> str:
        return "liquid"


@dataclass
class LinkList(Setting):
    default: str = "main-menu"

    @property
    def _type(self) -> str:
        return "link_list"


@dataclass
class Collection(Setting):
    @property
    def _type(self) -> str:
        return "collection"


@dataclass
class CollectionList(Setting):
    limit: int = 10

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d["limit"] = self.limit
        return d

    @property
    def _type(self) -> str:
        return "collection_list"


@dataclass
class Product(Setting):
    @property
    def _type(self) -> str:
        return "product"


@dataclass
class ProductList(Setting):
    limit: int = 10

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d["limit"] = self.limit
        return d

    @property
    def _type(self) -> str:
        return "product_list"


@dataclass
class Page(Setting):
    @property
    def _type(self) -> str:
        return "page"


@dataclass
class Article(Setting):
    @property
    def _type(self) -> str:
        return "article"


@dataclass
class Blog(Setting):
    @property
    def _type(self) -> str:
        return "blog"


@dataclass
class TextAlignment(Setting):
    default: str = "left"

    @property
    def _type(self) -> str:
        return "text_alignment"


@dataclass
class Video(Setting):
    @property
    def _type(self) -> str:
        return "video"


@dataclass
class VideoUrl(Setting):
    accept: List[str] = field(default_factory=lambda: ["youtube", "vimeo"])

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d["accept"] = self.accept
        return d

    @property
    def _type(self) -> str:
        return "video_url"


# ---------------------------------------------------------------------------
# Sidebar / non-input settings
# ---------------------------------------------------------------------------

@dataclass
class Header(Setting):
    """Section header / divider — not an input."""

    def __init__(self, content: str):
        super().__init__(id="", label="")
        self.content = content

    def to_dict(self) -> Dict[str, Any]:
        return {"type": "header", "content": self.content}

    @property
    def _type(self) -> str:
        return "header"


@dataclass
class Paragraph(Setting):
    """Info paragraph — not an input."""

    def __init__(self, content: str):
        super().__init__(id="", label="")
        self.content = content

    def to_dict(self) -> Dict[str, Any]:
        return {"type": "paragraph", "content": self.content}

    @property
    def _type(self) -> str:
        return "paragraph"


# Type alias for setting lists
SettingList = List[Union[Setting, Header, Paragraph]]
