"""
Wearix Collection Showcase — three alternating collection blocks (Men / Women / Kids).

Wearix pattern:
- Alternating left/right image + text blocks
- Each block is a collection link
- "Pricing starts from" pricing info
- Large portrait images, soft text side
"""
from __future__ import annotations

from ...core.section import Section, SectionPreset, SectionRegistry
from ...core.setting import (
    Text, ImagePicker, Collection, Url, Header,
)
from ...core.block import Block


COLLECTION_SHOWCASE_BLOCK = Block(
    type="collection_showcase",
    name="Collection",
    settings=[
        Text("eyebrow", label="Eyebrow", default="COLLECTION"),
        Text("title", label="Title", default="Men"),
        Text("subtitle", label="Subtitle", default="Essential pieces for him"),
        Text("price_text", label="Pricing text", default="Pricing starts from $49"),
        Text("button_text", label="Button text", default="Shop collection"),
        ImagePicker("image", label="Image"),
        Collection("collection", label="Collection"),
        Url("link", label="Custom link (optional)"),
    ],
)


class WearixCollectionShowcaseSection(Section):
    type = "wearix-collection-showcase"
    name = "Wearix collection showcase"
    tag = "section"
    class_name = "wearix-collection-showcase"

    settings = [
        Header("Section"),
        Text("section_heading", label="Section heading", default=""),
        Text("section_subheading", label="Section subheading", default=""),
    ]

    blocks = [COLLECTION_SHOWCASE_BLOCK]
    max_blocks = 6

    presets = [
        SectionPreset(
            name="Collection showcase",
            settings={},
            blocks=[
                {"type": "collection_showcase",
                 "settings": {"eyebrow": "MEN'S COLLECTION", "title": "For Him",
                              "subtitle": "Essential pieces built for everyday.",
                              "price_text": "Pricing starts from $49",
                              "button_text": "Shop Men's"}},
                {"type": "collection_showcase",
                 "settings": {"eyebrow": "WOMEN'S COLLECTION", "title": "For Her",
                              "subtitle": "Effortless style, premium quality.",
                              "price_text": "Pricing starts from $39",
                              "button_text": "Shop Women's"}},
                {"type": "collection_showcase",
                 "settings": {"eyebrow": "KIDS COLLECTION", "title": "For Kids",
                              "subtitle": "Comfort first, always.",
                              "price_text": "Pricing starts from $29",
                              "button_text": "Shop Kids"}},
            ],
        ),
    ]

    styles = """
.wearix-collection-showcase__header {
    text-align: center;
    margin-bottom: 48px;
}

.wearix-collection-showcase__heading {
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 500;
    letter-spacing: -0.02em;
    margin: 0 0 16px 0;
}

.wearix-collection-showcase__subheading {
    font-size: 18px;
    color: #707070;
    max-width: 600px;
    margin: 0 auto;
}

.wearix-collection-item {
    display: grid;
    grid-template-columns: 1fr 1fr;
    min-height: 500px;
}

.wearix-collection-item + .wearix-collection-item {
    margin-top: 2px;
}

.wearix-collection-item__image {
    position: relative;
    overflow: hidden;
}

.wearix-collection-item__image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.8s ease;
}

.wearix-collection-item:hover .wearix-collection-item__image img {
    transform: scale(1.03);
}

.wearix-collection-item__text {
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 64px;
    background: #f7f7f7;
}

.wearix-collection-item--reverse .wearix-collection-item__image { order: 2; }
.wearix-collection-item--reverse .wearix-collection-item__text { order: 1; }

.wearix-collection-item__eyebrow {
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #707070;
    margin-bottom: 16px;
}

.wearix-collection-item__title {
    font-size: clamp(1.75rem, 3.5vw, 2.5rem);
    font-weight: 500;
    letter-spacing: -0.02em;
    margin: 0 0 12px 0;
}

.wearix-collection-item__subtitle {
    font-size: 16px;
    color: #707070;
    margin: 0 0 24px 0;
}

.wearix-collection-item__price {
    font-size: 14px;
    color: #707070;
    margin-bottom: 32px;
}

.wearix-collection-item__cta {
    display: inline-block;
    font-size: 14px;
    font-weight: 500;
    text-decoration: none;
    color: #000;
    border-bottom: 1px solid #000;
    padding-bottom: 2px;
    transition: all 0.2s ease;
    align-self: flex-start;
}

.wearix-collection-item__cta:hover {
    opacity: 0.6;
}

@media (max-width: 768px) {
    .wearix-collection-item {
        grid-template-columns: 1fr;
        min-height: auto;
    }
    .wearix-collection-item__image {
        min-height: 350px;
    }
    .wearix-collection-item__text {
        padding: 40px 24px;
    }
    .wearix-collection-item--reverse .wearix-collection-item__image { order: 0; }
    .wearix-collection-item--reverse .wearix-collection-item__text { order: 1; }
}
"""

    def render(self, settings, blocks):
        header = ""
        if settings.get("section_heading") or settings.get("section_subheading"):
            heading_html = (
                f'<h2 class="wearix-collection-showcase__heading">{{{{ section.settings.section_heading | escape }}}}</h2>'
                if settings.get("section_heading") else ""
            )
            subheading_html = (
                f'<p class="wearix-collection-showcase__subheading">{{{{ section.settings.section_subheading | escape }}}}</p>'
                if settings.get("section_subheading") else ""
            )
            header = f'''
  <div class="wearix-collection-showcase__header container">
    {heading_html}
    {subheading_html}
  </div>
'''

        return f'''
<section class="wearix-collection-showcase">
  {header}
  <div class="wearix-collection-showcase__list">
    {{% for block in section.blocks %}}
      <div class="wearix-collection-item {{{{ "wearix-collection-item--reverse" if forloop.index0 % 2 == 1 else "" }}}}">
        <div class="wearix-collection-item__image">
          {{% if block.settings.image != blank %}}
            <img src="{{{{ block.settings.image | img_url: '1200x' }}}}"
                 alt="{{{{ block.settings.title | escape }}}}"
                 loading="lazy" width="1200" height="1600">
          {{% endif %}}
        </div>
        <div class="wearix-collection-item__text">
          {{% if block.settings.eyebrow != blank %}}
            <span class="wearix-collection-item__eyebrow">{{{{ block.settings.eyebrow | escape }}}}</span>
          {{% endif %}}
          {{% if block.settings.title != blank %}}
            <h3 class="wearix-collection-item__title">{{{{ block.settings.title | escape }}}}</h3>
          {{% endif %}}
          {{% if block.settings.subtitle != blank %}}
            <p class="wearix-collection-item__subtitle">{{{{ block.settings.subtitle | escape }}}}</p>
          {{% endif %}}
          {{% if block.settings.price_text != blank %}}
            <p class="wearix-collection-item__price">{{{{ block.settings.price_text | escape }}}}</p>
          {{% endif %}}
          {{% if block.settings.button_text != blank %}}
            <a href="{{{{ block.settings.link | default: block.settings.collection.url }}}}" class="wearix-collection-item__cta">
              {{{{ block.settings.button_text | escape }}}}
            </a>
          {{% endif %}}
        </div>
      </div>
    {{% endfor %}}
  </div>
</section>
'''


SectionRegistry.register(WearixCollectionShowcaseSection)
