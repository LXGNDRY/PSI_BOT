# Manifest Reference

Complete reference for the YAML/JSON manifest format.

## Top-level fields

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | yes | Theme name |
| `version` | string | yes | Semantic version (e.g. "1.0.0") |
| `author` | string | yes | Author / developer name |
| `vertical` | string | yes | Vertical / industry (streetwear, luxury, beauty, etc.) |
| `default_preset` | string | yes | Name of the default preset |
| `presets` | object | yes | Dictionary of presets (name → preset object) |
| `features` | object | no | Feature configuration |
| `performance` | object | no | Performance budgets and flags |
| `accessibility` | object | no | Accessibility feature toggles |
| `sections` | array | no | Section configuration per template |

## Preset object

Each preset defines a complete visual identity.

### `palette` (required)

| Field | Type | Description |
|---|---|---|
| `background` | string (hex) | Page background color |
| `foreground` | string (hex) | Primary text color |
| `accent` | string (hex) | Accent / brand color (buttons, links) |
| `secondary` | string (hex) | Secondary text color |
| `border` | string (hex) | Border / divider color |
| `success` | string (hex) | Success state color |
| `warning` | string (hex) | Warning state color |
| `error` | string (hex) | Error state color |
| `overlay` | string (hex) | Overlay / modal background |
| `surface` | string (hex) | Card / surface background |

### `typography` (required)

| Field | Type | Default | Description |
|---|---|---|---|
| `heading_font` | string | "Inter" | Heading font family |
| `body_font` | string | "Inter" | Body font family |
| `base_size` | string | "16px" | Base font size |
| `heading_weight` | string | "700" | Heading font weight |
| `body_weight` | string | "400" | Body font weight |
| `line_height` | string | "1.5" | Body line height |
| `heading_line_height` | string | "1.2" | Heading line height |

### `spacing` (required)

| Field | Type | Default | Description |
|---|---|---|---|
| `section_padding` | number | 80 | Vertical section padding (px) |
| `grid_gutter` | number | 24 | Grid gap between items (px) |
| `container_padding` | number | 24 | Horizontal page padding (px) |
| `button_padding_x` | number | 24 | Button horizontal padding (px) |
| `button_padding_y` | number | 14 | Button vertical padding (px) |

### `layout` (required)

| Field | Type | Default | Description |
|---|---|---|---|
| `max_width` | number | 1440 | Max page width (px) |
| `content_width` | number | 1200 | Content width (px) |
| `border_radius` | number | 0 | Default border radius (px) |
| `button_radius` | number | 0 | Button border radius (px) |
| `image_radius` | number | 0 | Image border radius (px) |

### `shadows` (optional)

| Field | Type | Default | Description |
|---|---|---|---|
| `small` | string | "none" | Small shadow (CSS box-shadow value) |
| `medium` | string | "none" | Medium shadow |
| `large` | string | "none" | Large shadow |

### `motion` (optional)

| Field | Type | Default | Description |
|---|---|---|---|
| `duration_fast` | string | "150ms" | Fast transition duration |
| `duration_normal` | string | "300ms" | Normal transition duration |
| `duration_slow` | string | "500ms" | Slow transition duration |
| `ease` | string | "ease" | Default easing function |

## `features` object

| Field | Type | Default | Description |
|---|---|---|---|
| `cart_style` | string | "drawer" | Cart type: "drawer" or "page" |
| `search_style` | string | "standard" | Search: "standard" or "predictive" |
| `mega_menu` | boolean | false | Enable mega menu on desktop |
| `quick_view` | boolean | false | Enable quick view modal |
| `sticky_header` | boolean | true | Sticky header on scroll |
| `breadcrumbs` | boolean | true | Show breadcrumbs on product/collection pages |
| `product_recommendations` | boolean | true | Show product recommendations on product page |
| `recently_viewed` | boolean | false | Show recently viewed products |
| `wishlist` | boolean | false | Enable wishlist (localStorage) |
| `compare` | boolean | false | Enable product comparison |
| `reviews` | boolean | false | Enable product reviews (app-integrated) |
| `newsletter` | boolean | true | Newsletter signup in footer |
| `social_icons` | boolean | true | Social media icons in header/footer |
| `currency_selector` | boolean | true | Currency selector in header |
| `language_selector` | boolean | true | Language selector in header |
| `account_links` | boolean | true | Show account / login link |
| `announcement_bar` | boolean | true | Enable announcement bar |
| `countdown_timer` | boolean | false | Countdown timer section available |
| `image_zoom` | boolean | false | Product image zoom on hover |

## `performance` object

| Field | Type | Default | Description |
|---|---|---|---|
| `lazy_load_images` | boolean | true | Lazy load images below the fold |
| `preconnect_fonts` | boolean | true | Preconnect to font CDNs |
| `inline_critical_css` | boolean | false | Inline above-the-fold CSS |
| `defer_non_critical_css` | boolean | true | Load non-critical CSS asynchronously |
| `js_budget_kb` | number | 15 | JavaScript bundle budget (KB) |
| `css_budget_kb` | number | 20 | CSS bundle budget (KB) |
| `lcp_target_ms` | number | 1800 | LCP target (ms, mobile) |
| `cls_target` | number | 0.02 | CLS target (mobile) |
| `image_dimensions_required` | boolean | true | Require explicit image width/height |
| `min_responsive_images` | boolean | true | Generate responsive image srcsets |

## `accessibility` object

| Field | Type | Default | Description |
|---|---|---|---|
| `skip_link` | boolean | true | Skip-to-content link |
| `focus_outlines` | boolean | true | Visible focus outlines (never removed) |
| `reduced_motion` | boolean | true | Respect prefers-reduced-motion |
| `semantic_headings` | boolean | true | Enforce proper heading hierarchy |
| `landmark_roles` | boolean | true | Use semantic landmarks (header, nav, main, footer) |
| `aria_labels` | boolean | true | ARIA labels on icon-only buttons |
| `alt_text_required` | boolean | true | Require alt text on all images |
| `color_contrast_check` | boolean | true | Validate WCAG AA contrast at generation time |
| `keyboard_nav` | boolean | true | All interactive elements keyboard-accessible |
| `screen_reader_text` | boolean | true | Visually-hidden text for screen readers |
| `form_labels` | boolean | true | All form fields have proper labels |
| `error_announcements` | boolean | true | Form errors announced to screen readers |

## `sections` object (optional)

Define which sections appear on each template. If omitted, defaults are used.

```yaml
sections:
  index:
    - type: image-banner
      preset: "Hero banner"
    - type: featured-collection
      preset: "Featured products"
    - type: rich-text
      preset: "Brand story"
  product:
    - type: main-product
    - type: product-recommendations
```

Each section entry can include:
- `type` — section type ID (required)
- `preset` — which preset config to use (optional, uses default)
- `settings` — override specific settings (optional)

## Complete example

See `examples/streetwear.yaml` for a full, production-ready manifest.

## Validation rules

The manifest is validated against these rules on load:

- All required fields must be present
- Color values must be valid hex codes (3, 6, or 8 characters)
- `default_preset` must match a key in `presets`
- Preset names must be unique
- At least one preset is required
- Section types must be registered
- Feature names must be valid
- Budget values must be positive numbers
- Font names must be valid font families

Invalid manifests produce a clear error with the specific field and rule violated.
