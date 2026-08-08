"""
Section system — the core building block of Shopify OS 2.0 themes.
Each section is a self-contained module with markup, schema, styles, and scripts.
"""
from __future__ import annotations

from typing import List, Optional, Dict, Any, TYPE_CHECKING
from dataclasses import dataclass, field

from .setting import Setting, SettingList, Header, Text
from .block import Block, APP_BLOCK

if TYPE_CHECKING:
    from ..core.manifest import ThemeManifest


# ---------------------------------------------------------------------------
# Preset class
# ---------------------------------------------------------------------------

@dataclass
class SectionPreset:
    """A default preset for a section (appears in Theme Editor "Add section" list)."""
    name: str
    settings: Dict[str, Any] = field(default_factory=dict)
    blocks: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "settings": self.settings,
            "blocks": self.blocks,
        }


# ---------------------------------------------------------------------------
# Base Section class
# ---------------------------------------------------------------------------

class Section:
    """
    Base class for all sections.
    Subclass to define a new section type.
    """

    # Class-level metadata
    type: str = ""  # section filename (without .liquid)
    name: str = ""  # display name in Theme Editor
    tag: str = "section"  # HTML tag wrapping the section
    class_name: str = ""  # CSS class prefix
    limit: Optional[int] = None  # max instances per page
    max_blocks: Optional[int] = None

    # Which templates this section can be added to
    available_on: List[str] = field(default_factory=lambda: [
        "index", "collection", "product", "page", "blog", "article",
        "search", "404", "list-collections", "cart",
    ])

    # Schema definitions
    settings: SettingList = []
    blocks: List[Block] = []
    presets: List[SectionPreset] = []

    # Content
    template: str = ""  # Liquid markup (Jinja2 template that generates .liquid)
    styles: str = ""  # CSS for this section
    scripts: str = ""  # JS for this section

    # Whether this is a section group (JSON only, no liquid)
    is_group: bool = False

    @classmethod
    def type_name(cls) -> str:
        return cls.type or cls.__name__.lower().replace("section", "").replace("section", "")

    @classmethod
    def schema_dict(cls) -> Dict[str, Any]:
        """Generate the section's {% schema %} JSON."""
        s: Dict[str, Any] = {
            "name": cls.name or cls.type_name().title(),
            "tag": cls.tag,
            "class": cls.class_name or cls.type_name(),
        }
        if cls.limit:
            s["limit"] = cls.limit

        if cls.settings:
            s["settings"] = [
                st.to_dict() for st in cls.settings
                if st.id or isinstance(st, Header)
            ]

        if cls.blocks:
            s["blocks"] = [b.to_dict() for b in cls.blocks]

        if cls.presets:
            s["presets"] = [p.to_dict() for p in cls.presets]

        return s

    @classmethod
    def render_liquid(cls, manifest: Optional["ThemeManifest"] = None) -> str:
        """Render the full .liquid file for this section."""
        if cls.is_group:
            return cls._render_group_json(manifest)

        lines = []
        # Schema tag
        import json
        schema_json = json.dumps(cls.schema_dict(), indent=2)
        lines.append("{% schema %}")
        lines.append(schema_json)
        lines.append("{% endschema %}")
        lines.append("")

        # Stylesheet tag
        if cls.styles:
            lines.append("{% stylesheet %}")
            lines.append(cls.styles.strip())
            lines.append("{% endstylesheet %}")
            lines.append("")

        # Javascript tag
        if cls.scripts:
            lines.append("{% javascript %}")
            lines.append(cls.scripts.strip())
            lines.append("{% endjavascript %}")
            lines.append("")

        # Markup
        if cls.template:
            lines.append(cls.template.strip())
            lines.append("")
        elif hasattr(cls, 'render'):
            # If class has a render method, call it with empty settings/blocks
            # to get the base template (settings/blocks are Liquid variables anyway)
            try:
                markup = cls.render(cls, {}, [])
                if markup:
                    lines.append(markup.strip())
                    lines.append("")
            except Exception:
                pass

        return "\n".join(lines)

    @classmethod
    def _render_group_json(cls) -> str:
        """Render a section group JSON file."""
        import json
        group = {
            "type": "header-group" if "header" in cls.type_name() else "footer-group",
            "name": cls.name,
            "sections": {},
            "order": [],
        }
        # Add default sections for the group
        if "header" in cls.type_name():
            group["sections"] = {
                "announcement-bar": {"type": "announcement-bar", "settings": {}},
                "header": {"type": "header", "settings": {}},
            }
            group["order"] = ["announcement-bar", "header"]
        else:
            group["sections"] = {
                "footer": {"type": "footer", "settings": {}},
            }
            group["order"] = ["footer"]
        return json.dumps(group, indent=2)


# ---------------------------------------------------------------------------
# Section registry
# ---------------------------------------------------------------------------

class SectionRegistry:
    """Global registry of all available section types."""
    _sections: Dict[str, type] = {}

    @classmethod
    def register(cls, section_cls: type) -> type:
        """Decorator to register a section class."""
        name = section_cls.type or section_cls.__name__.lower().replace("section", "")
        cls._sections[name] = section_cls
        return section_cls

    @classmethod
    def get(cls, name: str) -> Optional[type]:
        return cls._sections.get(name)

    @classmethod
    def all(cls) -> Dict[str, type]:
        return dict(cls._sections)

    @classmethod
    def names(cls) -> List[str]:
        return list(cls._sections.keys())
