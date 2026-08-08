"""Breadcrumb navigation snippet with JSON-LD structured data."""
from ...core.snippet import Snippet, SnippetRegistry


BREADCRUMB_CSS = """
.breadcrumb {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8125rem;
  color: var(--color-text-muted);
  margin: 1rem 0;
}

.breadcrumb__item {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.breadcrumb__link {
  color: var(--color-text-muted);
  text-decoration: none;
}

.breadcrumb__link:hover {
  color: var(--color-text);
  text-decoration: underline;
}

.breadcrumb__separator {
  opacity: 0.5;
}

.breadcrumb__current {
  color: var(--color-text);
  font-weight: 500;
}
"""

breadcrumb_snippet = Snippet(
    name="breadcrumb",
    template="""{% comment %}
  Renders breadcrumb navigation with schema.org structured data.
  Usage:
    {% render 'breadcrumb' %}
{% endcomment %}

{%- assign _crumbs = '' | split: '' -%}

{%- if template == 'product' -%}
  {%- assign _collection = product.selected_or_first_available_variant.product.collections.first -%}
  {%- capture _item1 -%}
    {"@type":"ListItem","position":1,"name":"{{ 'general.home' | t }}","item":"{{ routes.root_url }}"}
  {%- endcapture -%}
  {%- if _collection -%}
    {%- capture _item2 -%}
      {"@type":"ListItem","position":2,"name":"{{ _collection.title }}","item":"{{ _collection.url }}"}
    {%- endcapture -%}
    {%- assign _crumbs = _crumbs | push: _item1 | push: _item2 -%}
  {%- else -%}
    {%- assign _crumbs = _crumbs | push: _item1 -%}
  {%- endif -%}
  {%- capture _item_last -%}
    {"@type":"ListItem","position":{{ _crumbs.size | plus: 1 }},"name":"{{ product.title }}"}
  {%- endcapture -%}
  {%- assign _crumbs = _crumbs | push: _item_last -%}
{%- elsif template == 'collection' -%}
  {%- capture _item1 -%}
    {"@type":"ListItem","position":1,"name":"{{ 'general.home' | t }}","item":"{{ routes.root_url }}"}
  {%- endcapture -%}
  {%- capture _item2 -%}
    {"@type":"ListItem","position":2,"name":"{{ collection.title }}"}
  {%- endcapture -%}
  {%- assign _crumbs = _crumbs | push: _item1 | push: _item2 -%}
{%- elsif template == 'page' -%}
  {%- capture _item1 -%}
    {"@type":"ListItem","position":1,"name":"{{ 'general.home' | t }}","item":"{{ routes.root_url }}"}
  {%- endcapture -%}
  {%- capture _item2 -%}
    {"@type":"ListItem","position":2,"name":"{{ page.title }}"}
  {%- endcapture -%}
  {%- assign _crumbs = _crumbs | push: _item1 | push: _item2 -%}
{%- endif -%}

{%- if _crumbs.size > 1 -%}
  <nav class="breadcrumb" aria-label="{{ 'general.breadcrumb' | t }}">
    <script type="application/ld+json">
      {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [{{ _crumbs | join: ',' }}]
      }
    </script>
    {%- for crumb in _crumbs -%}
      {%- assign _crumb_data = crumb -%}
    {%- endfor -%}

    <span class="breadcrumb__item">
      <a href="{{ routes.root_url }}" class="breadcrumb__link">{{ 'general.home' | t }}</a>
    </span>
    {%- if template == 'product' and _collection -%}
      <span class="breadcrumb__separator">/</span>
      <span class="breadcrumb__item">
        <a href="{{ _collection.url }}" class="breadcrumb__link">{{ _collection.title }}</a>
      </span>
    {%- endif -%}
    <span class="breadcrumb__separator">/</span>
    <span class="breadcrumb__item breadcrumb__current">
      {%- if template == 'product' -%}{{ product.title }}
      {%- elsif template == 'collection' -%}{{ collection.title }}
      {%- elsif template == 'page' -%}{{ page.title }}
      {%- endif -%}
    </span>
  </nav>
{%- endif -%}
""",
    params=[],
    styles=BREADCRUMB_CSS,
)

SnippetRegistry.register(breadcrumb_snippet)
