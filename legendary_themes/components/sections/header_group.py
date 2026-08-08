"""
Header Section Group — bundles announcement-bar + header into a section group.

Shopify OS 2.0 requires header and footer to be section groups
(containers that hold multiple sections) so they can be placed in
the theme layout via {% section 'header-group' %}.
"""
from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from ...core.section import Section, SectionRegistry

if TYPE_CHECKING:
    from ...core.manifest import ThemeManifest


class HeaderGroupSection(Section):
    type = "header-group"
    name = "Header group"
    tag = "header"
    class_name = "header-group"
    is_group = True
    limit = 1
    available_on = []  # section group only, not addable in Theme Editor

    settings = []
    blocks = []
    presets = []

    # Group-level config
    group_type = "header"
    default_sections = [
        {"id": "announcement-bar", "type": "announcement-bar", "settings": {}},
        {"id": "header", "type": "header", "settings": {}},
    ]

    @classmethod
    def _render_group_json(cls, manifest: Optional["ThemeManifest"] = None) -> str:
        import json
        # Use manifest override if provided
        if manifest and manifest.header_group_sections:
            sections_list = manifest.header_group_sections
        elif manifest and manifest.header_section_type != "header":
            sections_list = [
                {"id": "announcement-bar", "type": "announcement-bar", "settings": {}},
                {"id": "header", "type": manifest.header_section_type, "settings": {}},
            ]
        else:
            sections_list = cls.default_sections

        sections = {}
        order = []
        for s in sections_list:
            sections[s["id"]] = {"type": s["type"], "settings": s.get("settings", {})}
            order.append(s["id"])
        group = {
            "type": "header-group",
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


SectionRegistry.register(HeaderGroupSection)
