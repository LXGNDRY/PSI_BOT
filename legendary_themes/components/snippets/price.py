"""
Price snippet — displays product/variant prices with all required elements:
regular price, compare-at price, sale badge, unit pricing.
"""
from ...core.snippet import Snippet, SnippetRegistry


PRICE_CSS = """
.price {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  line-height: 1.2;
}

.price__regular {
  font-size: var(--font-size-lg, 1.125rem);
  font-weight: 600;
  color: var(--color-text);
}

.price--on-sale .price__regular {
  color: var(--color-error, #e53935);
}

.price__compare {
  font-size: var(--font-size-sm, 0.875rem);
  text-decoration: line-through;
  color: var(--color-text-muted);
}

.price__unit {
  font-size: var(--font-size-xs, 0.75rem);
  color: var(--color-text-muted);
  margin-top: 0.125rem;
}

.price__badge {
  display: inline-block;
  padding: 0.125rem 0.5rem;
  background: var(--color-error, #e53935);
  color: #fff;
  font-size: var(--font-size-xs, 0.75rem);
  font-weight: 600;
  border-radius: var(--radius-sm, 2px);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.price--small .price__regular { font-size: 1rem; }
.price--large .price__regular { font-size: 1.5rem; }
"""


price_snippet = Snippet(
    name="price",
    template="""{% comment %}
  Renders product price with compare-at, sale badge, and unit pricing.
  Usage:
    {% render 'price', product: product, show_badge: true, size: 'medium' %}
  Parameters:
    - product: product object (required)
    - variant: variant object (optional, defaults to product.selected_or_first_available_variant)
    - show_badge: boolean (default: true)
    - size: 'small' | 'medium' | 'large' (default: 'medium')
    - show_unit_price: boolean (default: true)
{% endcomment %}

{%- assign _product = product -%}
{%- assign _variant = variant | default: _product.selected_or_first_available_variant -%}
{%- assign _show_badge = show_badge | default: true -%}
{%- assign _size = size | default: 'medium' -%}
{%- assign _show_unit = show_unit_price | default: true -%}
{%- assign _on_sale = false -%}

{%- if _variant.compare_at_price > _variant.price -%}
  {%- assign _on_sale = true -%}
{%- endif -%}

<div class="price price--{{ _size }}{% if _on_sale %} price--on-sale{% endif %}" data-price>
  {%- if _show_badge and _on_sale -%}
    <span class="price__badge">{{ 'products.product.sale' | t }}</span>
  {%- endif -%}

  <div class="price__row">
    <span class="price__regular">{{ _variant.price | money }}</span>
    {%- if _on_sale -%}
      <span class="price__compare">{{ _variant.compare_at_price | money }}</span>
    {%- endif -%}
  </div>

  {%- if _product.price_varies -%}
    <span class="price__range-text price--small">
      {{ 'products.product.price_from' | t: price: _product.price_min | money }}
    </span>
  {%- endif -%}

  {%- if _show_unit and _variant.unit_price_measurement -%}
    <p class="price__unit">
      {{ _variant.unit_price | money }}
      {{ _variant.unit_price_measurement.reference_value }}
      {{ _variant.unit_price_measurement.reference_unit }}
    </p>
  {%- endif -%}
</div>
""",
    params=["product", "variant", "show_badge", "size", "show_unit_price"],
    styles=PRICE_CSS,
)

SnippetRegistry.register(price_snippet)
