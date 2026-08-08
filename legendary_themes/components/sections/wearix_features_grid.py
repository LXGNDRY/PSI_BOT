"""
Wearix Features Grid — 3x2 grid of brand value propositions.

Wearix pattern:
- "Where style meets ease" heading
- 6 feature blocks in a 3-column grid
- Each has an icon/image, title, and short description
- Minimal, clean aesthetic
"""
from __future__ import annotations

from ...core.section import Section, SectionPreset, SectionRegistry
from ...core.setting import (
    Text, ImagePicker, Header, RichText, Checkbox,
)
from ...core.block import Block


FEATURE_BLOCK = Block(
    type="feature",
    name="Feature",
    settings=[
        ImagePicker("icon", label="Icon / image"),
        Text("title", label="Title", default="Premium Quality"),
        RichText("description", label="Description",
                 default="<p>Crafted with the finest materials for lasting wear.</p>"),
    ],
)


class WearixFeaturesGridSection(Section):
    type = "wearix-features-grid"
    name = "Wearix features grid"
    tag = "section"
    class_name = "wearix-features-grid"

    settings = [
        Header("Section"),
        Text("heading", label="Heading", default="Where style meets ease"),
        Text("subheading", label="Subheading", default=""),
        Checkbox("gray_bg", label="Gray background", default=False),
    ]

    blocks = [FEATURE_BLOCK]
    max_blocks = 12

    presets = [
        SectionPreset(
            name="Features grid",
            settings={
                "heading": "Where style meets ease",
                "gray_bg": False,
            },
            blocks=[
                {"type": "feature", "settings": {"title": "Premium Quality",
                 "description": "<p>Crafted with the finest materials for lasting wear.</p>"}},
                {"type": "feature", "settings": {"title": "Free Shipping",
                 "description": "<p>Complimentary shipping on all orders over $100.</p>"}},
                {"type": "feature", "settings": {"title": "Easy Returns",
                 "description": "<p>30-day hassle-free returns, no questions asked.</p>"}},
                {"type": "feature", "settings": {"title": "Sustainable",
                 "description": "<p>Ethically sourced materials and responsible production.</p>"}},
                {"type": "feature", "settings": {"title": "Perfect Fit",
                 "description": "<p>Our fit guide helps you find the perfect size every time.</p>"}},
                {"type": "feature", "settings": {"title": "24/7 Support",
                 "description": "<p>Our team is always here to help with any questions.</p>"}},
            ],
        ),
    ]

    styles = """
.wearix-features-grid {
    padding: 120px 24px;
    background: #fff;
}

.wearix-features-grid--gray {
    background: #f7f7f7;
}

.wearix-features-grid__header {
    text-align: center;
    margin-bottom: 64px;
}

.wearix-features-grid__heading {
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 500;
    letter-spacing: -0.02em;
    margin: 0 0 16px 0;
}

.wearix-features-grid__subheading {
    font-size: 18px;
    color: #707070;
    max-width: 600px;
    margin: 0 auto;
}

.wearix-features-grid__grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 48px 32px;
    max-width: 1000px;
    margin: 0 auto;
}

.wearix-feature {
    text-align: center;
}

.wearix-feature__icon {
    width: 64px;
    height: 64px;
    margin: 0 auto 24px auto;
    display: flex;
    align-items: center;
    justify-content: center;
}

.wearix-feature__icon img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
}

.wearix-feature__title {
    font-size: 18px;
    font-weight: 500;
    margin: 0 0 12px 0;
}

.wearix-feature__description {
    font-size: 14px;
    color: #707070;
    line-height: 1.6;
    margin: 0;
}

.wearix-feature__description p {
    margin: 0;
}

@media (max-width: 768px) {
    .wearix-features-grid {
        padding: 80px 24px;
    }
    .wearix-features-grid__grid {
        grid-template-columns: 1fr 1fr;
        gap: 32px 24px;
    }
}

@media (max-width: 480px) {
    .wearix-features-grid__grid {
        grid-template-columns: 1fr;
    }
}
"""

    def render(self, settings, blocks):
        gray = " wearix-features-grid--gray" if settings.get("gray_bg") else ""
        return f'''
<section class="wearix-features-grid{gray}">
  <div class="container">
    <div class="wearix-features-grid__header">
      {{% if section.settings.heading != blank %}}
        <h2 class="wearix-features-grid__heading">{{{{ section.settings.heading | escape }}}}</h2>
      {{% endif %}}
      {{% if section.settings.subheading != blank %}}
        <p class="wearix-features-grid__subheading">{{{{ section.settings.subheading | escape }}}}</p>
      {{% endif %}}
    </div>
    <div class="wearix-features-grid__grid">
      {{% for block in section.blocks %}}
        <div class="wearix-feature">
          {{% if block.settings.icon != blank %}}
            <div class="wearix-feature__icon">
              <img src="{{{{ block.settings.icon | img_url: '200x200' }}}}"
                   alt="{{{{ block.settings.title | escape }}}}"
                   loading="lazy" width="64" height="64">
            </div>
          {{% endif %}}
          {{% if block.settings.title != blank %}}
            <h3 class="wearix-feature__title">{{{{ block.settings.title | escape }}}}</h3>
          {{% endif %}}
          {{% if block.settings.description != blank %}}
            <div class="wearix-feature__description">{{{{ block.settings.description }}}}</div>
          {{% endif %}}
        </div>
      {{% endfor %}}
    </div>
  </div>
</section>
'''


SectionRegistry.register(WearixFeaturesGridSection)
