"""
Template system — JSON templates that compose sections into pages.
"""
from __future__ import annotations

import json
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field


@dataclass
class TemplateSection:
    """A section instance inside a template."""
    id: str  # unique id within template
    type: str  # section type name
    settings: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Template:
    """
    A JSON template (OS 2.0).
    Composes sections in a specific order.
    """
    name: str  # e.g. "index", "product", "page.contact"
    sections: List[TemplateSection] = field(default_factory=list)
    order: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.order and self.sections:
            self.order = [s.id for s in self.sections]

    def to_dict(self) -> Dict[str, Any]:
        sections_dict = {}
        for s in self.sections:
            sections_dict[s.id] = {
                "type": s.type,
                "settings": s.settings,
            }
        return {
            "sections": sections_dict,
            "order": self.order,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2) + "\n"

    @property
    def filename(self) -> str:
        # Handle nested templates like page.contact
        if "." in self.name and not self.name.startswith("gift_card"):
            return f"templates/{self.name}.json"
        return f"templates/{self.name}.json"


# Standard template names required for Theme Store
REQUIRED_TEMPLATES = [
    "index",
    "product",
    "collection",
    "cart",
    "page",
    "page.contact",
    "search",
    "404",
    "blog",
    "article",
    "list-collections",
    "password",
]


class TemplateRegistry:
    """Registry of all template definitions."""
    _templates: Dict[str, Template] = {}

    @classmethod
    def register(cls, template: Template) -> Template:
        cls._templates[template.name] = template
        return template

    @classmethod
    def get(cls, name: str) -> Optional[Template]:
        return cls._templates.get(name)

    @classmethod
    def all(cls) -> Dict[str, Template]:
        return dict(cls._templates)
