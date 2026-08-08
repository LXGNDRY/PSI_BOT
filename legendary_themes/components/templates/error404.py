"""404 template."""
from ...core.template import Template, TemplateSection, TemplateRegistry


error404_template = Template(
    name="404",
    sections=[
        TemplateSection(id="content", type="rich-text", settings={
            "heading": "Page not found",
            "text": "<p>The page you're looking for doesn't exist or has been moved.</p>",
            "show_button": True,
            "button_text": "Back to home",
            "button_url": "/",
        }),
    ],
    order=["content"],
)

TemplateRegistry.register(error404_template)
