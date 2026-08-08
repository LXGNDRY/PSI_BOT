"""
Button snippet — reusable button component with multiple variants.
"""
from ...core.snippet import Snippet, SnippetRegistry


BUTTON_CSS = """
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  font-family: var(--font-body-family);
  font-size: 0.875rem;
  font-weight: 600;
  line-height: 1.2;
  text-align: center;
  text-decoration: none;
  border: none;
  border-radius: var(--radius-md, 6px);
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  user-select: none;
}

.btn:focus-visible {
  outline: 2px solid var(--color-accent, #2563eb);
  outline-offset: 2px;
}

.btn:disabled,
.btn[aria-disabled="true"] {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn--primary {
  background: var(--color-primary, #111);
  color: var(--color-surface, #fff);
}

.btn--primary:hover:not(:disabled) {
  opacity: 0.9;
}

.btn--secondary {
  background: transparent;
  color: var(--color-primary, #111);
  border: 1px solid var(--color-primary, #111);
}

.btn--secondary:hover:not(:disabled) {
  background: var(--color-primary, #111);
  color: var(--color-surface, #fff);
}

.btn--tertiary {
  background: transparent;
  color: var(--color-primary, #111);
  padding: 0.5rem 1rem;
}

.btn--tertiary:hover:not(:disabled) {
  text-decoration: underline;
}

.btn--small { padding: 0.5rem 1rem; font-size: 0.8125rem; }
.btn--large { padding: 1rem 2rem; font-size: 1rem; }
.btn--full { width: 100%; }

.btn__icon {
  display: inline-flex;
  width: 1em;
  height: 1em;
}

.btn--loading {
  pointer-events: none;
}

.btn--loading::after {
  content: '';
  width: 1em;
  height: 1em;
  margin-left: 0.5rem;
  border: 2px solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: spin 0.75s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (prefers-reduced-motion: reduce) {
  .btn { transition: none; }
  .btn--loading::after { animation: none; }
}
"""


button_snippet = Snippet(
    name="button",
    template="""{% comment %}
  Renders a button.
  Usage:
    {% render 'button', text: 'Add to cart', variant: 'primary', size: 'medium', full: true %}
  Parameters:
    - text: string (required)
    - variant: 'primary' | 'secondary' | 'tertiary' (default: 'primary')
    - size: 'small' | 'medium' | 'large' (default: 'medium')
    - full: boolean (default: false)
    - type: 'button' | 'submit' | 'link' (default: 'button')
    - url: string (for link variant)
    - icon: string (icon name)
    - disabled: boolean (default: false)
    - classes: string (additional classes)
{% endcomment %}

{%- assign _variant = variant | default: 'primary' -%}
{%- assign _size = size | default: 'medium' -%}
{%- assign _type = type | default: 'button' -%}

{%- capture _classes -%}
  btn btn--{{ _variant }} btn--{{ _size }}
  {%- if full %} btn--full{% endif -%}
  {%- if classes %} {{ classes }}{% endif -%}
{%- endcapture -%}

{%- if _type == 'link' and url -%}
  <a href="{{ url }}" class="{{ _classes | strip_newlines }}" {% if disabled %}aria-disabled="true"{% endif %}>
    {%- if icon -%}{%- render 'icon-' | append: icon -%}{%- endif -%}
    <span>{{ text }}</span>
  </a>
{%- else -%}
  <button type="{{ _type }}" class="{{ _classes | strip_newlines }}" {% if disabled %}disabled{% endif %}>
    {%- if icon -%}{%- render 'icon-' | append: icon -%}{%- endif -%}
    <span>{{ text }}</span>
  </button>
{%- endif -%}
""",
    params=["text", "variant", "size", "full", "type", "url", "icon", "disabled", "classes"],
    styles=BUTTON_CSS,
)

SnippetRegistry.register(button_snippet)
