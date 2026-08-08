"""
Wearix Image With Text — full-width lifestyle image with text overlay block.

Characteristic of Wearix:
- One side: large portrait/lifestyle image
- Other side: text block on soft gray background
- CTA button at bottom
- Alternating layout (left image / right text, or right image / left text)
"""
from __future__ import annotations

from ...core.section import Section, SectionPreset, SectionRegistry
from ...core.setting import (
    Text, ImagePicker, Select, SelectOption, Checkbox, Url, Header, RichText,
)


class WearixImageWithTextSection(Section):
    type = "wearix-image-with-text"
    name = "Wearix image with text"
    tag = "section"
    class_name = "wearix-image-with-text"

    settings = [
        Header("Layout"),
        Select("layout", label="Image position",
               options=[
                   SelectOption("left", "Image left, text right"),
                   SelectOption("right", "Image right, text left"),
               ], default="left"),

        Header("Image"),
        ImagePicker("image", label="Image"),
        Text("image_alt", label="Image alt text", default=""),

        Header("Text"),
        Text("eyebrow", label="Eyebrow text", default="OUR STORY"),
        Text("heading", label="Heading", default="Defining modern style"),
        RichText("body", label="Body text",
                 default="<p>We craft every piece with intention — from fabric selection to final stitch. Our mission is simple: create clothing that moves with you.</p>"),
        Text("button_text", label="Button text", default="More about us"),
        Url("button_link", label="Button link"),
        Text("secondary_button_text", label="Secondary button text", default=""),
        Url("secondary_button_link", label="Secondary button link"),

        Header("Background"),
        Checkbox("gray_bg", label="Gray text background", default=True),
    ]

    blocks = []

    presets = [
        SectionPreset(
            name="Wearix image with text",
            settings={
                "layout": "left",
                "eyebrow": "OUR STORY",
                "heading": "Defining modern style",
                "button_text": "More about us",
                "gray_bg": True,
            },
            blocks=[],
        ),
        SectionPreset(
            name="Image right",
            settings={
                "layout": "right",
                "eyebrow": "OUR PHILOSOPHY",
                "heading": "Where quality meets ease",
                "button_text": "Learn more",
                "gray_bg": True,
            },
            blocks=[],
        ),
    ]

    styles = """
.wearix-image-with-text {
    display: grid;
    grid-template-columns: 1fr 1fr;
    min-height: 600px;
}

.wearix-image-with-text__image {
    position: relative;
    overflow: hidden;
}

.wearix-image-with-text__image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.6s ease;
}

.wearix-image-with-text:hover .wearix-image-with-text__image img {
    transform: scale(1.02);
}

.wearix-image-with-text__text {
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 80px 64px;
    background: #f7f7f7;
}

.wearix-image-with-text--white .wearix-image-with-text__text {
    background: #fff;
}

.wearix-image-with-text__eyebrow {
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #707070;
    margin-bottom: 20px;
}

.wearix-image-with-text__heading {
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 500;
    line-height: 1.1;
    letter-spacing: -0.02em;
    margin: 0 0 24px 0;
    color: #000;
}

.wearix-image-with-text__body {
    font-size: 16px;
    line-height: 1.6;
    color: #707070;
    margin: 0 0 32px 0;
    max-width: 500px;
}

.wearix-image-with-text__buttons {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
}

.wearix-image-with-text--reverse .wearix-image-with-text__image { order: 2; }
.wearix-image-with-text--reverse .wearix-image-with-text__text { order: 1; }

@media (max-width: 768px) {
    .wearix-image-with-text {
        grid-template-columns: 1fr;
        min-height: auto;
    }
    .wearix-image-with-text__image {
        min-height: 400px;
    }
    .wearix-image-with-text__text {
        padding: 48px 24px;
    }
    .wearix-image-with-text--reverse .wearix-image-with-text__image { order: 0; }
    .wearix-image-with-text--reverse .wearix-image-with-text__text { order: 1; }
}
"""

    def render(self, settings, blocks):
        layout = settings.get("layout", "left")
        reverse = " wearix-image-with-text--reverse" if layout == "right" else ""
        white = " wearix-image-with-text--white" if not settings.get("gray_bg", True) else ""
        return f'''
<section class="wearix-image-with-text{reverse}{white}">
  <div class="wearix-image-with-text__image">
    {{% if section.settings.image != blank %}}
      <img src="{{{{ section.settings.image | img_url: '1200x' }}}}"
           alt="{{{{ section.settings.image_alt | default: section.settings.heading | escape }}}}"
           loading="lazy" width="1200" height="1600">
    {{% endif %}}
  </div>
  <div class="wearix-image-with-text__text">
    {{% if section.settings.eyebrow != blank %}}
      <span class="wearix-image-with-text__eyebrow">{{{{ section.settings.eyebrow | escape }}}}</span>
    {{% endif %}}
    {{% if section.settings.heading != blank %}}
      <h2 class="wearix-image-with-text__heading">{{{{ section.settings.heading | escape }}}}</h2>
    {{% endif %}}
    {{% if section.settings.body != blank %}}
      <div class="wearix-image-with-text__body">{{{{ section.settings.body }}}}</div>
    {{% endif %}}
    <div class="wearix-image-with-text__buttons">
      {{% if section.settings.button_text != blank %}}
        <a href="{{{{ section.settings.button_link }}}}" class="btn btn--primary btn--pill">
          {{{{ section.settings.button_text | escape }}}}
        </a>
      {{% endif %}}
      {{% if section.settings.secondary_button_text != blank %}}
        <a href="{{{{ section.settings.secondary_button_link }}}}" class="btn btn--outline btn--pill">
          {{{{ section.settings.secondary_button_text | escape }}}}
        </a>
      {{% endif %}}
    </div>
  </div>
</section>
'''


SectionRegistry.register(WearixImageWithTextSection)
