"""Pagination snippet."""
from ...core.snippet import Snippet, SnippetRegistry


PAGINATION_CSS = """
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin: 2rem 0;
}

.pagination__item {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 2.5rem;
  height: 2.5rem;
  padding: 0 0.75rem;
  border: 1px solid var(--color-border, #ddd);
  border-radius: var(--radius-md, 6px);
  font-size: 0.875rem;
  color: var(--color-text);
  text-decoration: none;
  background: var(--color-surface, #fff);
  transition: all 0.15s ease;
}

.pagination__item:hover:not(.pagination__item--active):not([aria-disabled]) {
  border-color: var(--color-primary, #111);
}

.pagination__item--active {
  background: var(--color-primary, #111);
  color: var(--color-surface, #fff);
  border-color: var(--color-primary, #111);
}

.pagination__item[aria-disabled="true"] {
  opacity: 0.4;
  pointer-events: none;
}
"""

pagination_snippet = Snippet(
    name="pagination",
    template="""{% comment %}
  Renders pagination controls.
  Usage:
    {% render 'pagination', paginate: paginate %}
{% endcomment %}

{%- if paginate.pages > 1 -%}
  <nav class="pagination" role="navigation" aria-label="{{ 'general.pagination' | t }}">
    {%- if paginate.previous -%}
      <a href="{{ paginate.previous.url }}" class="pagination__item" aria-label="{{ 'general.previous_page' | t }}">
        {%- render 'icon-chevron-left' -%}
      </a>
    {%- else -%}
      <span class="pagination__item" aria-disabled="true">
        {%- render 'icon-chevron-left' -%}
      </span>
    {%- endif -%}

    {%- for part in paginate.parts -%}
      {%- if part.is_link -%}
        <a href="{{ part.url }}" class="pagination__item">{{ part.title }}</a>
      {%- else -%}
        <span class="pagination__item {% if part.is_current %}pagination__item--active{% endif %}">
          {{ part.title }}
        </span>
      {%- endif -%}
    {%- endfor -%}

    {%- if paginate.next -%}
      <a href="{{ paginate.next.url }}" class="pagination__item" aria-label="{{ 'general.next_page' | t }}">
        {%- render 'icon-chevron-right' -%}
      </a>
    {%- else -%}
      <span class="pagination__item" aria-disabled="true">
        {%- render 'icon-chevron-right' -%}
      </span>
    {%- endif -%}
  </nav>
{%- endif -%}
""",
    params=["paginate"],
    styles=PAGINATION_CSS,
)

SnippetRegistry.register(pagination_snippet)
