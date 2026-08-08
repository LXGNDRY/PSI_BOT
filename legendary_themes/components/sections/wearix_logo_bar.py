"""
Wearix Logo Bar — row of brand/press logos.
"""
from __future__ import annotations

from ...core.section import Section, SectionPreset, SectionRegistry
from ...core.setting import (
    Text, ImagePicker, Header, Checkbox,
)
from ...core.block import Block


LOGO_BLOCK = Block(
    type="logo",
    name="Logo",
    settings=[
        ImagePicker("image", label="Logo image"),
        Text("alt", label="Alt text", default="Brand logo"),
    ],
)


class WearixLogoBarSection(Section):
    type = "wearix-logo-bar"
    name = "Wearix logo bar"
    tag = "section"
    class_name = "wearix-logo-bar"

    settings = [
        Header("Section"),
        Text("heading", label="Heading", default="As featured in"),
        Checkbox("grayscale", label="Grayscale logos", default=True),
    ]

    blocks = [LOGO_BLOCK]
    max_blocks = 12

    presets = [
        SectionPreset(
            name="Logo bar",
            settings={
                "heading": "As featured in",
                "grayscale": True,
            },
            blocks=[
                {"type": "logo", "settings": {"alt": "Brand 1"}},
                {"type": "logo", "settings": {"alt": "Brand 2"}},
                {"type": "logo", "settings": {"alt": "Brand 3"}},
                {"type": "logo", "settings": {"alt": "Brand 4"}},
                {"type": "logo", "settings": {"alt": "Brand 5"}},
                {"type": "logo", "settings": {"alt": "Brand 6"}},
            ],
        ),
    ]

    styles = """
.wearix-logo-bar {
    padding: 48px 24px;
    text-align: center;
    border-top: 1px solid #e5e5e5;
    border-bottom: 1px solid #e5e5e5;
}

.wearix-logo-bar__heading {
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #707070;
    margin: 0 0 32px 0;
}

.wearix-logo-bar__grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 32px;
    align-items: center;
    max-width: 1000px;
    margin: 0 auto;
}

.wearix-logo-bar__logo {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 40px;
    opacity: 0.6;
    filter: grayscale(100%);
    transition: opacity 0.2s ease, filter 0.2s ease;
}

.wearix-logo-bar--color .wearix-logo-bar__logo {
    filter: none;
    opacity: 1;
}

.wearix-logo-bar__logo:hover {
    opacity: 1;
    filter: none;
}

.wearix-logo-bar__logo img {
    max-height: 100%;
    max-width: 100%;
    object-fit: contain;
}

@media (max-width: 768px) {
    .wearix-logo-bar__grid {
        grid-template-columns: repeat(3, 1fr);
        gap: 24px;
    }
    .wearix-logo-bar__logo {
        height: 32px;
    }
}

@media (max-width: 480px) {
    .wearix-logo-bar__grid {
        grid-template-columns: repeat(2, 1fr);
    }
}
"""

    def render(self, settings, blocks):
        grayscale = "" if not settings.get("grayscale") else ""
        color = " wearix-logo-bar--color" if not settings.get("grayscale") else ""
        return f'''
<section class="wearix-logo-bar{color}">
  <div class="container">
    {{% if section.settings.heading != blank %}}
      <p class="wearix-logo-bar__heading">{{{{ section.settings.heading | escape }}}}</p>
    {{% endif %}}
    <div class="wearix-logo-bar__grid">
      {{% for block in section.blocks %}}
        <div class="wearix-logo-bar__logo">
          {{% if block.settings.image != blank %}}
            <img src="{{{{ block.settings.image | img_url: '300x' }}}}"
                 alt="{{{{ block.settings.alt | escape }}}}"
                 loading="lazy" width="150" height="40">
          {{% else %}}
            <span style="font-size: 18px; font-weight: 600; color: #999;">LOGO</span>
          {{% endif %}}
        </div>
      {{% endfor %}}
    </div>
  </div>
</section>
'''


SectionRegistry.register(WearixLogoBarSection)
