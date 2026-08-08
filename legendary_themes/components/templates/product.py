"""Product template."""
from ...core.template import Template, TemplateSection, TemplateRegistry


product_template = Template(
    name="product",
    sections=[
        TemplateSection(id="main", type="main-product", settings={}),
        TemplateSection(id="recommendations", type="product-recommendations", settings={}),
    ],
    order=["main", "recommendations"],
)

TemplateRegistry.register(product_template)
