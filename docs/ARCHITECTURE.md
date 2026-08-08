# Architecture

This document describes the internal architecture of the Legendary Theme Generator.

## Design principles

1. **Manifest is the single source of truth.** Every output file is derived from the manifest. No configuration lives in the engine itself.
2. **Registry pattern.** Sections, blocks, and snippets are auto-discovered via decorator-based registries. Adding a new component = adding one file.
3. **Strict separation of concerns.** Templates compose, sections configure, blocks reorder, snippets present, generators emit. Nothing does two jobs.
4. **Generation-time enforcement.** Rules that can be checked statically are checked at generation time, not left for runtime or Theme Store review.
5. **Structural uniqueness.** Output themes must never look Dawn-derived. Section architecture, CSS naming, and JS patterns are all intentionally different.
6. **Progressive enhancement.** The core browsing and purchasing flow works without JavaScript. JS only adds enhancements.

## Pipeline

```
┌─────────────────────────────┐
│  1. Manifest Validation     │  Pydantic schema + rules engine
│                             │  (type checks, constraint checks,
│                             │   Theme Store rule set)
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  2. Component Loading       │  Import all section/block/snippet
│                             │  modules to trigger registration
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  3. Template Composition    │  Build JSON templates from the
│                             │  manifest's section list + presets
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  4. Asset Generation        │  CSS, JS, icons, locales, schemas
│                             │  all produced from manifest data
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  5. Static Audit            │  50+ checks across 8 categories
│                             │  (bundle size, a11y, Liquid quality)
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  6. Output                  │  Write to disk, optional zip
└─────────────────────────────┘
```

## Core modules

### `core/manifest.py` — Theme manifest

Pydantic model that represents the entire theme specification. Top-level fields:

- `name`, `version`, `author`, `vertical`
- `presets` — dict of preset name → ThemePreset (palette, typography, spacing, layout)
- `default_preset` — which preset is active by default
- `features` — feature toggles (cart style, search style, mega menu, etc.)
- `performance` — performance budgets and flags
- `accessibility` — accessibility feature toggles
- `sections` — optional list of sections to include (defaults to all)

The manifest is validated on load. Invalid manifests (wrong types, missing fields, broken references) are rejected before any generation happens.

### `core/setting.py` — Setting type system

25+ setting types, each with:
- A `name` and `label`
- A `default` value
- Type-specific options (min/max for ranges, options for selects, info for headers)
- A `to_schema()` method that outputs the Shopify JSON schema format

Setting types: `Text`, `TextArea`, `Number`, `Range`, `Checkbox`, `Select`, `Radio`, `Color`, `ColorBackground`, `ImagePicker`, `FontPicker`, `Url`, `LinkList`, `Header`, `Paragraph`, `RichText`, `Collection`, `Product`, `Page`, `Blog`, `Article`, `File`, `VideoUrl`, `TextAlignment`

### `core/section.py` — Section base + registry

A section is the largest configurable unit in Shopify. Each section:
- Has a `type`, `name`, `tag`, `class_name`, and optional `limit`
- Declares `settings` (list of Setting objects)
- Declares `blocks` (list of Block subclasses)
- Declares `presets` (default configurations for the Theme Editor)
- Has a `render()` method that returns Liquid markup
- Optionally has `styles` (CSS) and `scripts` (JS)

The `SectionRegistry` is a module-level dict that holds all loaded sections. Importing a section module auto-registers it via the class inheritance mechanism (subclassing `Section` auto-registers).

### `core/block.py` — Block base + registry

Blocks are reorderable content units inside sections. They work just like sections but are nested. Special block types:
- `@app` — the app block slot (always included in content sections)
- `custom_liquid` — merchant-editable Liquid inside a block

### `core/snippet.py` — Snippet base + registry

Snippets are pure presentational Liquid components with no schema. They're the reusable UI building blocks. Each snippet:
- Has a `name`
- Has a `render()` method that returns Liquid markup
- Optionally has `styles` (CSS) and `scripts` (JS)

Snippets are always `{% render %}`-ed, never `{% include %}`-ed (the latter is deprecated).

### `core/template.py` — Template composer

Takes the manifest's section list and produces JSON templates. Each template is a dict with:
- `sections` — section id → { type, settings, blocks }
- `order` — array of section ids in render order

Special templates:
- `index.json` — homepage, merchant-reorderable
- `product.json` — product page with main-product + recommendations
- `collection.json` — collection with product grid + sort + filter
- `cart.json` — cart page
- `password.json` — password page (section-group enabled)
- 404, search, blog, article, list-collections, page, page.contact, gift_card

### `core/rules.py` — Theme Store compliance engine

30+ rules that validate a theme against Shopify Theme Store requirements. Each rule has:
- A code (e.g., `TS001`)
- A severity (error / warning)
- A human-readable message
- A check function that takes the manifest + composer output

Error-level rules block generation. Warning-level rules are surfaced but don't block.

### `core/composer.py` — Pipeline orchestrator

Orchestrates the full generation pipeline. Produces a `files` dict of path → content. Also runs post-generation validation.

Public API: `ThemeComposer(manifest).compose() -> Dict[str, str]`

### `core/pipeline.py` — Public entry point

The single function `generate_theme(manifest, output_dir, run_audit=True, run_theme_check=False, zip=False)` that ties everything together.

## Generators

Each generator produces a specific category of output file:

| Generator | Output |
|---|---|
| `liquid_generator.py` | Section Liquid files (markup + schema) |
| `schema_generator.py` | `settings_schema.json`, `settings_data.json` |
| `css_generator.py` | `base.css`, per-component CSS files |
| `js_generator.py` | `global.js`, per-component JS modules |
| `icon_generator.py` | SVG icon files + SVG sprite |
| `locale_generator.py` | `en.default.json` with all translation keys |

All generators are pure functions of the manifest + registries. No side effects.

## Audit system

### Static audit (`audit/static_audit.py`)

Runs 50+ checks in 8 categories:

1. **File structure** — required files present, no extra files
2. **JSON validity** — all JSON files parse correctly
3. **Bundle size** — CSS/JS budget enforcement
4. **Liquid quality** — no deprecated tags, no hardcoded URLs, proper render
5. **Accessibility basics** — skip link, alt tags, semantic landmarks
6. **Performance basics** — lazy loading, preconnect, image dimensions
7. **Hardcoded strings** — all user-facing text uses `t` filter
8. **Theme Store rules** — app blocks, section groups, required templates

### Theme Check (`audit/theme_check.py`)

Optional integration with Shopify's official `theme check` CLI. Runs if available on PATH, skips gracefully if not.

## CSS architecture

### Cascade Layers

```css
@layer reset, tokens, base, utilities, components;
```

Layers guarantee that component CSS can never accidentally override utility or base styles without an explicit layer bump.

### Design tokens

All visual values are CSS custom properties defined at `:root`, derived from the manifest preset. Tokens are namespaced:

```css
--color-bg: ...;
--color-fg: ...;
--color-accent: ...;
--font-heading: ...;
--font-body: ...;
--space-section: ...;
--radius-sm: ...;
```

### Component CSS

Each component gets its own CSS file (e.g., `component-card-product.css`). Components are loaded by the section that needs them, either in the section's Liquid (`{% stylesheet %}` tag) or via the section CSS output.

## JS architecture

### Lazy hydration

Nothing runs on page load. Each component has a `data-component` attribute. The global `hydrate()` function uses an IntersectionObserver to initialize components only when they enter the viewport.

### Event bus

A tiny pub/sub system (`window.LTG.EventBus`) lets components communicate without tight coupling:

```javascript
window.LTG.EventBus.publish('cart:updated', { count: 3 });
window.LTG.EventBus.subscribe('cart:updated', (data) => { ... });
```

### Module pattern

Each component is a factory function that takes an element and returns a controller with `init()` and `destroy()` methods. No classes, no inheritance.

## Extending the engine

### Adding a section

1. Create `components/sections/my_section.py`
2. Subclass `Section`
3. Define settings, blocks, presets, and render()
4. It's auto-registered — no other changes needed

### Adding a setting type

1. Add a class in `core/setting.py`
2. Implement `to_schema()` that returns the Shopify JSON format
3. Use it in any section

### Adding a vertical preset pack

1. Create `examples/{vertical}.yaml`
2. Define palette, typography, spacing, and feature set
3. Test with `legendary generate examples/{vertical}.yaml -o /tmp/test`

## Data flow

```
manifest.yaml
    │
    ▼
ThemeManifest (Pydantic model)
    │
    ├───→ SettingsSchemaGenerator ──→ settings_schema.json
    ├───→ CSSGenerator ─────────────→ base.css + component-*.css
    ├───→ JSGenerator ──────────────→ global.js + component-*.js
    ├───→ LocaleGenerator ──────────→ en.default.json
    ├───→ IconGenerator ────────────→ icon-*.svg + sprite.svg
    │
    └───→ ThemeComposer
              │
              ├── loads SectionRegistry, BlockRegistry, SnippetRegistry
              ├── builds Template objects from manifest sections
              ├── generates section Liquid + schema via LiquidGenerator
              ├── produces layout/theme.liquid
              └── runs StaticAudit + optional ThemeCheck
                        │
                        ▼
                   output/ theme files
```
