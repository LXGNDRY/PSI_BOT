"""
Snippet system — small reusable Liquid fragments.
Snippets are pure presentational: no schema, no state, just markup + CSS.
"""
from __future__ import annotations

from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field


@dataclass
class Snippet:
    """A reusable Liquid snippet."""
    name: str
    template: str  # Liquid content
    params: List[str] = field(default_factory=list)  # expected parameter names
    styles: str = ""  # accompanying CSS (emitted into component CSS)

    def render(self) -> str:
        return self.template.strip() + "\n"

    @property
    def filename(self) -> str:
        return f"{self.name}.liquid"


class SnippetRegistry:
    """Global registry of all available snippets."""
    _snippets: Dict[str, Snippet] = {}

    @classmethod
    def register(cls, snippet: Snippet) -> Snippet:
        cls._snippets[snippet.name] = snippet
        return snippet

    @classmethod
    def get(cls, name: str) -> Optional[Snippet]:
        return cls._snippets.get(name)

    @classmethod
    def all(cls) -> Dict[str, Snippet]:
        return dict(cls._snippets)
