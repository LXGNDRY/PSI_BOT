"""List collections template."""
from ...core.template import Template, TemplateSection, TemplateRegistry


list_collections_template = Template(
    name="list-collections",
    sections=[
        TemplateSection(id="main", type="list-collections", settings={}),
    ],
    order=["main"],
)

TemplateRegistry.register(list_collections_template)
