"""
Footer Section Group — footer section group.

Shopify OS 2.0 requires footer to be a section group.
"""
from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from ...core.section import Section, SectionRegistry

if TYPE_CHECKING:
    from ...core.manifest import ThemeManifest


class FooterGroupSection(Section):
    type = "footer-group"
    name = "Footer group"
    tag = "footer"
    class_name = "footer-group"
    is_group = True
    limit = 1
    available_on = []

    settings = []
    blocks = []
    presets = []

    group_type = "footer"
    default_sections = [
        {"id": "footer", "type": "footer", "settings": {}},
    ]

    @classmethod
    def _render_group_json(cls, manifest: Optional["ThemeManifest"] = None) -> str:
        import json
        # Use manifest override if provided
        if manifest and manifest.footer_group_sections:
            sections_list = manifest.footer_group_sections
        elif manifest and manifest.footer_section_type != "footer":
            sections_list = [
                {"id": "footer", "type": manifest.footer_section_type, "settings": {}},
            ]
        else:
            sections_list = cls.default_sections

        sections = {}
        order = []
        for s in sections_list:
            sections[s["id"]] = {"type": s["type"], "settings": s.get("settings", {})}
            order.append(s["id"])
        group = {
            "type": "footer-group",
            "name": cls.name,
            "sections": sections,
            "order": order,
        }
        return json.dumps(group, indent=2) + "\n"

    @classmethod
    def render_liquid(cls, manifest=None) -> str:
        if cls.is_group:
            return cls._render_group_json(manifest)
        return super().render_liquid(manifest)


SectionRegistry.register(FooterGroupSection)
