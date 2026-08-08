"""Product media gallery snippet — images, 3D, video, zoom."""
from ...core.snippet import Snippet, SnippetRegistry


PRODUCT_MEDIA_CSS = """
.product-media {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.product-media__main {
  position: relative;
  aspect-ratio: var(--media-ratio, 4/5);
  overflow: hidden;
  background: var(--color-surface, #f9f9f9);
  border-radius: var(--radius-md, 8px);
}

.product-media__main img,
.product-media__main video,
.product-media__main model-viewer {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-media__zoom-btn {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  width: 2.5rem;
  height: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 50%;
  cursor: pointer;
  z-index: 2;
}

.product-media__thumbnails {
  display: flex;
  gap: 0.5rem;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch;
}

.product-media__thumbnails[hidden] {
  display: none;
}

.product-media__thumb {
  flex: 0 0 auto;
  width: 4rem;
  height: 4rem;
  scroll-snap-align: start;
  border: 2px solid transparent;
  border-radius: var(--radius-sm, 4px);
  overflow: hidden;
  cursor: pointer;
  background: var(--color-surface, #f9f9f9);
  padding: 0;
}

.product-media__thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-media__thumb[aria-selected="true"] {
  border-color: var(--color-primary, #111);
}

.product-media__thumb:focus-visible {
  outline: 2px solid var(--color-accent, #2563eb);
  outline-offset: 2px;
}

@media (min-width: 1024px) {
  .product-media--thumbnails-left {
    flex-direction: row;
  }
  .product-media--thumbnails-left .product-media__thumbnails {
    flex-direction: column;
    order: -1;
    overflow-x: hidden;
    overflow-y: auto;
    scroll-snap-type: y mandatory;
  }
}
"""

product_media_snippet = Snippet(
    name="product-media",
    template="""{% comment %}
  Renders product media gallery: main image + thumbnails, supports images, video, 3D models.
  Usage:
    {% render 'product-media', product: product, thumbnail_position: 'bottom' %}
{% endcomment %}

{%- assign _product = product -%}
{%- assign _media = _product.media -%}
{%- assign _thumb_pos = thumbnail_position | default: 'bottom' -%}
{%- assign _enable_zoom = enable_zoom | default: true -%}
{%- assign _ratio = image_ratio | default: 'adapt' -%}

{%- if _media.size > 0 -%}
  <div class="product-media product-media--thumbnails-{{ _thumb_pos }}">
    <div class="product-media__main" role="region" aria-label="{{ 'products.product.media.gallery' | t }}">
      {%- for media in _media -%}
        <div
          class="product-media__slide {% if forloop.first %}is-active{% endif %}"
          data-media-id="{{ media.id }}"
          data-media-type="{{ media.media_type }}"
          {% unless forloop.first %}hidden{% endunless %}
        >
          {%- if media.media_type == 'image' -%}
            {{ media | image_url: width: 1200 | image_tag:
              alt: media.alt | default: _product.title | escape,
              sizes: '(min-width: 1024px) 50vw, 100vw',
              loading: forloop.first | default: 'eager' | replace: 'true', 'eager' | replace: 'false', 'lazy'
            }}
          {%- elsif media.media_type == 'video' or media.media_type == 'external_video' -%}
            <video controls poster="{{ media.preview_image | image_url: width: 1200 }}" playsinline>
              {%- if media.media_type == 'video' -%}
                <source src="{{ media.sources[0].url }}" type="{{ media.sources[0].mime_type }}">
              {%- else -%}
                <source src="{{ media.sources[0].url }}">
              {%- endif -%}
            </video>
          {%- elsif media.media_type == 'model' -%}
            {{ media | model_viewer_tag:
              alt: media.alt | default: _product.title | escape,
              loading: forloop.first | default: 'eager' | replace: 'true', 'eager' | replace: 'false', 'lazy'
            }}
          {%- endif -%}
        </div>
      {%- endfor -%}

      {%- if _enable_zoom and _media.first.media_type == 'image' -%}
        <button
          type="button"
          class="product-media__zoom-btn"
          aria-label="{{ 'products.product.media.zoom' | t }}"
          data-action="zoom"
        >
          {%- render 'icon-zoom-in' -%}
        </button>
      {%- endif -%}
    </div>

    {%- if _media.size > 1 -%}
      <div
        class="product-media__thumbnails"
        role="tablist"
        aria-label="{{ 'products.product.media.thumbnails' | t }}"
      >
        {%- for media in _media -%}
          <button
            type="button"
            class="product-media__thumb"
            role="tab"
            aria-selected="{% if forloop.first %}true{% else %}false{% endif %}"
            aria-label="{{ 'products.product.media.view_image' | t: index: forloop.index }}"
            data-media-index="{{ forloop.index0 }}"
          >
            {%- if media.media_type == 'image' -%}
              {{ media | image_url: width: 200 | image_tag:
                alt: media.alt | default: '' | escape,
                loading: 'lazy'
              }}
            {%- elsif media.preview_image -%}
              {{ media.preview_image | image_url: width: 200 | image_tag:
                alt: '',
                loading: 'lazy'
              }}
            {%- endif -%}
          </button>
        {%- endfor -%}
      </div>
    {%- endif -%}
  </div>
{%- else -%}
  <div class="product-media product-media--empty">
    <div class="product-media__main">
      <div class="product-media__placeholder" aria-hidden="true"></div>
    </div>
  </div>
{%- endif -%}
""",
    params=["product", "thumbnail_position", "enable_zoom", "image_ratio"],
    styles=PRODUCT_MEDIA_CSS,
)

SnippetRegistry.register(product_media_snippet)
