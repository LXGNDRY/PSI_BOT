"""
Badge snippet — sale, sold out, new, custom badges.
"""
from ...core.snippet import Snippet, SnippetRegistry


BADGE_CSS = """
.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.25rem 0.625rem;
  font-size: 0.6875rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  line-height: 1.2;
  text-transform: uppercase;
  border-radius: var(--radius-sm, 3px);
  white-space: nowrap;
  font-family: var(--font-body-family);
}

.badge--sale {
  background: var(--color-error, #e53935);
  color: #fff;
}

.badge--sold-out {
  background: var(--color-surface, #f5f5f5);
  color: var(--color-text-muted);
  border: 1px solid var(--color-border);
}

.badge--new {
  background: var(--color-accent, #2563eb);
  color: #fff;
}

.badge--custom {
  background: var(--color-accent);
  color: #fff;
}

.badge--top-left {
  position: absolute;
  top: 0.75rem;
  left: 0.75rem;
}

.badge--top-right {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
}

.badge--bottom-left {
  position: absolute;
  bottom: 0.75rem;
  left: 0.75rem;
}

.badge--bottom-right {
  position: absolute;
  bottom: 0.75rem;
  right: 0.75rem;
}
"""


badge_snippet = Snippet(
    name="badge",
    template="""{% comment %}
  Renders a badge.
  Usage:
    {% render 'badge', text: 'Sale', type: 'sale', position: 'top-left' %}
{% endcomment %}

{%- assign _text = text | default: '' -%}
{%- assign _type = type | default: 'custom' -%}
{%- assign _position = position | default: 'top-left' -%}

{%- if _text != '' -%}
  <span class="badge badge--{{ _type }} badge--{{ _position }}">{{ _text }}</span>
{%- endif -%}
""",
    params=["text", "type", "position"],
    styles=BADGE_CSS,
)

SnippetRegistry.register(badge_snippet)
