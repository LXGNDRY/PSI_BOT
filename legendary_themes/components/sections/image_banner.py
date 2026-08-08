"""Image banner section — hero section with image background + text overlay."""
from ...core.section import Section, SectionPreset, SectionRegistry
from ...core.setting import (
    Text, ImagePicker, Select, SelectOption, Checkbox, Url, Header, Color, Range,
)


class ImageBannerSection(Section):
    type = "image-banner"
    name = "Image banner"
    tag = "section"
    class_name = "image-banner"
    available_on = ["index", "collection", "product", "page", "blog", "article", "404"]

    settings = [
        Header("Image"),
        ImagePicker("desktop_image", label="Desktop image"),
        ImagePicker("mobile_image", label="Mobile image (optional)"),
        Select("image_fit", label="Image fit",
               options=[
                   SelectOption("cover", "Cover"),
                   SelectOption("contain", "Contain"),
               ],
               default="cover"),
        Header("Content"),
        Text("heading", label="Heading", default="Welcome to our store"),
        Text("subheading", label="Subheading", default="Discover our collection"),
        Text("text", label="Body text", default=""),
        Select("text_position", label="Text position",
               options=[
                   SelectOption("center", "Center"),
                   SelectOption("left", "Left"),
                   SelectOption("right", "Right"),
                   SelectOption("bottom-left", "Bottom left"),
                   SelectOption("bottom-right", "Bottom right"),
                   SelectOption("top-left", "Top left"),
                   SelectOption("top-right", "Top right"),
               ],
               default="center"),
        Select("text_alignment", label="Text alignment",
               options=[
                   SelectOption("left", "Left"),
                   SelectOption("center", "Center"),
                   SelectOption("right", "Right"),
               ],
               default="center"),
        Header("Buttons"),
        Checkbox("show_button_primary", label="Show primary button", default=True),
        Text("button_primary_text", label="Primary button text", default="Shop now"),
        Url("button_primary_url", label="Primary button link", default="/collections/all"),
        Checkbox("show_button_secondary", label="Show secondary button", default=False),
        Text("button_secondary_text", label="Secondary button text", default="Learn more"),
        Url("button_secondary_url", label="Secondary button link", default="/pages/about"),
        Header("Style"),
        Range("section_height", label="Section height", min=300, max=800, step=50, default=500, unit="px"),
        Select("overlay_opacity", label="Overlay opacity",
               options=[
                   SelectOption("0", "None"),
                   SelectOption("0.2", "Light"),
                   SelectOption("0.4", "Medium"),
                   SelectOption("0.6", "Dark"),
               ],
               default="0.2"),
        Color("overlay_color", label="Overlay color", default="#000000"),
        Color("text_color", label="Text color", default="#ffffff"),
        Header("Settings"),
        Checkbox("full_width", label="Full width", default=True),
        Checkbox("show_on_mobile", label="Show on mobile", default=True),
    ]

    presets = [
        SectionPreset(name="Image banner", settings={
            "heading": "Welcome to our store",
            "subheading": "Discover our collection",
            "text_position": "center",
            "text_alignment": "center",
            "show_button_primary": True,
            "button_primary_text": "Shop now",
            "button_primary_url": "/collections/all",
            "section_height": 500,
            "overlay_opacity": "0.2",
            "overlay_color": "#000000",
            "text_color": "#ffffff",
            "full_width": True,
        }),
    ]

    template = """
<section
  class="image-banner image-banner--{{ section.settings.text_position }} {% if section.settings.show_on_mobile == false %}image-banner--hide-mobile{% endif %}"
  {{ section.shopify_attributes }}
  style="min-height: {{ section.settings.section_height }}px; --overlay-color: {{ section.settings.overlay_color }}; --overlay-opacity: {{ section.settings.overlay_opacity }}; --text-color: {{ section.settings.text_color }};"
>
  <div class="image-banner__media">
    {%- if section.settings.desktop_image -%}
      {{ section.settings.desktop_image | image_url: width: 2000 | image_tag:
        alt: section.settings.heading | default: '' | escape,
        sizes: '100vw',
        loading: 'eager',
        class: 'image-banner__image image-banner__image--desktop'
      }}
    {%- endif -%}
    {%- if section.settings.mobile_image -%}
      {{ section.settings.mobile_image | image_url: width: 1000 | image_tag:
        alt: section.settings.heading | default: '' | escape,
        sizes: '100vw',
        loading: 'eager',
        class: 'image-banner__image image-banner__image--mobile'
      }}
    {%- endif -%}
    <div class="image-banner__overlay"></div>
  </div>

  <div class="image-banner__content">
    <div class="image-banner__text" style="text-align: {{ section.settings.text_alignment }};">
      {%- if section.settings.heading -%}
        <h2 class="image-banner__heading">{{ section.settings.heading }}</h2>
      {%- endif -%}
      {%- if section.settings.subheading -%}
        <p class="image-banner__subheading">{{ section.settings.subheading }}</p>
      {%- endif -%}
      {%- if section.settings.text -%}
        <p class="image-banner__text">{{ section.settings.text }}</p>
      {%- endif -%}
      <div class="image-banner__buttons">
        {%- if section.settings.show_button_primary and section.settings.button_primary_text -%}
          <a href="{{ section.settings.button_primary_url }}" class="btn btn--primary">
            {{ section.settings.button_primary_text }}
          </a>
        {%- endif -%}
        {%- if section.settings.show_button_secondary and section.settings.button_secondary_text -%}
          <a href="{{ section.settings.button_secondary_url }}" class="btn btn--secondary">
            {{ section.settings.button_secondary_text }}
          </a>
        {%- endif -%}
      </div>
    </div>
  </div>
</section>
    """

    styles = """
.image-banner {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  color: var(--text-color, #fff);
}

.image-banner__media {
  position: absolute;
  inset: 0;
  z-index: 0;
}

.image-banner__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-banner__image--mobile {
  display: none;
}

.image-banner__overlay {
  position: absolute;
  inset: 0;
  background: var(--overlay-color, #000);
  opacity: var(--overlay-opacity, 0);
}

.image-banner__content {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: var(--max-width, 1440px);
  padding: 4rem 1.5rem;
}

.image-banner--center .image-banner__content {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.image-banner--left .image-banner__content {
  display: flex;
  justify-content: flex-start;
}

.image-banner--right .image-banner__content {
  display: flex;
  justify-content: flex-end;
}

.image-banner--bottom-left .image-banner__content {
  display: flex;
  align-items: flex-end;
  justify-content: flex-start;
}

.image-banner--bottom-right .image-banner__content {
  display: flex;
  align-items: flex-end;
  justify-content: flex-end;
}

.image-banner__text {
  max-width: 600px;
}

.image-banner__heading {
  font-family: var(--font-heading-family);
  font-size: clamp(2rem, 5vw, 4rem);
  font-weight: 700;
  line-height: 1.1;
  margin: 0 0 1rem;
}

.image-banner__subheading {
  font-size: clamp(1rem, 2vw, 1.25rem);
  line-height: 1.5;
  margin: 0 0 1.5rem;
  opacity: 0.9;
}

.image-banner__text {
  font-size: 1rem;
  line-height: 1.6;
  margin: 0 0 2rem;
  opacity: 0.85;
}

.image-banner__buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: inherit;
}

@media (max-width: 767px) {
  .image-banner__image--desktop {
    display: none;
  }
  .image-banner__image--mobile {
    display: block;
  }
  .image-banner__buttons {
    justify-content: center;
  }
  .image-banner--hide-mobile {
    display: none;
  }
}
    """


SectionRegistry.register(ImageBannerSection)
