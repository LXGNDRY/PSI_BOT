"""
Icon generator — produces SVG icon assets.
"""
from __future__ import annotations

from typing import Dict

from ..components.snippets.icon_system import ICONS, generate_icon_svg, generate_sprite


class IconGenerator:
    """Generates icon assets."""

    def generate(self) -> Dict[str, str]:
        files: Dict[str, str] = {}
        # Individual SVGs for use in snippets (though we use sprite approach)
        for name in ICONS:
            svg = generate_icon_svg(name)
            files[f"assets/icon-{name}.svg"] = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">{svg}</svg>\n'

        # SVG sprite
        files["assets/icon-sprite.svg"] = generate_sprite()
        return files
