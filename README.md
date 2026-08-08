# Legendary Theme Generator

> Premium Shopify OS 2.0 theme engine — manifest-driven, Theme Store compliant, production-grade.

Generate complete, upload-ready Shopify themes from a single YAML manifest. Every theme is structurally unique (not Dawn-derived), passes Theme Store review criteria, and ships with best-in-class performance and accessibility baked in.

---

## Why this exists

Shopify theme development is slow and repetitive. Most agencies fork Dawn, tweak the CSS, and rebrand — which means every theme has the same architecture, the same bugs, and gets flagged by Theme Store review as a Dawn derivative.

Legendary Theme Generator builds themes from first principles:

- **Manifest-driven.** Describe your theme (vertical, palette, features, sections) in one YAML file. The engine produces every file.
- **Structurally unique.** Each theme has its own section architecture, CSS naming, and JS patterns — nothing is Dawn-derived.
- **Theme Store compliant.** Every generated theme meets all 20+ mandatory requirements (JSON templates, sections everywhere, app blocks, section groups, accessibility, progressive enhancement).
- **Zero JavaScript by default.** Browsing and purchasing work without JS. JavaScript is loaded progressively, per-component, only when elements enter the viewport.
- **Audit first.** 50+ static checks run before any file is written. Bundle budgets, accessibility rules, and Liquid anti-patterns are enforced at generation time.

---

## Features

### Core
- 10 production section types (header, footer, main-product, featured-collection, image-banner, etc.)
- 13 block types inside the main product section (title, price, description, variants, quantity, add-to-cart, SKU, vendor, share, etc.)
- App block support in all content sections
- Section group architecture (header + footer groups)
- 14 JSON templates (index, product, collection, cart, page, search, 404, blog, article, list-collections, password, gift_card, +6 customer templates)

### Design system
- CSS Cascade Layers architecture (reset → tokens → base → utilities → components)
- Manifest-driven design tokens (colors, typography, spacing, radii, shadows)
- Fully responsive with a mobile-first approach
- `prefers-reduced-motion` and `prefers-color-scheme` support
- WCAG 2.1 AA color contrast built into the palette validation

### Performance
- Total CSS: ~16 KB
- Total JS: ~11 KB
- No jQuery, no React, no framework overhead
- Vanilla JS with IntersectionObserver-based lazy hydration
- SVG icon system with sprite
- CSS-only fallback for all interactive components

### Developer experience
- YAML/JSON manifest as single source of truth
- Multiple presets per theme (e.g. Midnight, Bone)
- Plugin-style component system — add a section/block/snippet by dropping a Python file
- Full CLI with rich output
- 100% test coverage for the generation pipeline

---

## Quick start

### Install

```bash
pip install legendary-theme-generator
```

Or from source:

```bash
git clone https://github.com/LXGNDRY/Legendary_Theme_Generator.git
cd Legendary_Theme_Generator
pip install -e .
```

### Generate your first theme

```bash
legendary generate examples/streetwear.yaml -o ./my-theme
```

This produces a complete, upload-ready Shopify theme in `./my-theme/`.

### Upload to Shopify

1. Go to **Online Store → Themes → Upload theme** in your Shopify admin
2. Upload the generated directory (or zip it first with `legendary generate --zip`)
3. Preview and customize via the Theme Editor

### CLI commands

```bash
# Generate a theme from a manifest
legendary generate manifest.yaml -o ./output-dir
legendary generate manifest.yaml -o ./output-dir --zip    # also produce a .zip
legendary generate manifest.yaml -o ./output-dir --skip-audit
legendary generate manifest.yaml -o ./output-dir --theme-check  # run Shopify Theme Check

# Validate a manifest (no generation)
legendary validate manifest.yaml

# Audit an existing theme directory
legendary audit ./my-theme

# List available components
legendary list-sections
legendary list-snippets
```

---

## Manifest format

The manifest is a YAML file that describes the entire theme. Example:

```yaml
name: Axiom
version: 1.0.0
author: Legendary Branding
vertical: streetwear
default_preset: midnight

presets:
  midnight:
    label: "Midnight"
    palette:
      background: "#0a0a0a"
      foreground: "#ffffff"
      accent: "#ff3b30"
      secondary: "#8b8b8b"
      border: "#2a2a2a"
      success: "#30d158"
      warning: "#ffd60a"
      error: "#ff453a"
    typography:
      heading_font: "Inter"
      body_font: "Inter"
      base_size: "16px"
      heading_weight: "700"
      body_weight: "400"
    spacing:
      section_padding: 80
      grid_gutter: 24
    layout:
      max_width: 1440
      content_width: 1200

features:
  cart_style: drawer
  search_style: predictive
  mega_menu: false
  quick_view: false
  sticky_header: true
  breadcrumbs: true

performance:
  lazy_load_images: true
  preconnect_fonts: true
  inline_critical_css: false
  js_budget_kb: 15
  css_budget_kb: 20

accessibility:
  skip_link: true
  focus_outlines: true
  reduced_motion: true
  semantic_headings: true
  landmark_roles: true
  aria_labels: true
```

See `examples/streetwear.yaml` for a complete reference.

---

## Architecture

### The 10-phase pipeline

```
1.  Manifest Validation   →  Pydantic schema + rules engine
2.  Component Loading     →  Import sections, blocks, snippets from registry
3.  Template Composition  →  Build JSON templates from section manifests
4.  Layout Generation     →  Produce theme.liquid with SEO + meta
5.  Schema Generation     →  settings_schema.json + settings_data.json
6.  CSS Generation        →  Design tokens → base → components (layered)
7.  JS Generation         →  Global init + lazy component modules
8.  Icon + Locale Gen     →  SVG sprite + translation strings
9.  Static Audit          →  50+ checks (bundle size, a11y, Liquid quality)
10. Output / Package      →  Write files (and optional .zip)
```

### Core modules

| Module | Location | Purpose |
|---|---|---|
| Manifest | `core/manifest.py` | Pydantic-validated theme manifest |
| Settings | `core/setting.py` | 25+ Shopify setting types |
| Sections | `core/section.py` + `components/sections/` | Section base class + 10 sections |
| Blocks | `core/block.py` + `components/blocks/` | Block system with app block support |
| Snippets | `core/snippet.py` + `components/snippets/` | Presentational components |
| Templates | `core/template.py` + `components/templates/` | JSON template composer |
| Rules | `core/rules.py` | Theme Store compliance engine (30+ rules) |
| Composer | `core/composer.py` | Orchestrates the full pipeline |
| Generators | `generators/` | Liquid, CSS, JS, icon, locale, schema |
| Audit | `audit/static_audit.py` + `audit/theme_check.py` | Static analysis + Theme Check |
| CLI | `cli/main.py` | `legendary` command-line interface |

### CSS architecture

Cascade Layers keep specificity flat and predictable:

```
@layer reset, tokens, base, utilities, components;
```

- **reset** — minimal CSS reset (not normalize.css)
- **tokens** — CSS custom properties from manifest (colors, typography, spacing)
- **base** — typography, forms, links, focus states
- **utilities** — small utility classes (visually-hidden, text-truncate, container)
- **components** — per-component CSS, one file per component

### JS architecture

No framework. Vanilla JS with a tiny event bus and lazy hydration:

- `global.js` — boot script, event bus, IntersectionObserver hydrator
- `component-cart.js` — AJAX cart / drawer
- `component-menu.js` — mobile menu + desktop mega menu
- `component-variants.js` — product variant selector
- `component-quantity.js` — quantity input
- `component-search.js` — predictive search
- `component-media.js` — product gallery / media viewer

Each component is only initialized when its root element enters the viewport. Nothing runs on page load until it's needed.

### Adding a new section

Drop a Python file in `components/sections/`:

```python
from ..core.section import Section, SectionPreset, SectionRegistry
from ..core.setting import Text, ImagePicker, Header, Url

class MySection(Section):
    type = "my-section"
    name = "My section"
    tag = "section"
    class_name = "my-section"

    settings = [
        Header("Content"),
        Text("heading", label="Heading", default="Hello world"),
        ImagePicker("image", label="Background image"),
        Url("link", label="Link"),
    ]

    blocks = []
    presets = [
        SectionPreset(
            name="My section",
            settings={"heading": "Hello world"},
            blocks=[],
        ),
    ]

    def render(self, settings, blocks):
        return '''
<div class="my-section">
  <h2>{{ section.settings.heading }}</h2>
</div>
        '''
```

It's automatically registered and available in the Theme Editor.

---

## Roadmap

### v1.0 (current)
- Core engine with 10 sections
- Streetwear vertical manifest
- Static audit system
- Full CLI

### v1.1
- More sections: testimonials, FAQ, lookbook-grid, logo-wall, countdown, multi-column, video, slideshow
- Luxury + beauty vertical manifests
- Predictive search UI
- Quick view modal

### v1.2
- Faceted filtering (filter-and-search)
- AJAX cart drawer
- Mega menu builder
- Recently viewed products
- Wishlist (localStorage)

### v2.0
- Visual manifest builder (web UI)
- A/B test framework for sections
- Theme store submission kit
- Demo store generator
- AI manifest from a store URL

---

## Performance benchmarks

Target for all generated themes:

| Metric | Mobile | Desktop |
|---|---|---|
| Performance score | ≥ 85 | ≥ 95 |
| LCP | < 1.8s | < 1.0s |
| CLS | < 0.02 | < 0.01 |
| Total CSS | < 20 KB | < 20 KB |
| Total JS | < 15 KB | < 15 KB |

Current baseline (streetwear manifest):
- CSS: 16.0 KB
- JS: 11.1 KB
- Lighthouse: targeted 92/98 mobile/desktop performance

---

## Accessibility

All generated themes target **WCAG 2.1 AA**:

- Semantic HTML with proper landmark roles
- Skip-to-content link
- Visible focus outlines (never removed)
- `prefers-reduced-motion` respected for all animations
- Color contrast validated at generation time
- Keyboard-navigable menus, modals, and forms
- ARIA labels on all icon-only buttons
- Form fields with proper `label` associations
- Screen reader announcements for cart updates

---

## Development

```bash
# Clone
git clone https://github.com/LXGNDRY/Legendary_Theme_Generator.git
cd Legendary_Theme_Generator

# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=legendary_themes

# Build a test theme
legendary generate examples/streetwear.yaml -o /tmp/test-theme
```

### Project structure

```
legendary_theme_generator/
├── legendary_themes/         # The engine package
│   ├── core/                 # Foundation: manifest, sections, blocks, composer
│   ├── components/           # Sections, blocks, snippets, templates
│   ├── generators/           # Liquid, CSS, JS, icon, locale, schema generators
│   ├── audit/                # Static audit + Theme Check runner
│   └── cli/                  # Command-line interface
├── examples/                 # Example manifest files
├── tests/                    # Test suite
├── docs/                     # Architecture and API docs
└── pyproject.toml            # Package config
```

---

## License

MIT © Legendary Branding

---

## Credits

Built by the Legendary Branding engineering team. Engine design informed by 5+ years of Shopify theme development and 20+ Theme Store submissions.
