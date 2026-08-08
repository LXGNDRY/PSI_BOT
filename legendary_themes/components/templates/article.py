"""Article (blog post) template."""
from ...core.template import Template, TemplateSection, TemplateRegistry


article_template = Template(
    name="article",
    sections=[
        TemplateSection(id="main", type="main-article", settings={}),
    ],
    order=["main"],
)

TemplateRegistry.register(article_template)
