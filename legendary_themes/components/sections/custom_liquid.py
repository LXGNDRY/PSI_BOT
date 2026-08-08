"""Custom Liquid section — required for Theme Store (app insertion point)."""
from ...core.section import Section, SectionPreset, SectionRegistry
from ...core.setting import Liquid, Header


class CustomLiquidSection(Section):
    type = "custom-liquid"
    name = "Custom Liquid"
    tag = "section"
    class_name = "custom-liquid"
    available_on = [
        "index", "collection", "product", "page", "blog", "article",
        "search", "404", "list-collections", "cart",
    ]

    settings = [
        Header("Custom Liquid"),
        Liquid("code", label="Liquid code", default=""),
    ]

    presets = [
        SectionPreset(name="Custom Liquid", settings={"code": ""}),
    ]

    template = """
<section class="custom-liquid" {{ section.shopify_attributes }}>
  <div class="page-width">
    {{ section.settings.code }}
  </div>
</section>
    """

    styles = """
.custom-liquid {
  padding: 2rem 0;
}
    """


SectionRegistry.register(CustomLiquidSection)
