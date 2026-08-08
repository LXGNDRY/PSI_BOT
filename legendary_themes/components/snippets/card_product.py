"""
Product card snippet — the most important UI component.
Rendered in collection grids, related products, featured collections, search results.
"""
from ...core.snippet import Snippet, SnippetRegistry


CARD_PRODUCT_CSS = """
.c-card {
  position: relative;
  display: flex;
  flex-direction: column;
  height: 100%;
  font-family: var(--font-body-family);
}

.c-card__media {
  position: relative;
  overflow: hidden;
  background: var(--color-surface, #f9f9f9);
  aspect-ratio: var(--card-ratio, 4/5);
}

.c-card__media img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.c-card:hover .c-card__media img {
  transform: scale(1.03);
}

.c-card__media-secondary {
  position: absolute;
  inset: 0;
  opacity: 0;
  transition: opacity 0.4s ease;
}

.c-card:hover .c-card__media-secondary {
  opacity: 1;
}

.c-card__badge-wrap {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 1;
}

.c-card__info {
  padding: 1rem 0 0;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.c-card__vendor {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin: 0;
}

.c-card__title {
  font-family: var(--font-heading-family, inherit);
  font-size: 0.875rem;
  font-weight: 500;
  line-height: 1.3;
  margin: 0;
  color: var(--color-text);
}

.c-card__title a {
  color: inherit;
  text-decoration: none;
}

.c-card__title a:hover {
  text-decoration: underline;
}

.c-card__price {
  margin-top: auto;
  padding-top: 0.25rem;
}

.c-card__quick-add {
  position: absolute;
  bottom: 0.75rem;
  left: 0.75rem;
  right: 0.75rem;
  opacity: 0;
  transform: translateY(8px);
  transition: all 0.3s ease;
  z-index: 2;
}

.c-card:hover .c-card__quick-add {
  opacity: 1;
  transform: translateY(0);
}

@media (max-width: 767px) {
  .c-card__quick-add {
    opacity: 1;
    transform: none;
    position: static;
    margin-top: 0.75rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  .c-card__media img { transition: none; }
  .c-card__media-secondary { transition: none; }
  .c-card__quick-add { transition: none; }
}
"""


card_product_snippet = Snippet(
    name="card-product",
    template="""{% comment %}
  Renders a product card.
  Usage:
    {% render 'card-product', product: product, show_vendor: true, show_price: true, image_ratio: '4/5' %}
  Parameters:
    - product: product object (required)
    - show_vendor: boolean (default: false)
    - show_price: boolean (default: true)
    - show_rating: boolean (default: false)
    - show_quick_add: boolean (default: false)
    - image_ratio: 'adapt' | 'square' | 'portrait' | 'landscape' | 'widescreen' (default: 'adapt')
    - badge_position: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right' (default: 'top-left')
    - secondary_image: boolean (default: false)
    - grid_columns: number (default: 4) — used for image sizing
    - full_width: boolean (default: false)
{% endcomment %}

{%- assign _product = product -%}
{%- assign _show_vendor = show_vendor | default: false -%}
{%- assign _show_price = show_price | default: true -%}
{%- assign _show_rating = show_rating | default: false -%}
{%- assign _show_quick_add = show_quick_add | default: false -%}
{%- assign _image_ratio = image_ratio | default: 'adapt' -%}
{%- assign _badge_pos = badge_position | default: 'top-left' -%}
{%- assign _secondary_image = secondary_image | default: false -%}
{%- assign _grid_cols = grid_columns | default: 4 -%}

{%- assign _featured_image = _product.featured_image -%}
{%- assign _ratio_style = '' -%}
{%- if _image_ratio == 'adapt' and _featured_image -%}
  {%- assign _ratio_style = _featured_image.aspect_ratio | default: '1' -%}
  {%- assign _ratio_style = '--card-ratio: ' | append: _ratio_style -%}
{%- elsif _image_ratio == 'square' -%}
  {%- assign _ratio_style = '--card-ratio: 1/1' -%}
{%- elsif _image_ratio == 'portrait' -%}
  {%- assign _ratio_style = '--card-ratio: 4/5' -%}
{%- elsif _image_ratio == 'landscape' -%}
  {%- assign _ratio_style = '--card-ratio: 3/2' -%}
{%- elsif _image_ratio == 'widescreen' -%}
  {%- assign _ratio_style = '--card-ratio: 16/9' -%}
{%- endif -%}

{%- assign _on_sale = false -%}
{%- if _product.compare_at_price_min > _product.price_min -%}
  {%- assign _on_sale = true -%}
{%- endif -%}

<div class="c-card" style="{{ _ratio_style }}">
  <a href="{{ _product.url }}" class="c-card__link" aria-label="{{ _product.title | escape }}">
    <div class="c-card__media">
      <div class="c-card__badge-wrap">
        {%- if _on_sale -%}
          {%- render 'badge', text: 'products.product.sale' | t, type: 'sale', position: _badge_pos -%}
        {%- endif -%}
        {%- unless _product.available -%}
          {%- render 'badge', text: 'products.product.sold_out' | t, type: 'sold-out', position: _badge_pos -%}
        {%- endunless -%}
      </div>

      {%- if _featured_image -%}
        {{ _featured_image | image_url: width: 600 | image_tag:
          alt: _featured_image.alt | default: _product.title | escape,
          sizes: '
            (min-width: 1280px) ' | append: _grid_cols | append: 'fr,
            (min-width: 768px) 33vw,
            50vw
          ',
          loading: 'lazy',
          decoding: 'async'
        }}
      {%- else -%}
        <div class="c-card__media-placeholder" aria-hidden="true"></div>
      {%- endif -%}

      {%- if _secondary_image and _product.images.size > 1 -%}
        <div class="c-card__media-secondary">
          {{ _product.images[1] | image_url: width: 600 | image_tag:
            alt: _product.images[1].alt | default: _product.title | escape,
            loading: 'lazy',
            decoding: 'async'
          }}
        </div>
      {%- endif -%}
    </div>
  </a>

  <div class="c-card__info">
    {%- if _show_vendor and _product.vendor -%}
      <p class="c-card__vendor">{{ _product.vendor }}</p>
    {%- endif -%}

    <h3 class="c-card__title">
      <a href="{{ _product.url }}">{{ _product.title }}</a>
    </h3>

    {%- if _show_price -%}
      <div class="c-card__price">
        {%- render 'price', product: _product, show_badge: false, size: 'small' -%}
      </div>
    {%- endif -%}

    {%- if _show_quick_add and _product.available and _product.variants.size == 1 -%}
      <div class="c-card__quick-add">
        {%- form 'product', _product, id: 'QuickAdd-' | append: _product.id -%}
          <input type="hidden" name="id" value="{{ _product.selected_or_first_available_variant.id }}">
          <button type="submit" class="btn btn--secondary btn--small btn--full">
            {{ 'products.product.quick_add' | t }}
          </button>
        {%- endform -%}
      </div>
    {%- endif -%}
  </div>
</div>
""",
    params=[
        "product", "show_vendor", "show_price", "show_rating",
        "show_quick_add", "image_ratio", "badge_position",
        "secondary_image", "grid_columns", "full_width",
    ],
    styles=CARD_PRODUCT_CSS,
)

SnippetRegistry.register(card_product_snippet)
