"""
Theme composer — takes a manifest and produces a complete theme file tree.
This is the orchestrator that wires together all the pieces.
"""
from __future__ import annotations

import json
import os
from typing import Dict, List, Any, Optional, TYPE_CHECKING

from .manifest import ThemeManifest
from .rules import ThemeStoreRules, RuleIssue
from .section import SectionRegistry
from .snippet import SnippetRegistry
from .template import TemplateRegistry, Template, TemplateSection

if TYPE_CHECKING:
    pass


class ThemeComposer:
    """
    Orchestrates theme generation.
    Takes a manifest → produces a complete file index (path → content).
    """

    def __init__(self, manifest: ThemeManifest):
        self.manifest = manifest
        self.files: Dict[str, str] = {}
        self.issues: List[RuleIssue] = []

    def compose(self) -> Dict[str, str]:
        """Run the full composition pipeline and return file dict."""
        # Phase 1: Validate manifest
        self.issues.extend(ThemeStoreRules.validate_manifest(self.manifest))
        errors = [i for i in self.issues if i.severity == "error"]
        if errors:
            raise ValueError(
                f"Manifest has {len(errors)} errors: "
                + "; ".join(e.message for e in errors)
            )

        # Phase 2: Load components
        self._load_components()

        # Phase 3: Generate layout
        self._generate_layout()

        # Phase 4: Generate templates
        self._generate_templates()

        # Phase 5: Generate sections
        self._generate_sections()

        # Phase 6: Generate snippets
        self._generate_snippets()

        # Phase 7: Generate config
        self._generate_config()

        # Phase 8: Generate locales
        self._generate_locales()

        # Phase 9: Generate assets (CSS, JS, icons)
        self._generate_assets()

        # Phase 10: Validate output structure
        self._validate_output()

        return self.files

    def _load_components(self) -> None:
        """Register all built-in sections, snippets, and templates."""
        # Import triggers registration via decorators
        from ..components.sections import (  # noqa: F401
            header, footer, announcement_bar,
            main_product, main_collection_product_grid,
            image_banner, rich_text, featured_collection,
            custom_liquid, product_recommendations,
        )
        from ..components.snippets import (  # noqa: F401
            card_product, price, badge, button, icon_system,
            form_components, pagination, breadcrumb, product_media,
        )
        from ..components.templates import (  # noqa: F401
            index, product, collection, cart, page_template,
            search, error404, blog, article, list_collections, password,
            contact_page,
        )

    def _generate_layout(self) -> None:
        """Generate theme.liquid layout."""
        from ..generators.liquid_generator import LayoutGenerator
        gen = LayoutGenerator(self.manifest)
        content = gen.generate()
        self.files["layout/theme.liquid"] = content

    def _generate_templates(self) -> None:
        """Generate all JSON templates.

        If the manifest has section configurations for specific templates,
        those override the default template compositions.
        """
        # Build a set of templates from the registry (defaults)
        templates = dict(TemplateRegistry.all())

        # Check if manifest has sections config to override templates
        if hasattr(self.manifest, 'sections') and self.manifest.sections:
            for template_name, section_list in self.manifest.sections.items():
                from .template import Template, TemplateSection
                sections = []
                for s in section_list:
                    section_dict = s if isinstance(s, dict) else s.__dict__
                    sections.append(TemplateSection(
                        id=section_dict.get('id', section_dict.get('type', '')),
                        type=section_dict.get('type', ''),
                        settings=section_dict.get('settings', {}),
                    ))
                templates[template_name] = Template(
                    name=template_name,
                    sections=sections,
                )

        for name, template in templates.items():
            self.files[template.filename] = template.to_json()

        # Gift card template (only required .liquid template)
        self.files["templates/gift_card.liquid"] = self._gift_card_template()

        # Customer templates
        for tmpl in ["account", "login", "register", "addresses", "orders", "reset_password"]:
            self.files[f"templates/customers/{tmpl}.json"] = self._customer_template(tmpl)

    def _gift_card_template(self) -> str:
        return """{% layout 'gift_card' %}
{% comment %}Gift card template{% endcomment %}
<div class="gift-card">
  <h1 class="gift-card__title">{{ 'gift_card.title' | t }}</h1>
  <div class="gift-card__card">
    <h2>{{ shop.name }}</h2>
    <p class="gift-card__code">{{ gift_card.code | upcase }}</p>
    <p class="gift-card__amount">{{ gift_card.initial_value | money }}</p>
    <img src="{{ gift_card | qr_code: 240 }}" alt="{{ 'gift_card.qr_alt' | t }}">
  </div>
  <p class="gift-card__expiry">
    {% if gift_card.expires_on %}
      {{ 'gift_card.expires_on' | t: date: gift_card.expires_on | date: format: 'long' }}
    {% endif %}
  </p>
</div>
"""

    def _customer_template(self, name: str) -> str:
        section_type = f"main-customer-{name}"
        template = Template(
            name=f"customers/{name}",
            sections=[
                TemplateSection(id="main", type=section_type if False else "main-page"),
            ],
        )
        return template.to_json()

    def _generate_sections(self) -> None:
        """Generate all section .liquid files."""
        for name, section_cls in SectionRegistry.all().items():
            content = section_cls.render_liquid(self.manifest)
            if section_cls.is_group:
                self.files[f"sections/{name}.json"] = content
            else:
                self.files[f"sections/{name}.liquid"] = content

    def _generate_snippets(self) -> None:
        """Generate all snippet .liquid files."""
        for name, snippet in SnippetRegistry.all().items():
            self.files[f"snippets/{name}.liquid"] = snippet.render()

    def _generate_config(self) -> None:
        """Generate settings_schema.json and settings_data.json."""
        from ..generators.schema_generator import SchemaGenerator
        schema_gen = SchemaGenerator(self.manifest)
        self.files["config/settings_schema.json"] = schema_gen.settings_schema_json()
        self.files["config/settings_data.json"] = schema_gen.settings_data_json()

    def _generate_locales(self) -> None:
        """Generate locale files."""
        from ..generators.locale_generator import LocaleGenerator
        locale_gen = LocaleGenerator(self.manifest)
        self.files["locales/en.default.json"] = locale_gen.default_locale_json()

    def _generate_assets(self) -> None:
        """Generate CSS, JS, and icon assets."""
        from ..generators.css_generator import CSSGenerator
        from ..generators.js_generator import JSGenerator
        from ..generators.icon_generator import IconGenerator

        css_gen = CSSGenerator(self.manifest)
        for path, content in css_gen.generate().items():
            self.files[path] = content

        js_gen = JSGenerator(self.manifest)
        for path, content in js_gen.generate().items():
            self.files[path] = content

        icon_gen = IconGenerator()
        for path, content in icon_gen.generate().items():
            self.files[path] = content

    def _validate_output(self) -> None:
        """Validate output structure against Theme Store rules."""
        dirs = set()
        files_list = []
        for path in self.files.keys():
            parts = path.split("/")
            if len(parts) > 1:
                dirs.add(parts[0])
            if len(parts) > 2 and parts[0] == "templates":
                dirs.add("templates/" + parts[1])
            files_list.append(path)

        file_index = {"dirs": list(dirs), "files": files_list}
        self.issues.extend(ThemeStoreRules.validate_output(file_index))

    def audit_report(self) -> str:
        """Generate a markdown audit report."""
        lines = [
            f"# {self.manifest.name} — Generation Audit Report",
            "",
            f"**Version:** {self.manifest.version}",
            f"**Author:** {self.manifest.author}",
            f"**Vertical:** {self.manifest.vertical}",
            "",
            "## Summary",
            "",
            f"- **Files generated:** {len(self.files)}",
            f"- **Sections:** {len(SectionRegistry.all())}",
            f"- **Snippets:** {len(SnippetRegistry.all())}",
            f"- **Templates:** {len(TemplateRegistry.all()) + 7}",  # + customer templates + gift_card
            f"- **Issues found:** {len(self.issues)}",
            "",
        ]

        errors = [i for i in self.issues if i.severity == "error"]
        warnings = [i for i in self.issues if i.severity == "warning"]
        infos = [i for i in self.issues if i.severity == "info"]

        lines.extend([
            f"  - Errors: {len(errors)}",
            f"  - Warnings: {len(warnings)}",
            f"  - Info: {len(infos)}",
            "",
        ])

        if errors:
            lines.extend(["## Errors", ""])
            for e in errors:
                lines.append(f"- **[{e.rule_id}]** {e.message}")
                if e.affected:
                    lines.append(f"  - Affected: `{e.affected}`")
            lines.append("")

        if warnings:
            lines.extend(["## Warnings", ""])
            for w in warnings:
                lines.append(f"- **[{w.rule_id}]** {w.message}")
                if w.affected:
                    lines.append(f"  - Affected: `{w.affected}`")
            lines.append("")

        # File inventory
        lines.extend(["## File Inventory", ""])
        for path in sorted(self.files.keys()):
            lines.append(f"- `{path}`")

        return "\n".join(lines) + "\n"
