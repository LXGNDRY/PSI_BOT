"""Featured collection section."""
from ...core.section import Section, SectionPreset, SectionRegistry
from ...core.setting import (
    Text, Collection, Select, SelectOption, Checkbox, Header, Number, Url, Range,
)


class FeaturedCollectionSection(Section):
    type = "featured-collection"
    name = "Featured collection"
    tag = "section"
    class_name = "featured-collection"
    available_on = ["index", "product", "collection", "page"]

    settings = [
        Header("Content"),
        Text("heading", label="Heading", default="Featured collection"),
        Collection("collection", label="Collection"),
        Header("Layout"),
        Range("products_per_row", label="Products per row",
              min=2, max=6, step=1, default=4, unit="products"),
        Range("products_to_show", label="Products to show",
              min=2, max=12, step=2, default=8, unit="products"),
        Select("image_ratio", label="Image aspect ratio",
               options=[
                   SelectOption("adapt", "Adapt to image"),
                   SelectOption("square", "Square (1:1)"),
                   SelectOption("portrait", "Portrait (4:5)"),
                   SelectOption("landscape", "Landscape (3:2)"),
               ],
               default="adapt"),
        Header("Product card"),
        Checkbox("show_vendor", label="Show vendor", default=False),
        Checkbox("show_price", label="Show price", default=True),
        Checkbox("show_rating", label="Show star rating", default=False),
        Checkbox("show_quick_add", label="Show quick add button", default=False),
        Checkbox("show_secondary_image", label="Show second image on hover", default=False),
        Header("View all link"),
        Checkbox("show_view_all", label="Show 'View all' link", default=True),
        Text("view_all_text", label="View all text", default="View all"),
    ]

    presets = [
        SectionPreset(name="Featured collection", settings={
            "heading": "Featured collection",
            "products_per_row": 4,
            "products_to_show": 8,
            "image_ratio": "adapt",
            "show_price": True,
            "show_view_all": True,
            "view_all_text": "View all",
        }),
    ]

    template = """
<section class="featured-collection" {{ section.shopify_attributes }}>
  <div class="page-width">
    <div class="featured-collection__header">
      {%- if section.settings.heading -%}
        <h2 class="featured-collection__heading">{{ section.settings.heading }}</h2>
      {%- endif -%}
      {%- if section.settings.show_view_all and section.settings.collection -%}
        <a href="{{ section.settings.collection.url }}" class="featured-collection__view-all">
          {{ section.settings.view_all_text }}
          {%- render 'icon-arrow-right' -%}
        </a>
      {%- endif -%}
    </div>

    {%- if section.settings.collection and section.settings.collection.products.size > 0 -%}
      <div
        class="featured-collection__grid"
        data-columns="{{ section.settings.products_per_row }}"
      >
        {%- for product in section.settings.collection.products limit: section.settings.products_to_show -%}
          <div class="featured-collection__item">
            {%- render 'card-product',
              product: product,
              show_vendor: section.settings.show_vendor,
              show_price: section.settings.show_price,
              show_rating: section.settings.show_rating,
              show_quick_add: section.settings.show_quick_add,
              image_ratio: section.settings.image_ratio,
              secondary_image: section.settings.show_secondary_image,
              grid_columns: section.settings.products_per_row
            -%}
          </div>
        {%- endfor -%}
      </div>
    {%- else -%}
      <div class="featured-collection__empty">
        <p>{{ 'sections.featured_collection.empty' | t }}</p>
      </div>
    {%- endif -%}
  </div>
</section>
    """

    styles = """
.featured-collection {
  padding: 3rem 0;
}

.featured-collection__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
  gap: 1rem;
  flex-wrap: wrap;
}

.featured-collection__heading {
  font-family: var(--font-heading-family);
  font-size: clamp(1.5rem, 3vw, 2.25rem);
  font-weight: 600;
  margin: 0;
}

.featured-collection__view-all {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-text);
  text-decoration: none;
}

.featured-collection__view-all:hover {
  text-decoration: underline;
}

.featured-collection__grid {
  display: grid;
  gap: var(--grid-gap, 1.5rem);
  grid-template-columns: repeat(2, 1fr);
}

.featured-collection__grid[data-columns="3"] { grid-template-columns: repeat(3, 1fr); }
.featured-collection__grid[data-columns="4"] { grid-template-columns: repeat(4, 1fr); }
.featured-collection__grid[data-columns="5"] { grid-template-columns: repeat(5, 1fr); }
.featured-collection__grid[data-columns="6"] { grid-template-columns: repeat(6, 1fr); }

.featured-collection__empty {
  text-align: center;
  padding: 3rem;
  color: var(--color-text-muted);
  background: var(--color-surface, #f9f9f9);
  border-radius: var(--radius-md, 8px);
}

@media (max-width: 1023px) {
  .featured-collection__grid[data-columns="5"],
  .featured-collection__grid[data-columns="6"] {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 767px) {
  .featured-collection__grid,
  .featured-collection__grid[data-columns="3"],
  .featured-collection__grid[data-columns="4"],
  .featured-collection__grid[data-columns="5"],
  .featured-collection__grid[data-columns="6"] {
    grid-template-columns: repeat(2, 1fr);
  }
}
    """


SectionRegistry.register(FeaturedCollectionSection)
