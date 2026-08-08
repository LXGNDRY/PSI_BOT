"""Collection template."""
from ...core.template import Template, TemplateSection, TemplateRegistry


collection_template = Template(
    name="collection",
    sections=[
        TemplateSection(id="main", type="main-collection-product-grid", settings={}),
    ],
    order=["main"],
)

TemplateRegistry.register(collection_template)
