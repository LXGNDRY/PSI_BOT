"""
Main product section — block-based, the most important template section.
Every element is a reorderable block. App block support included.
"""
from ...core.section import Section, SectionPreset, SectionRegistry
from ...core.setting import ( 
    Text, Select, SelectOption, Checkbox, Header, Color, Number, Range,
)
from ...core.block import Block


class MainProductSection(Section):
    type = "main-product"
    name = "Main product"
    tag = "section"
    class_name = "main-product"
    limit = 1
    available_on = ["product"]

    settings = [
        Header("Layout"),
        Select("layout", label="Product layout",
               options=[
                   SelectOption("split", "Split (image left, info right)"),
                   SelectOption("stacked", "Stacked (image top)"),
                   SelectOption("centered", "Centered"),
                   SelectOption("fullwidth", "Full width media"),
               ],
               default="split"),
        Select("media_width", label="Media width",
               options=[
                   SelectOption("small", "Small"),
                   SelectOption("medium", "Medium"),
                   SelectOption("large", "Large"),
               ],
               default="medium"),
        Select("image_ratio", label="Image aspect ratio",
               options=[
                   SelectOption("adapt", "Adapt to image"),
                   SelectOption("square", "Square (1:1)"),
                   SelectOption("portrait", "Portrait (4:5)"),
                   SelectOption("landscape", "Landscape (3:2)"),
                   SelectOption("widescreen", "Widescreen (16:9)"),
               ],
               default="adapt"),
        Select("thumbnail_position", label="Thumbnail position",
               options=[
                   SelectOption("bottom", "Bottom"),
                   SelectOption("left", "Left (desktop)"),
                   SelectOption("hide", "Hide"),
               ],
               default="bottom"),
        Header("Gallery"),
        Checkbox("enable_zoom", label="Enable image zoom", default=True),
        Checkbox("enable_video", label="Enable video", default=True),
        Checkbox("enable_3d", label="Enable 3D models", default=True),
        Header("Content"),
        Checkbox("show_vendor", label="Show vendor", default=False),
        Checkbox("show_sku", label="Show SKU", default=False),
        Checkbox("sticky_add_to_cart", label="Sticky add to cart (mobile)", default=True),
        Header("Swatches"),
        Checkbox("enable_swatches", label="Enable color/image swatches", default=True),
        Select("swatch_style", label="Swatch style",
               options=[
                   SelectOption("round", "Round"),
                   SelectOption("square", "Square"),
               ],
               default="round"),
    ]

    blocks = [
        Block(type="title", name="Title", limit=1),
        Block(type="vendor", name="Vendor", limit=1),
        Block(type="price", name="Price", limit=1),
        Block(type="rating", name="Star rating", limit=1),
        Block(type="description", name="Description", limit=1),
        Block(type="variant_picker", name="Variant picker", limit=1),
        Block(type="quantity", name="Quantity selector", limit=1),
        Block(type="buy_buttons", name="Buy buttons", limit=1),
        Block(type="pickup_availability", name="Pickup availability", limit=1),
        Block(type="share_buttons", name="Share", limit=1),
        Block(type="text", name="Text",
              settings=[Text("text", label="Text", default="")]),
        Block(type="liquid", name="Custom Liquid",
              settings=[]),
        Block(type="@app", name="App", is_app_block=True),
    ]

    presets = [
        SectionPreset(name="Product information", settings={}, blocks=[
            {"type": "title", "settings": {}},
            {"type": "vendor", "settings": {}},
            {"type": "price", "settings": {}},
            {"type": "rating", "settings": {}},
            {"type": "description", "settings": {}},
            {"type": "variant_picker", "settings": {}},
            {"type": "quantity", "settings": {}},
            {"type": "buy_buttons", "settings": {}},
            {"type": "pickup_availability", "settings": {}},
            {"type": "share_buttons", "settings": {}},
        ]),
    ]

    template = """
{%- comment -%} Main product section — block-based {%- endcomment -%}
<section class="main-product main-product--{{ section.settings.layout }}" {{ section.shopify_attributes }}>
  <div class="main-product__inner page-width">
    <div class="main-product__media">
      {%- render 'product-media',
        product: product,
        enable_zoom: section.settings.enable_zoom,
        thumbnail_position: section.settings.thumbnail_position,
        image_ratio: section.settings.image_ratio
      -%}
    </div>

    <div class="main-product__info" data-product-info>
      {%- for block in section.blocks -%}
        <div class="product__info-block product__info-block--{{ block.type }}" {{ block.shopify_attributes }}>
          {%- case block.type -%}

            {%- when 'title' -%}
              <h1 class="product__title">{{ product.title }}</h1>

            {%- when 'vendor' -%}
              {%- if section.settings.show_vendor and product.vendor -%}
                <p class="product__vendor">
                  <a href="{{ product.vendor | url_for_vendor }}">{{ product.vendor }}</a>
                </p>
              {%- endif -%}

            {%- when 'price' -%}
              {%- render 'price',
                product: product,
                show_badge: true,
                size: 'large'
              -%}

            {%- when 'rating' -%}
              {%- if product.metafields.reviews.rating and product.metafields.reviews.rating_count -%}
                <div class="product__rating">
                  <div class="product__rating-stars" aria-label="{{ product.metafields.reviews.rating_count }} reviews, {{ product.metafields.reviews.rating.value }} out of 5 stars">
                    {%- for i in (1..5) -%}
                      {%- if i <= product.metafields.reviews.rating.value -%}
                        {%- render 'icon-star' -%}
                      {%- else -%}
                        {%- render 'icon-star-outline' -%}
                      {%- endif -%}
                    {%- endfor -%}
                  </div>
                  <span class="product__rating-count">({{ product.metafields.reviews.rating_count }})</span>
                </div>
              {%- endif -%}

            {%- when 'description' -%}
              <div class="product__description">
                {{ product.description }}
              </div>

            {%- when 'variant_picker' -%}
              {%- if product.options.size > 0 -%}
                <div class="product__variants" data-variant-picker>
                  {%- for option in product.options_with_values -%}
                    <div class="product__option">
                      <label class="product__option-label">{{ option.name }}</label>
                      <div class="product__option-values">
                        {%- for value in option.values -%}
                          {%- if section.settings.enable_swatches and option.name == 'Color' -%}
                            <button
                              type="button"
                              class="swatch swatch--{{ section.settings.swatch_style }}"
                              data-value="{{ value }}"
                              data-option-index="{{ forloop.index0 }}"
                              aria-label="{{ value }}"
                            >
                              <span class="swatch__color" style="background: {{ value | downcase }}"></span>
                            </button>
                          {%- else -%}
                            <button
                              type="button"
                              class="product__option-value"
                              data-value="{{ value }}"
                              data-option-index="{{ forloop.index0 }}"
                            >
                              {{ value }}
                            </button>
                          {%- endif -%}
                        {%- endfor -%}
                      </div>
                    </div>
                  {%- endfor -%}
                </div>
              {%- endif -%}

            {%- when 'quantity' -%}
              <div class="product__quantity">
                <label class="product__quantity-label">{{ 'products.product.quantity' | t }}</label>
                {%- render 'quantity-input', name: 'quantity', value: 1, min: 1 -%}
              </div>

            {%- when 'buy_buttons' -%}
              <div class="product__buy-buttons">
                {%- form 'product', product, id: 'product-form-' | append: section.id, data_product_form: '' -%}
                  <input type="hidden" name="id" value="{{ product.selected_or_first_available_variant.id }}" data-variant-id>
                  <button
                    type="submit"
                    name="add"
                    class="btn btn--primary btn--full"
                    {% unless product.selected_or_first_available_variant.available %}disabled="disabled"{% endunless %}
                  >
                    {%- if product.selected_or_first_available_variant.available -%}
                      {{ 'products.product.add_to_cart' | t }}
                    {%- else -%}
                      {{ 'products.product.sold_out' | t }}
                    {%- endif -%}
                  </button>
                  <div class="product__dynamic-checkout">
                    {{ form | payment_button }}
                  </div>
                {%- endform -%}
              </div>

            {%- when 'pickup_availability' -%}
              {%- if product.selected_or_first_available_variant.available and product.selected_or_first_available_variant.pickup_in_store -%}
                <div class="product__pickup">
                  {%- render 'icon-map-pin' -%}
                  <span>{{ 'products.product.pickup_available' | t }}</span>
                </div>
              {%- endif -%}

            {%- when 'share_buttons' -%}
              <div class="product__share">
                <span>{{ 'products.product.share' | t }}:</span>
                <a href="https://www.facebook.com/sharer/sharer.php?u={{ product.url | absolute_url }}" target="_blank" rel="noopener" aria-label="Share on Facebook">
                  {%- render 'icon-facebook' -%}
                </a>
                <a href="https://twitter.com/intent/tweet?url={{ product.url | absolute_url }}" target="_blank" rel="noopener" aria-label="Share on Twitter">
                  {%- render 'icon-twitter' -%}
                </a>
                <a href="https://pinterest.com/pin/create/button/?url={{ product.url | absolute_url }}" target="_blank" rel="noopener" aria-label="Share on Pinterest">
                  {%- render 'icon-pinterest' -%}
                </a>
              </div>

            {%- when 'text' -%}
              <div class="product__text-block">
                {{ block.settings.text }}
              </div>

            {%- when 'liquid' -%}
              <div class="product__custom-liquid">
                {{ block.settings.code }}
              </div>

          {%- endcase -%}
        </div>
      {%- endfor -%}

      {%- if section.settings.show_sku and product.selected_or_first_available_variant.sku -%}
        <p class="product__sku">{{ 'products.product.sku' | t }}: {{ product.selected_or_first_available_variant.sku }}</p>
      {%- endif -%}
    </div>
  </div>
</section>
    """

    styles = """
.main-product {
  padding: 2rem 0;
}

.main-product__inner {
  display: grid;
  gap: 3rem;
  max-width: var(--max-width, 1440px);
  margin: 0 auto;
  padding: 0 1.5rem;
}

.main-product--split .main-product__inner {
  grid-template-columns: 1fr 1fr;
}

.main-product--stacked .main-product__inner {
  grid-template-columns: 1fr;
  max-width: 800px;
}

.main-product--centered .main-product__inner {
  grid-template-columns: 1fr;
  max-width: 600px;
  text-align: center;
}

.product__title {
  font-family: var(--font-heading-family);
  font-size: 2rem;
  font-weight: 600;
  line-height: 1.2;
  margin: 0 0 0.5rem;
  color: var(--color-text);
}

.product__vendor {
  font-size: 0.875rem;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin: 0 0 1rem;
}

.product__vendor a {
  color: inherit;
  text-decoration: none;
}

.product__vendor a:hover {
  text-decoration: underline;
}

.product__description {
  font-size: 0.875rem;
  line-height: 1.6;
  color: var(--color-text);
  margin: 1rem 0;
}

.product__variants {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  margin: 1.5rem 0;
}

.product__option-label {
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  display: block;
}

.product__option-values {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.product__option-value {
  padding: 0.5rem 1rem;
  border: 1px solid var(--color-border, #ddd);
  border-radius: var(--radius-md, 6px);
  background: var(--color-surface, #fff);
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.15s ease;
}

.product__option-value:hover {
  border-color: var(--color-primary, #111);
}

.product__option-value[aria-selected="true"] {
  background: var(--color-primary, #111);
  color: var(--color-surface, #fff);
  border-color: var(--color-primary, #111);
}

.swatch {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  border: 2px solid var(--color-border, #ddd);
  padding: 0;
  cursor: pointer;
  overflow: hidden;
}

.swatch--square {
  border-radius: var(--radius-sm, 4px);
}

.swatch__color {
  display: block;
  width: 100%;
  height: 100%;
}

.swatch[aria-selected="true"] {
  border-color: var(--color-primary, #111);
  box-shadow: 0 0 0 2px var(--color-background, #fff), 0 0 0 4px var(--color-primary, #111);
}

.product__quantity {
  margin: 1rem 0;
}

.product__quantity-label {
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  display: block;
}

.product__buy-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin: 1.5rem 0;
}

.product__dynamic-checkout {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.product__pickup {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: var(--color-text-muted);
  margin: 1rem 0;
}

.product__sku {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  margin-top: 1rem;
}

.product__share {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.875rem;
  color: var(--color-text-muted);
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--color-border, #eee);
}

.product__share a {
  color: inherit;
}

.product__share a:hover {
  color: var(--color-text);
}

.product__rating {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: var(--color-text-muted);
  margin: 0.5rem 0;
}

.product__rating-stars {
  display: inline-flex;
  color: #f59e0b;
}

@media (max-width: 1023px) {
  .main-product--split .main-product__inner {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
}

@media (max-width: 767px) {
  .product__title { font-size: 1.5rem; }
  .main-product__inner { padding: 0 1rem; }
}
    """

    scripts = """
// Product variant picker logic
(function() {
  const sectionId = 'shopify-section-' + __section_id;
  const section = document.getElementById(sectionId);
  if (!section) return;

  const form = section.querySelector('[data-product-form]');
  if (!form) return;

  const variantIdInput = form.querySelector('[data-variant-id]');
  const optionButtons = section.querySelectorAll('[data-option-index]');
  const product = window.__product__ || {};

  let selectedOptions = [];

  optionButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const index = parseInt(btn.dataset.optionIndex);
      const value = btn.dataset.value;
      selectedOptions[index] = value;
      updateVariant();
    });
  });

  function updateVariant() {
    if (!product.variants) return;
    const variant = product.variants.find(v =>
      v.options.every((opt, i) => opt === selectedOptions[i])
    );
    if (variant) {
      variantIdInput.value = variant.id;
    }
  }
})();
    """


SectionRegistry.register(MainProductSection)
