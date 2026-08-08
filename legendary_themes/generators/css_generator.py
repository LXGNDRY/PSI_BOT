"""
CSS generator — produces base.css and component CSS files
from the manifest and snippet registry.
"""
from __future__ import annotations

import json
from typing import TYPE_CHECKING, Dict, List

from ..core.snippet import SnippetRegistry

if TYPE_CHECKING:
    from ..core.manifest import ThemeManifest


class CSSGenerator:
    """Generates all CSS asset files."""

    def __init__(self, manifest: "ThemeManifest"):
        self.manifest = manifest
        self.preset = manifest.presets[manifest.default_preset]

    def generate(self) -> Dict[str, str]:
        """Generate all CSS files. Returns dict of path -> content."""
        files: Dict[str, str] = {}
        files["assets/base.css"] = self._base_css()

        # Collect component CSS from snippets
        component_css: Dict[str, str] = {}
        for name, snippet in SnippetRegistry.all().items():
            if snippet.styles:
                if name.startswith("icon-"):
                    continue
                key = name.replace("_", "-")
                if key not in component_css:
                    component_css[key] = snippet.styles
                else:
                    component_css[key] += "\n\n" + snippet.styles

        for name, styles in component_css.items():
            files[f"assets/component-{name}.css"] = styles + "\n"

        # Icon system
        from ..components.snippets.icon_system import icon_system_style
        files["assets/component-icons.css"] = icon_system_style + "\n"

        return files

    def _base_css(self) -> str:
        """Generate base.css with reset, tokens, typography, utilities."""
        p = self.preset
        return f"""/* ============================================
   Base styles — {self.manifest.name}
   ============================================ */

@layer reset, tokens, base, utilities;

@layer reset {{
  *, *::before, *::after {{
    box-sizing: border-box;
  }}

  * {{
    margin: 0;
    padding: 0;
  }}

  html {{
    -webkit-text-size-adjust: 100%;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    scroll-behavior: smooth;
  }}

  body {{
    line-height: 1.5;
    -webkit-font-smoothing: antialiased;
  }}

  img, picture, video, canvas, svg {{
    display: block;
    max-width: 100%;
    height: auto;
  }}

  input, button, textarea, select {{
    font: inherit;
    color: inherit;
  }}

  button {{
    cursor: pointer;
    background: none;
    border: none;
  }}

  p, h1, h2, h3, h4, h5, h6 {{
    overflow-wrap: break-word;
  }}

  ul, ol {{
    list-style: none;
  }}

  a {{
    text-decoration: none;
    color: inherit;
  }}

  #MainContent {{
    min-height: 40vh;
  }}
}}

@layer tokens {{
  :root {{
    --color-primary: {p.palette.primary};
    --color-secondary: {p.palette.secondary};
    --color-accent: {p.palette.accent};
    --color-background: {p.palette.background};
    --color-surface: {p.palette.surface};
    --color-text: {p.palette.text};
    --color-text-muted: {p.palette.text_muted};
    --color-border: {p.palette.border};
    --color-success: {p.palette.success or '#10b981'};
    --color-error: {p.palette.error or '#ef4444'};
    --color-warning: {p.palette.warning or '#f59e0b'};

    --font-heading-family: {{ settings.heading_font.family }}, system-ui, sans-serif;
    --font-body-family: {{ settings.body_font.family }}, system-ui, sans-serif;
    --font-size-base: {p.typography.base_font_size}px;
    --line-height-body: {p.typography.body_line_height};
    --heading-scale: {p.typography.heading_scale};

    --spacing-unit: {p.spacing.base_unit}px;
    --radius-sm: calc(var(--spacing-unit) * 2);
    --spacing-md: calc(var(--spacing-unit) * 4);
    --spacing-lg: calc(var(--spacing-unit) * 8);
    --spacing-xl: calc(var(--spacing-unit) * 12);

    --radius-sm: 4px;
    --radius-md: 8px;
    --radius-lg: 12px;
    --radius-full: 9999px;

    --max-width: {p.spacing.section_padding and 1440}px;
    --grid-gap: {p.spacing.grid_gap}px;

    --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);

    --transition-fast: 0.15s ease;
    --transition-base: 0.25s ease;
    --transition-slow: 0.4s ease;
  }}
}}

@layer base {{
  body {{
    font-family: var(--font-body-family);
    font-size: var(--font-size-base);
    line-height: var(--line-height-body);
    color: var(--color-text);
    background: var(--color-background);
  }}

  h1, h2, h3, h4, h5, h6 {{
    font-family: var(--font-heading-family);
    font-weight: 600;
    line-height: 1.2;
    color: var(--color-text);
  }}

  h1 {{ font-size: calc(var(--font-size-base) * var(--heading-scale) * var(--heading-scale) * var(--heading-scale)); }}
  h2 {{ font-size: calc(var(--font-size-base) * var(--heading-scale) * var(--heading-scale)); }}
  h3 {{ font-size: calc(var(--font-size-base) * var(--heading-scale)); }}
  h4 {{ font-size: var(--font-size-base); }}

  a {{
    color: var(--color-accent);
  }}

  a:hover {{
    text-decoration: underline;
  }}

  ::selection {{
    background: var(--color-accent);
    color: var(--color-background);
  }}

  :focus-visible {{
    outline: 2px solid var(--color-accent);
    outline-offset: 2px;
    border-radius: 2px;
  }}
}}

@layer utilities {{
  .visually-hidden {{
    position: absolute !important;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }}

  .skip-link {{
    position: absolute;
    top: -100%;
    left: 1rem;
    z-index: 1000;
    padding: 1rem 1.5rem;
    background: var(--color-primary);
    color: var(--color-surface);
    font-weight: 600;
    border-radius: var(--radius-md);
    transition: top 0.2s ease;
  }}

  .skip-link:focus {{
    top: 1rem;
  }}

  .text-left {{ text-align: left; }}
  .text-center {{ text-align: center; }}
  .text-right {{ text-align: right; }}

  .page-width {{
    max-width: var(--max-width);
    margin: 0 auto;
    padding: 0 1.5rem;
  }}

  @media (prefers-reduced-motion: reduce) {{
    *, *::before, *::after {{
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
      scroll-behavior: auto !important;
    }}
  }}
}}
"""
