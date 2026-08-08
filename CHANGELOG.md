# Changelog

All notable changes to the Legendary Theme Generator are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-08-08

### Added

- **Core engine**: Manifest-driven Shopify OS 2.0 theme generation pipeline
- **Manifest system**: Pydantic-validated YAML/JSON theme definition with palette, typography, spacing, features, performance budgets, and accessibility configuration
- **Setting system**: 25+ Shopify setting types (text, color, range, image_picker, font_picker, link_list, etc.)
- **Section system**: 10 production sections:
  - header (4 layout variants, sticky, search, cart, account, mobile menu)
  - footer (multi-column, newsletter, social, payment icons)
  - announcement-bar (multi-message, rotating, auto-advance)
  - main-product (block-based, 13 block types, app block support)
  - main-collection-product-grid (sort, filter, pagination, faceted-ready)
  - image-banner (hero, full-bleed, overlay, mobile-first)
  - rich-text (text alignment, content-first)
  - featured-collection (grid, carousel-ready, quick-view ready)
  - custom-liquid (merchant-editable Liquid)
  - product-recommendations (Shopify-powered)
- **Snippet library**: card-product, price, badge, button, quantity-input, pagination, breadcrumb, product-media, 40-icon SVG system
- **Templates**: 14 JSON templates (index, product, collection, cart, page, page.contact, search, 404, blog, article, list-collections, password, gift_card) + 6 customer templates
- **CSS architecture**: Cascade Layers (reset → tokens → base → utilities → components), design tokens, responsive system, reduced-motion support
- **JS architecture**: Vanilla JS with event bus, IntersectionObserver lazy hydration, 6 component modules (cart, menu, variants, quantity, search, media)
- **Generators**: Liquid, schema, CSS, JS, icon sprite, locale
- **Audit system**: 50+ static checks across 8 categories (file structure, JSON validity, bundle size, Liquid quality, accessibility, performance, hardcoded strings, Theme Store rules)
- **Theme Check integration**: Optional Shopify Theme Check runner
- **CLI**: `legendary generate`, `legendary validate`, `legendary audit`, `legendary list-sections`, `legendary list-snippets`
- **Test suite**: 10 passing tests (manifest validation + end-to-end generation)
- **Example manifests**: Streetwear vertical (Axiom theme, 2 presets)

### Design highlights

- CSS: ~16 KB, JS: ~11 KB — well under 20KB / 15KB budgets
- Zero JavaScript required for core browsing/purchasing
- WCAG 2.1 AA target: semantic HTML, skip link, focus outlines, reduced motion support
- Structurally unique from Dawn — different section architecture, CSS naming, JS patterns
- Fully OS 2.0 compliant: JSON templates, sections everywhere, section groups, app blocks, dynamic sources

### Known limitations

- Only English locale shipped (extendable via locale generator)
- 10 sections shipped (roadmap: testimonials, FAQ, lookbook, logo-wall, multi-column, video, slideshow)
- Predictive search UI, cart drawer, and faceted filtering are skeleton-only (roadmap for v1.1)
- Mega menu is setting-only (full implementation in v1.1)
