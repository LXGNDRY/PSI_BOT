"""
Wearix Instagram / Community Section — fanned-out vertical image gallery.

Wearix pattern:
- "See our community" heading
- Unique carousel / fanned layout of vertical images
- Each image is a different angle / slightly offset
- "Follow us" CTA
"""
from __future__ import annotations

from ...core.section import Section, SectionPreset, SectionRegistry
from ...core.setting import (
    Text, ImagePicker, Header, Url,
)
from ...core.block import Block


INSTAGRAM_IMAGE_BLOCK = Block(
    type="instagram_image",
    name="Instagram image",
    settings=[
        ImagePicker("image", label="Image"),
        Url("link", label="Link (optional)"),
        Text("alt", label="Alt text", default="Instagram post"),
    ],
)


class WearixInstagramSection(Section):
    type = "wearix-instagram"
    name = "Wearix instagram"
    tag = "section"
    class_name = "wearix-instagram"

    settings = [
        Header("Section"),
        Text("heading", label="Heading", default="See our community in modern silhouettes"),
        Text("subheading", label="Subheading", default=""),
        Text("handle", label="Instagram handle", default="@wearix"),
        Url("link", label="Instagram link"),
    ]

    blocks = [INSTAGRAM_IMAGE_BLOCK]
    max_blocks = 8

    presets = [
        SectionPreset(
            name="Instagram gallery",
            settings={
                "heading": "See our community in modern silhouettes",
                "handle": "@wearix",
            },
            blocks=[
                {"type": "instagram_image", "settings": {"alt": "Community look 1"}},
                {"type": "instagram_image", "settings": {"alt": "Community look 2"}},
                {"type": "instagram_image", "settings": {"alt": "Community look 3"}},
                {"type": "instagram_image", "settings": {"alt": "Community look 4"}},
                {"type": "instagram_image", "settings": {"alt": "Community look 5"}},
                {"type": "instagram_image", "settings": {"alt": "Community look 6"}},
            ],
        ),
    ]

    styles = """
.wearix-instagram {
    padding: 120px 24px;
    text-align: center;
    background: #fff;
    overflow: hidden;
}

.wearix-instagram__heading {
    font-size: clamp(1.75rem, 3.5vw, 2.5rem);
    font-weight: 500;
    letter-spacing: -0.02em;
    margin: 0 0 8px 0;
}

.wearix-instagram__handle {
    font-size: 14px;
    color: #707070;
    margin: 0 0 48px 0;
}

.wearix-instagram__handle a {
    color: #000;
    text-decoration: none;
    border-bottom: 1px solid #000;
    padding-bottom: 2px;
    font-weight: 500;
}

.wearix-instagram__grid {
    display: flex;
    gap: 16px;
    justify-content: center;
    align-items: center;
    max-width: 100%;
    margin: 0 auto;
    flex-wrap: wrap;
}

.wearix-instagram__item {
    position: relative;
    width: calc(16.66% - 14px);
    min-width: 150px;
    aspect-ratio: 3/4;
    border-radius: 12px;
    overflow: hidden;
    transition: transform 0.4s ease;
    display: block;
    text-decoration: none;
}

.wearix-instagram__item:nth-child(odd) {
    transform: translateY(-16px);
}

.wearix-instagram__item:nth-child(3n+2) {
    transform: translateY(16px);
}

.wearix-instagram__item:hover {
    transform: translateY(-8px) scale(1.02);
    z-index: 2;
}

.wearix-instagram__item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.4s ease;
}

.wearix-instagram__item:hover img {
    transform: scale(1.08);
}

.wearix-instagram__overlay {
    position: absolute;
    inset: 0;
    background: rgba(0, 0, 0, 0.3);
    opacity: 0;
    transition: opacity 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-size: 20px;
}

.wearix-instagram__item:hover .wearix-instagram__overlay {
    opacity: 1;
}

.wearix-instagram__cta {
    display: inline-block;
    margin-top: 48px;
    font-size: 14px;
    font-weight: 500;
    text-decoration: none;
    color: #000;
    border: 1px solid #000;
    padding: 12px 28px;
    border-radius: 50px;
    transition: all 0.2s ease;
}

.wearix-instagram__cta:hover {
    background: #000;
    color: #fff;
}

@media (max-width: 900px) {
    .wearix-instagram__item {
        width: calc(25% - 12px);
        min-width: 120px;
    }
    .wearix-instagram__item:nth-child(n+5) {
        display: none;
    }
}

@media (max-width: 600px) {
    .wearix-instagram {
        padding: 80px 16px;
    }
    .wearix-instagram__item {
        width: calc(33.33% - 8px);
        min-width: 100px;
    }
    .wearix-instagram__item:nth-child(n+4) {
        display: none;
    }
}
"""

    def render(self, settings, blocks):
        return f'''
<section class="wearix-instagram">
  <div class="container">
    {{% if section.settings.heading != blank %}}
      <h2 class="wearix-instagram__heading">{{{{ section.settings.heading | escape }}}}</h2>
    {{% endif %}}
    {{% if section.settings.handle != blank %}}
      <p class="wearix-instagram__handle">
        Follow us on Instagram: <a href="{{{{ section.settings.link }}}}" target="_blank" rel="noopener">{{{{ section.settings.handle | escape }}}}</a>
      </p>
    {{% endif %}}

    <div class="wearix-instagram__grid">
      {{% for block in section.blocks %}}
        <a href="{{{{ block.settings.link | default: section.settings.link }}}}"
           class="wearix-instagram__item" target="_blank" rel="noopener">
          {{% if block.settings.image != blank %}}
            <img src="{{{{ block.settings.image | img_url: '500x' }}}}"
                 alt="{{{{ block.settings.alt | escape }}}}"
                 loading="lazy" width="300" height="400">
          {{% endif %}}
          <div class="wearix-instagram__overlay" aria-hidden="true">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="2" y="2" width="20" height="20" rx="5" ry="5"/>
              <circle cx="12" cy="12" r="4"/>
              <circle cx="17.5" cy="6.5" r="1" fill="currentColor"/>
            </svg>
          </div>
        </a>
      {{% endfor %}}
    </div>

    {{% if section.settings.link != blank %}}
      <a href="{{{{ section.settings.link }}}}" class="wearix-instagram__cta" target="_blank" rel="noopener">
        Follow on Instagram
      </a>
    {{% endif %}}
  </div>
</section>
'''


SectionRegistry.register(WearixInstagramSection)
