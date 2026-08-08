"""Password (coming soon) template."""
from ...core.template import Template, TemplateSection, TemplateRegistry


password_template = Template(
    name="password",
    sections=[
        TemplateSection(id="main", type="password-main", settings={}),
    ],
    order=["main"],
)

TemplateRegistry.register(password_template)
