"""
Wearix Hero Section — full-viewport hero with background image/video,
centered content, two CTA buttons, and thumbnail carousel at the bottom.

Characteristic of the Wearix Framer template:
- Full viewport height
- Dark overlay for text contrast
- Pill-shaped buttons (primary solid, secondary ghost)
- Row of thumbnail images at bottom for quick navigation
- Tag / eyebrow text above heading
"""
from __future__ import annotations

from ...core.section import Section, SectionPreset, SectionRegistry
from ...core.setting import (
    Text, ImagePicker, Select, SelectOption, Checkbox, Url, Header,
    TextAlignment, RichText, Range, Color,
)
from ...core.block import Block


class WearixHeroSection(Section):
    type = "wearix-hero"
    name = "Wearix hero"
    tag = "section"
    class_name = "wearix-hero"
    limit = 1

    settings = [
        Header("Content"),
        Text("eyebrow", label="Eyebrow text", default="NEW COLLECTION"),
        Text("heading", label="Heading", default="Premium wear for modern living"),
        RichText("subheading", label="Subheading",
                 default="<p>Effortless style. Premium quality. Pieces that define your everyday.</p>"),

        Header("Primary Button"),
        Text("primary_text", label="Button text", default="See all collections"),
        Url("primary_link", label="Button link"),

        Header("Secondary Button"),
        Text("secondary_text", label="Button text", default="Contact us"),
        Url("secondary_link", label="Button link"),

        Header("Background"),
        ImagePicker("background_image", label="Background image"),
        Select("overlay", label="Overlay style",
               options=[
                   SelectOption("none", "None"),
                   SelectOption("light", "Light"),
                   SelectOption("medium", "Medium"),
                   SelectOption("dark", "Dark"),
               ], default="dark"),
        Range("overlay_opacity", label="Overlay opacity", min=0, max=90, default=40, unit="%"),
        Checkbox("full_height", label="Full viewport height", default=True),
        TextAlignment("text_align", label="Text alignment", default="center"),

        Header("Thumbnails"),
        Checkbox("show_thumbnails", label="Show thumbnail carousel", default=True),
    ]

    blocks = []

    presets = [
        SectionPreset(
            name="Wearix hero",
            settings={
                "eyebrow": "NEW COLLECTION",
                "heading": "Premium wear for modern living",
                "primary_text": "See all collections",
                "secondary_text": "Contact us",
                "overlay": "dark",
                "overlay_opacity": 40,
                "full_height": True,
                "text_align": "center",
                "show_thumbnails": True,
            },
            blocks=[],
        ),
    ]

    styles = """
.wearix-hero {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 80vh;
    overflow: hidden;
}

.wearix-hero--full {
    min-height: 100vh;
}

.wearix-hero__bg {
    position: absolute;
    inset: 0;
    z-index: 0;
}

.wearix-hero__bg img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.wearix-hero__overlay {
    position: absolute;
    inset: 0;
    z-index: 1;
    background: rgba(0, 0, 0, 0.4);
}

.wearix-hero__overlay--none { display: none; }
.wearix-hero__overlay--light { background: rgba(0, 0, 0, 0.15); }
.wearix-hero__overlay--medium { background: rgba(0, 0, 0, 0.35); }
.wearix-hero__overlay--dark { background: rgba(0, 0, 0, 0.55); }

.wearix-hero__content {
    position: relative;
    z-index: 2;
    max-width: 800px;
    padding: 64px 24px;
    text-align: center;
    color: #fff;
}

.wearix-hero__eyebrow {
    display: inline-block;
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 24px;
    opacity: 0.9;
    padding: 6px 16px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 50px;
}

.wearix-hero__heading {
    font-size: clamp(2.5rem, 6vw, 4.5rem);
    font-weight: 500;
    line-height: 1.05;
    letter-spacing: -0.02em;
    margin: 0 0 24px 0;
}

.wearix-hero__subheading {
    font-size: 18px;
    line-height: 1.5;
    opacity: 0.9;
    margin: 0 0 40px 0;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
}

.wearix-hero__buttons {
    display: flex;
    gap: 16px;
    justify-content: center;
    flex-wrap: wrap;
}

.wearix-hero__thumbnails {
    position: absolute;
    bottom: 32px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 2;
    display: flex;
    gap: 12px;
    max-width: 90%;
    overflow-x: auto;
    padding-bottom: 4px;
}

.wearix-hero__thumb {
    width: 72px;
    height: 72px;
    flex-shrink: 0;
    border-radius: 8px;
    overflow: hidden;
    cursor: pointer;
    opacity: 0.6;
    transition: opacity 0.2s ease, transform 0.2s ease;
    border: 2px solid transparent;
}

.wearix-hero__thumb:hover,
.wearix-hero__thumb--active {
    opacity: 1;
    border-color: #fff;
}

.wearix-hero__thumb img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

@media (max-width: 768px) {
    .wearix-hero {
        min-height: 70vh;
    }
    .wearix-hero--full {
        min-height: 85vh;
    }
    .wearix-hero__heading {
        font-size: clamp(2rem, 8vw, 3rem);
    }
    .wearix-hero__subheading {
        font-size: 16px;
    }
    .wearix-hero__buttons {
        flex-direction: column;
        align-items: center;
    }
    .wearix-hero__thumbnails {
        bottom: 20px;
        gap: 8px;
    }
    .wearix-hero__thumb {
        width: 56px;
        height: 56px;
    }
}
"""

    def render(self, settings, blocks):
        full_class = " wearix-hero--full" if settings.get("full_height") else ""
        align = settings.get("text_align", "center")
        overlay = settings.get("overlay", "dark")
        return f'''
<div class="wearix-hero{full_class}">
  <div class="wearix-hero__bg">
    {{% if section.settings.background_image != blank %}}
      <img src="{{{{ section.settings.background_image | img_url: '1920x' }}}}"
           alt="{{{{ section.settings.background_image.alt | escape }}}}"
           loading="eager" width="1920" height="1080">
    {{% endif %}}
  </div>
  <div class="wearix-hero__overlay wearix-hero__overlay--{overlay}"></div>

  <div class="wearix-hero__content" style="text-align: {align}">
    {{% if section.settings.eyebrow != blank %}}
      <span class="wearix-hero__eyebrow">{{{{ section.settings.eyebrow | escape }}}}</span>
    {{% endif %}}
    {{% if section.settings.heading != blank %}}
      <h1 class="wearix-hero__heading">{{{{ section.settings.heading | escape }}}}</h1>
    {{% endif %}}
    {{% if section.settings.subheading != blank %}}
      <div class="wearix-hero__subheading">{{{{ section.settings.subheading }}}}</div>
    {{% endif %}}
    <div class="wearix-hero__buttons">
      {{% if section.settings.primary_text != blank %}}
        <a href="{{{{ section.settings.primary_link }}}}" class="btn btn--primary btn--pill">
          {{{{ section.settings.primary_text | escape }}}}
        </a>
      {{% endif %}}
      {{% if section.settings.secondary_text != blank %}}
        <a href="{{{{ section.settings.secondary_link }}}}" class="btn btn--ghost btn--pill btn--light">
          {{{{ section.settings.secondary_text | escape }}}}
        </a>
      {{% endif %}}
    </div>
  </div>

  {{% if section.settings.show_thumbnails %}}
  <div class="wearix-hero__thumbnails" role="list">
    {{% for i in (1..4) %}}
      <button type="button" class="wearix-hero__thumb {{% if i == 1 %}}wearix-hero__thumb--active{{% endif %}}"
              aria-label="Go to slide {{{{ i }}}}">
        {{% if section.settings.background_image != blank %}}
          <img src="{{{{ section.settings.background_image | img_url: '200x' }}}}" alt="" loading="lazy">
        {{% endif %}}
      </button>
    {{% endfor %}}
  </div>
  {{% endif %}}
</div>
'''


SectionRegistry.register(WearixHeroSection)
