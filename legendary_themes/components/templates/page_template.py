"""Page template."""
from ...core.template import Template, TemplateSection, TemplateRegistry


page_template = Template(
    name="page",
    sections=[
        TemplateSection(id="main", type="main-page", settings={}),
    ],
    order=["main"],
)

TemplateRegistry.register(page_template)
