"""Cart template."""
from ...core.template import Template, TemplateSection, TemplateRegistry


cart_template = Template(
    name="cart",
    sections=[
        TemplateSection(id="main", type="main-cart-items", settings={}),
    ],
    order=["main"],
)

TemplateRegistry.register(cart_template)
