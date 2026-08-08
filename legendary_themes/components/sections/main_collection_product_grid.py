"""
Main collection product grid section — collection + search pages.
Includes sorting, filtering, pagination.
"""
from ...core.section import Section, SectionPreset, SectionRegistry
from ...core.setting import (
    Text, Select, SelectOption, Checkbox, Number, Header, Range,
)


class MainCollectionProductGridSection(Section):
    type = "main-collection-product-grid"
    name = "Product grid"
    tag = "section"
    class_name = "collection-product-grid"
    limit = 1
    available_on = ["collection", "search"]

    settings = [
        Header("Layout"),
        Range("products_per_page", label="Products per page",
              min=6, max=48, step=2, default=24, unit="products"),
        Range("columns_mobile", label="Columns (mobile)",
              min=2, max=3, step=1, default=2, unit="columns"),
        Range("columns_desktop", label="Columns (desktop)",
              min=3, max=6, step=1, default=4, unit="columns"),
        Select("image_ratio", label="Image aspect ratio",
               options=[
                   SelectOption("adapt", "Adapt to image"),
                   SelectOption("square", "Square (1:1)"),
                   SelectOption("portrait", "Portrait (4:5)"),
                   SelectOption("landscape", "Landscape (3:2)"),
               ],
               default="adapt"),
        Header("Content"),
        Checkbox("show_vendor", label="Show vendor", default=False),
        Checkbox("show_rating", label="Show star rating", default=False),
        Checkbox("show_swatches", label="Show color swatches", default=False),
        Checkbox("show_quick_add", label="Show quick add button", default=False),
        Checkbox("show_secondary_image", label="Show second image on hover", default=False),
        Header("Collection header"),
        Checkbox("show_title", label="Show collection title", default=True),
        Checkbox("show_description", label="Show collection description", default=True),
        Checkbox("show_image", label="Show collection image", default=False),
        Header("Sorting & filtering"),
        Checkbox("enable_sorting", label="Enable sorting", default=True),
        Checkbox("enable_filtering", label="Enable filtering", default=True),
    ]

    presets = [
        SectionPreset(name="Product grid", settings={
            "products_per_page": 24,
            "columns_mobile": 2,
            "columns_desktop": 4,
            "image_ratio": "adapt",
            "show_vendor": False,
            "show_quick_add": False,
            "enable_sorting": True,
            "enable_filtering": True,
        }),
    ]

    template = """
{%- comment -%} Collection / search product grid section {%- endcomment -%}
<section class="collection-product-grid" {{ section.shopify_attributes }}>
  <div class="page-width">
    {%- if section.settings.show_title and collection -%}
      <div class="collection__header">
        {%- if section.settings.show_image and collection.image -%}
          <div class="collection__image">
            {{ collection.image | image_url: width: 400 | image_tag:
              alt: collection.title | escape,
              sizes: '400px',
              loading: 'eager'
            }}
          </div>
        {%- endif -%}
        <div class="collection__info">
          <h1 class="collection__title">{{ collection.title }}</h1>
          {%- if section.settings.show_description and collection.description != '' -%}
            <div class="collection__description">{{ collection.description }}</div>
          {%- endif -%}
        </div>
      </div>
    {%- endif -%}

    <div class="collection__toolbar">
      {%- if section.settings.enable_filtering -%}
        <button
          type="button"
          class="collection__filter-btn"
          data-action="toggle-filters"
          aria-controls="collection-filters"
        >
          {%- render 'icon-filter' -%}
          {{ 'collections.filters.filter' | t }}
        </button>
      {%- endif -%}

      <div class="collection__results">
        {%- if collection -%}
          <span>{{ collection.all_products_count }} {{ 'collections.filters.results' | t }}</span>
        {%- elsif search -%}
          <span>{{ search.results_count }} {{ 'search.results' | t }}</span>
        {%- endif -%}
      </div>

      {%- if section.settings.enable_sorting -%}
        <div class="collection__sort">
          <label for="sort-by" class="visually-hidden">{{ 'collections.sorting.label' | t }}</label>
          <select id="sort-by" class="form-field__input form-field__select" data-sort-by>
            <option value="manual">{{ 'collections.sorting.manual' | t }}</option>
            <option value="best-selling">{{ 'collections.sorting.best_selling' | t }}</option>
            <option value="title-ascending">{{ 'collections.sorting.title_asc' | t }}</option>
            <option value="title-descending">{{ 'collections.sorting.title_desc' | t }}</option>
            <option value="price-ascending">{{ 'collections.sorting.price_asc' | t }}</option>
            <option value="price-descending">{{ 'collections.sorting.price_desc' | t }}</option>
            <option value="created-descending">{{ 'collections.sorting.newest' | t }}</option>
            <option value="created-ascending">{{ 'collections.sorting.oldest' | t }}</option>
          </select>
        </div>
      {%- endif -%}
    </div>

    <div class="collection__content">
      {%- if section.settings.enable_filtering -%}
        <aside class="collection__filters" id="collection-filters" aria-label="{{ 'collections.filters.label' | t }}">
          <div class="collection__filters-header">
            <h3>{{ 'collections.filters.label' | t }}</h3>
            <button type="button" class="collection__filters-close" data-action="close-filters" aria-label="Close filters">
              {%- render 'icon-close' -%}
            </button>
          </div>
          <div class="collection__filter-group">
            <h4>{{ 'collections.filters.availability' | t }}</h4>
            <label class="filter-checkbox">
              <input type="checkbox" data-filter="availability" value="in_stock">
              {{ 'collections.filters.in_stock' | t }}
            </label>
          </div>
          <div class="collection__filter-group">
            <h4>{{ 'collections.filters.price' | t }}</h4>
            <div class="filter-price">
              <input type="number" placeholder="Min" data-filter="price_min" class="form-field__input">
              <input type="number" placeholder="Max" data-filter="price_max" class="form-field__input">
            </div>
          </div>
        </aside>
      {%- endif -%}

      <div class="collection__grid-wrap">
        {%- paginate collection.products by section.settings.products_per_page -%}
          {%- if collection.products.size > 0 -%}
            <ul
              class="collection__grid"
              data-columns="{{ section.settings.columns_desktop }}"
              data-columns-mobile="{{ section.settings.columns_mobile }}"
            >
              {%- for product in collection.products -%}
                <li class="collection__item">
                  {%- render 'card-product',
                    product: product,
                    show_vendor: section.settings.show_vendor,
                    show_price: true,
                    show_rating: section.settings.show_rating,
                    show_quick_add: section.settings.show_quick_add,
                    image_ratio: section.settings.image_ratio,
                    secondary_image: section.settings.show_secondary_image,
                    grid_columns: section.settings.columns_desktop
                  -%}
                </li>
              {%- endfor -%}
            </ul>
          {%- else -%}
            <div class="collection__empty">
              <p>{{ 'collections.general.no_products' | t }}</p>
            </div>
          {%- endif -%}

          {%- render 'pagination', paginate: paginate -%}
        {%- endpaginate -%}
      </div>
    </div>
  </div>
</section>
    """

    styles = """
.collection-product-grid {
  padding: 2rem 0;
}

.page-width {
  max-width: var(--max-width, 1440px);
  margin: 0 auto;
  padding: 0 1.5rem;
}

.collection__header {
  display: flex;
  gap: 2rem;
  align-items: center;
  margin-bottom: 3rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid var(--color-border, #eee);
}

.collection__image {
  flex: 0 0 200px;
  border-radius: var(--radius-md, 8px);
  overflow: hidden;
}

.collection__title {
  font-family: var(--font-heading-family);
  font-size: 2.5rem;
  font-weight: 600;
  margin: 0 0 0.5rem;
}

.collection__description {
  font-size: 0.9375rem;
  color: var(--color-text-muted);
  line-height: 1.6;
  max-width: 600px;
}

.collection__toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.collection__filter-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: var(--color-surface, #fff);
  border: 1px solid var(--color-border, #ddd);
  border-radius: var(--radius-md, 6px);
  font-size: 0.875rem;
  cursor: pointer;
}

.collection__results {
  font-size: 0.875rem;
  color: var(--color-text-muted);
}

.collection__sort {
  min-width: 200px;
}

.collection__content {
  display: grid;
  gap: 2rem;
  grid-template-columns: 260px 1fr;
  align-items: start;
}

.collection__filters {
  position: sticky;
  top: 5rem;
}

.collection__filters-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.collection__filters h3 {
  font-family: var(--font-heading-family);
  font-size: 1.125rem;
  margin: 0;
}

.collection__filters-close {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  color: var(--color-text);
}

.collection__filter-group {
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--color-border, #eee);
}

.collection__filter-group h4 {
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin: 0 0 0.75rem;
}

.filter-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  cursor: pointer;
  padding: 0.25rem 0;
}

.filter-price {
  display: flex;
  gap: 0.5rem;
}

.filter-price input {
  flex: 1;
}

.collection__grid {
  display: grid;
  gap: var(--grid-gap, 1.5rem);
  grid-template-columns: repeat(2, 1fr);
  list-style: none;
  padding: 0;
  margin: 0;
}

.collection__grid[data-columns="3"] { grid-template-columns: repeat(3, 1fr); }
.collection__grid[data-columns="4"] { grid-template-columns: repeat(4, 1fr); }
.collection__grid[data-columns="5"] { grid-template-columns: repeat(5, 1fr); }
.collection__grid[data-columns="6"] { grid-template-columns: repeat(6, 1fr); }

.collection__empty {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--color-text-muted);
}

@media (max-width: 1023px) {
  .collection__content {
    grid-template-columns: 1fr;
  }
  .collection__filters {
    position: fixed;
    top: 0;
    left: 0;
    width: 85vw;
    max-width: 320px;
    height: 100vh;
    background: var(--color-background, #fff);
    padding: 1.5rem;
    z-index: 200;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
    overflow-y: auto;
  }
  .collection__filters:not([hidden]) {
    transform: translateX(0);
  }
  .collection__filters-close {
    display: inline-flex;
  }
}

@media (max-width: 767px) {
  .collection__header {
    flex-direction: column;
    text-align: center;
  }
  .collection__title { font-size: 1.75rem; }
  .collection__grid[data-columns-mobile="3"] { grid-template-columns: repeat(3, 1fr); }
}

@media (prefers-reduced-motion: reduce) {
  .collection__filters { transition: none; }
}
    """


SectionRegistry.register(MainCollectionProductGridSection)
