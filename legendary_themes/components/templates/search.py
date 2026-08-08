"""Search template."""
from ...core.template import Template, TemplateSection, TemplateRegistry


search_template = Template(
    name="search",
    sections=[
        TemplateSection(id="main", type="main-collection-product-grid", settings={}),
    ],
    order=["main"],
)

TemplateRegistry.register(search_template)
