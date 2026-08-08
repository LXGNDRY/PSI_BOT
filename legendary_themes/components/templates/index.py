"""Index (homepage) template."""
from ...core.template import Template, TemplateSection, TemplateRegistry


index_template = Template(
    name="index",
    sections=[
        TemplateSection(id="banner", type="image-banner", settings={}),
        TemplateSection(id="featured", type="featured-collection", settings={}),
        TemplateSection(id="rich", type="rich-text", settings={}),
    ],
    order=["banner", "featured", "rich"],
)

TemplateRegistry.register(index_template)
