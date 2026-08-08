"""Blog template."""
from ...core.template import Template, TemplateSection, TemplateRegistry


blog_template = Template(
    name="blog",
    sections=[
        TemplateSection(id="main", type="main-blog", settings={}),
    ],
    order=["main"],
)

TemplateRegistry.register(blog_template)
