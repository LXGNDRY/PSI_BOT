"""Rich text section."""
from ...core.section import Section, SectionPreset, SectionRegistry
from ...core.setting import (
    Text, RichText, Select, SelectOption, Checkbox, Url, Header, TextAlignment,
)


class RichTextSection(Section):
    type = "rich-text"
    name = "Rich text"
    tag = "section"
    class_name = "rich-text"
    available_on = ["index", "collection", "product", "page", "blog", "article", "cart", "search", "404"]

    settings = [
        Header("Content"),
        Text("heading", label="Heading", default="Rich text heading"),
        RichText("text", label="Text", default="<p>Your rich text content goes here.</p>"),
        Header("Layout"),
        Select("width", label="Container width",
               options=[
                   SelectOption("narrow", "Narrow"),
                   SelectOption("medium", "Medium"),
                   SelectOption("full", "Full width"),
               ],
               default="medium"),
        TextAlignment("text_alignment", label="Text alignment", default="center"),
        Header("Button"),
        Checkbox("show_button", label="Show button", default=False),
        Text("button_text", label="Button text", default="Learn more"),
        Url("button_url", label="Button link", default=""),
    ]

    presets = [
        SectionPreset(name="Rich text", settings={
            "heading": "Rich text heading",
            "text": "<p>Your rich text content goes here.</p>",
            "width": "medium",
            "text_alignment": "center",
            "show_button": False,
        }),
    ]

    template = """
<section
  class="rich-text rich-text--{{ section.settings.width }} rich-text--{{ section.settings.text_alignment }}"
  {{ section.shopify_attributes }}
  style="text-align: {{ section.settings.text_alignment }};"
>
  <div class="rich-text__inner page-width">
    <div class="rich-text__content">
      {%- if section.settings.heading -%}
        <h2 class="rich-text__heading">{{ section.settings.heading }}</h2>
      {%- endif -%}
      {%- if section.settings.text -%}
        <div class="rich-text__text">{{ section.settings.text }}</div>
      {%- endif -%}
      {%- if section.settings.show_button and section.settings.button_text -%}
        <div class="rich-text__button">
          <a href="{{ section.settings.button_url }}" class="btn btn--primary">
            {{ section.settings.button_text }}
          </a>
        </div>
      {%- endif -%}
    </div>
  </div>
</section>
    """

    styles = """
.rich-text {
  padding: 3rem 0;
}

.rich-text__inner {
  max-width: var(--max-width, 1440px);
  margin: 0 auto;
  padding: 0 1.5rem;
}

.rich-text--narrow .rich-text__content {
  max-width: 600px;
  margin: 0 auto;
}

.rich-text--medium .rich-text__content {
  max-width: 800px;
  margin: 0 auto;
}

.rich-text__heading {
  font-family: var(--font-heading-family);
  font-size: clamp(1.5rem, 3vw, 2.5rem);
  font-weight: 600;
  margin: 0 0 1rem;
}

.rich-text__text {
  font-size: 1rem;
  line-height: 1.6;
  color: var(--color-text);
}

.rich-text__text p {
  margin: 0 0 1rem;
}

.rich-text__text p:last-child {
  margin-bottom: 0;
}

.rich-text__button {
  margin-top: 1.5rem;
}
    """


SectionRegistry.register(RichTextSection)
