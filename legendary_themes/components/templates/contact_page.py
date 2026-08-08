"""Contact page template (page.contact.json)."""
from ...core.template import Template, TemplateSection, TemplateRegistry


contact_template = Template(
    name="page.contact",
    sections=[
        TemplateSection(id="main", type="contact-form", settings={}),
    ],
    order=["main"],
)

TemplateRegistry.register(contact_template)
