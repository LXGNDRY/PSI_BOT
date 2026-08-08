# Section Authoring Guide

This guide explains how to add new sections to the Legendary Theme Generator.

## Overview

A section is a self-contained, configurable module that appears in the Shopify Theme Editor. Each section is defined as a single Python class. The engine automatically produces its Liquid file, schema, CSS, and JS.

## Anatomy of a section

```python
from ..core.section import Section, SectionPreset, SectionRegistry
from ..core.setting import Text, Header, ImagePicker, Checkbox
from ..core.block import Block

class ExampleSection(Section):
    type = "example-section"          # Unique ID, used in JSON templates
    name = "Example section"          # Human name shown in Theme Editor
    tag = "section"                   # HTML wrapper tag (section / div / header / footer)
    class_name = "example-section"    # CSS class for the wrapper
    limit = 1                         # Optional: max instances per page
    available_on = []                 # Optional: restrict to certain templates

    # Schema settings (the sidebar controls in Theme Editor)
    settings = [
        Header("Content"),
        Text("heading", label="Heading", default="Hello"),
        ImagePicker("image", label="Image"),
        Checkbox("show_button", label="Show button", default=True),
    ]

    # Block types this section supports
    blocks = []  # Or [MyBlock, AnotherBlock]

    # Default presets shown in the Theme Editor "Add section" picker
    presets = [
        SectionPreset(
            name="Example section",
            settings={"heading": "Hello world"},
            blocks=[],
        ),
    ]

    # CSS for this section (written to the section file or component CSS)
    styles = """
    .example-section {
        padding: var(--space-section) 0;
    }
    """

    # JS for this section (optional — progressive enhancement)
    scripts = """
    document.querySelectorAll('.example-section').forEach(el => {
        // progressive enhancement here
    });
    """

    def render(self, settings, blocks) -> str:
        """Return the Liquid markup for this section."""
        return '''
<div class="example-section__inner">
    {%- if section.settings.heading != blank -%}
        <h2 class="example-section__heading">{{ section.settings.heading | escape }}</h2>
    {%- endif -%}

    {%- if section.settings.image != blank -%}
        <div class="example-section__image">
            {{ section.settings.image | img_url: '1500x' | img_tag }}
        </div>
    {%- endif -%}
</div>
        '''
```

## Setting types

All Shopify setting types are supported. Here are the most commonly used:

### Text settings

```python
Text("heading", label="Heading", default="Hello")
TextArea("description", label="Description", default="")
RichText("body", label="Body text", default="<p>Hello</p>")
```

### Numeric settings

```python
Number("items_per_row", label="Items per row", default=4)
Range("opacity", label="Opacity", min=0, max=100, step=1, default=50, unit="%")
```

### Boolean settings

```python
Checkbox("show_badge", label="Show badge", default=True)
```

### Selection settings

```python
Select("layout", label="Layout",
       options=[SelectOption("left", "Left"), SelectOption("right", "Right")],
       default="left")

Radio("alignment", label="Alignment",
      options=[RadioOption("left", "Left"), RadioOption("center", "Center")],
      default="center")
```

### Color settings

```python
Color("text_color", label="Text color", default="#000000")
ColorBackground("bg_color", label="Background color", default="#ffffff")
```

### Media settings

```python
ImagePicker("image", label="Image")
ImagePicker("logo", label="Logo", info="Recommended: 200x60px")
VideoUrl("video_url", label="Video URL")
File("file", label="File")
```

### Link and navigation settings

```python
Url("link", label="Link")
LinkList("menu", label="Menu", default="main-menu")
```

### Content reference settings

```python
Product("featured_product", label="Featured product")
Collection("featured_collection", label="Featured collection")
Page("page", label="Page")
Blog("blog", label="Blog")
Article("article", label="Article")
```

### Typography settings

```python
FontPicker("heading_font", label="Heading font", default="Inter")
```

### Section organization

```python
Header("Content")        # Group header
Paragraph("info_text")   # Info text (non-interactive)
```

## Blocks

Blocks are reorderable content units inside sections. Define a block class:

```python
class TextBlock(Block):
    type = "text"
    name = "Text"

    settings = [
        Text("heading", label="Heading", default=""),
        RichText("body", label="Body", default=""),
    ]

    def render(self, block, index) -> str:
        return '''
<div class="text-block">
    {%- if block.settings.heading != blank -%}
        <h3>{{ block.settings.heading | escape }}</h3>
    {%- endif -%}
    {{ block.settings.body }}
</div>
        '''
```

Then include it in your section's `blocks` list:

```python
blocks = [TextBlock, ImageBlock, ButtonBlock]
```

### App blocks

All content sections should support app blocks. Add the `AppBlock` to your blocks list:

```python
from ..core.block import AppBlock

blocks = [TextBlock, AppBlock]
```

App blocks are automatically included with `{% for block in section.blocks %}` loops.

## Best practices

### Liquid

1. **Always escape user content.** Use `| escape` for text, `| img_url | img_tag` for images.
2. **Use `{%- -%}` for whitespace control.** Prefer strip tags to keep output clean.
3. **Always check for blank values.** `{%- if section.settings.heading != blank -%}`
4. **Use `{% render %}` not `{% include %}`.** The latter is deprecated.
5. **No hardcoded strings.** All user-facing text uses the `| t` filter.
6. **Use semantic HTML.** `<header>`, `<nav>`, `<main>`, `<article>`, `<footer>`.

### CSS

1. **Use design tokens.** Never hardcode colors, spacing, or font sizes.
2. **BEM-ish naming.** `.section-name__element--modifier`
3. **Mobile first.** Default styles are mobile, override at `min-width` breakpoints.
4. **Respect `prefers-reduced-motion`.** Wrap all animations/transitions.
5. **No `!important`.** Cascade layers eliminate the need.

### JavaScript

1. **Progressive enhancement.** The component must work without JS.
2. **Use the event bus.** `window.LTG.EventBus.subscribe/publish` for cross-component communication.
3. **Lazy hydrate.** Add `data-component="your-component"` to the root element. The observer will call your init function.
4. **Clean up.** Provide a `destroy()` method that removes listeners and observers.
5. **No framework dependencies.** Vanilla JS only.

### Accessibility

1. **All interactive elements must be focusable.** Buttons, links, inputs — not divs with click handlers.
2. **Icon-only buttons need `aria-label`.**
3. **Images need `alt` text.** Decorative images get empty alt (`alt=""`).
4. **Modals need focus trapping.**
5. **Form fields need `<label>`** — never placeholder-only.
6. **Skip link is always present.** Don't remove it.

## Testing your section

1. Add your section file to `components/sections/`
2. Add it to a manifest (or use `examples/streetwear.yaml` as a base)
3. Generate: `legendary generate my-manifest.yaml -o /tmp/test-theme`
4. Upload to a Shopify development store and test in the Theme Editor
5. Verify:
   - The section appears in the "Add section" menu
   - All settings work and update the preview
   - Blocks can be added, reordered, and deleted
   - App blocks appear in the block picker
   - It looks correct on mobile and desktop
   - It works with JavaScript disabled

## Common patterns

### Section with background image + text overlay

```python
def render(self, settings, blocks):
    return '''
<div class="image-banner__content">
    {%- if section.settings.heading != blank -%}
        <h2 class="image-banner__heading">{{ section.settings.heading | escape }}</h2>
    {%- endif -%}
</div>
    '''

styles = """
.image-banner {
    position: relative;
    min-height: 60vh;
    display: grid;
    place-items: center;
}
.image-banner::before {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(to bottom, rgba(0,0,0,0.3), rgba(0,0,0,0.6));
}
"""
```

### Responsive grid

```python
styles = """
.product-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--grid-gutter);
}
@media (min-width: 768px) {
    .product-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}
@media (min-width: 1024px) {
    .product-grid {
        grid-template-columns: repeat(4, 1fr);
    }
}
"""
```

### Lazy-loaded image with placeholder

```python
def render(self, settings, blocks):
    return '''
<div class="media-wrapper" style="padding-bottom: {{ 100 | divided_by: section.settings.image.aspect_ratio }}%">
    <img
        src="{{ section.settings.image | img_url: '500x' }}"
        alt="{{ section.settings.image.alt | escape }}"
        loading="lazy"
        width="{{ section.settings.image.width }}"
        height="{{ section.settings.image.height }}"
    >
</div>
    '''
```
