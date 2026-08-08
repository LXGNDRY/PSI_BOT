"""
Schema generator — produces settings_schema.json and settings_data.json
from the manifest and section registry.
"""
from __future__ import annotations

import json
from typing import TYPE_CHECKING, List, Dict, Any

from ..core.setting import Header, Color, FontPicker, Checkbox, Range, Select
from ..core.section import SectionRegistry

if TYPE_CHECKING:
    from ..core.manifest import ThemeManifest


class SchemaGenerator:
    """Generates config/settings_schema.json and config/settings_data.json."""

    def __init__(self, manifest: "ThemeManifest"):
        self.manifest = manifest
        self.preset = manifest.presets[manifest.default_preset]

    def settings_schema_json(self) -> str:
        """Generate the complete settings_schema.json."""
        m = self.manifest
        p = self.preset

        schema: List[Dict[str, Any]] = []

        # Theme info block
        schema.append({
            "name": "theme_info",
            "theme_name": m.name,
            "theme_author": m.author,
            "theme_version": m.version,
            "theme_documentation_url": "",
            "theme_support_url": "",
        })

        # Colors
        schema.append({
            "name": "t:settings_schema.colors.name",
            "settings": [
                {"type": "header", "content": "t:settings_schema.colors.settings.header__1.content"},
                {
                    "type": "color_palette",
                    "id": "colors",
                    "default": {
                        "primary": p.palette.primary,
                        "secondary": p.palette.secondary,
                        "accent": p.palette.accent,
                        "background": p.palette.background,
                        "surface": p.palette.surface,
                        "text": p.palette.text,
                        "text_muted": p.palette.text_muted,
                        "border": p.palette.border,
                        "success": p.palette.success or "#10b981",
                        "error": p.palette.error or "#ef4444",
                    },
                },
                {
                    "type": "color_scheme_group",
                    "id": "color_schemes",
                    "definition": [
                        {"type": "color", "id": "background", "label": "Background", "default": p.palette.background},
                        {"type": "color", "id": "text", "label": "Text", "default": p.palette.text},
                        {"type": "color", "id": "accent", "label": "Accent", "default": p.palette.accent},
                        {"type": "color", "id": "card", "label": "Card / Surface", "default": p.palette.surface},
                        {"type": "color", "id": "card_text", "label": "Card text", "default": p.palette.text},
                        {"type": "color", "id": "button", "label": "Button background", "default": p.palette.primary},
                        {"type": "color", "id": "button_text", "label": "Button text", "default": p.palette.surface},
                        {"type": "color", "id": "border", "label": "Border", "default": p.palette.border},
                    ],
                    "role": {
                        "text": "text",
                        "background": {"solid": "background", "gradient": ""},
                        "links": "accent",
                        "icons": "text",
                        "primary_button": "button",
                        "on_primary_button": "button_text",
                        "primary_button_border": "button",
                        "secondary_button": "card",
                        "on_secondary_button": "card_text",
                        "secondary_button_border": "border",
                    },
                },
            ],
        })

        # Typography
        schema.append({
            "name": "t:settings_schema.typography.name",
            "settings": [
                {"type": "header", "content": "t:settings_schema.typography.settings.heading_font.content"},
                {
                    "type": "font_picker",
                    "id": "heading_font",
                    "label": "t:settings_schema.typography.settings.heading_font.label",
                    "default": p.typography.heading_font,
                },
                {
                    "type": "range",
                    "id": "heading_scale",
                    "label": "t:settings_schema.typography.settings.heading_scale.label",
                    "min": 1.1,
                    "max": 1.6,
                    "step": 0.05,
                    "default": p.typography.heading_scale,
                    "unit": "x",
                },
                {"type": "header", "content": "t:settings_schema.typography.settings.body_font.content"},
                {
                    "type": "font_picker",
                    "id": "body_font",
                    "label": "t:settings_schema.typography.settings.body_font.label",
                    "default": p.typography.body_font,
                },
                {
                    "type": "range",
                    "id": "base_font_size",
                    "label": "t:settings_schema.typography.settings.base_font_size.label",
                    "min": 12,
                    "max": 24,
                    "step": 1,
                    "default": p.typography.base_font_size,
                    "unit": "px",
                },
                {
                    "type": "range",
                    "id": "body_line_height",
                    "label": "t:settings_schema.typography.settings.body_line_height.label",
                    "min": 1.3,
                    "max": 2,
                    "step": 0.1,
                    "default": p.typography.body_line_height,
                },
            ],
        })

        # Layout
        schema.append({
            "name": "t:settings_schema.layout.name",
            "settings": [
                {"type": "header", "content": "t:settings_schema.layout.settings.max_width.content"},
                {
                    "type": "range",
                    "id": "max_width",
                    "label": "t:settings_schema.layout.settings.max_width.label",
                    "min": 1000,
                    "max": 1800,
                    "step": 20,
                    "default": 1440,
                    "unit": "px",
                },
                {
                    "type": "range",
                    "id": "grid_gap",
                    "label": "t:settings_schema.layout.settings.grid_gap.label",
                    "min": 8,
                    "max": 64,
                    "step": 4,
                    "default": p.spacing.grid_gap,
                    "unit": "px",
                },
                {
                    "type": "range",
                    "id": "section_padding",
                    "label": "t:settings_schema.layout.settings.section_padding.label",
                    "min": 24,
                    "max": 128,
                    "step": 8,
                    "default": p.spacing.section_padding,
                    "unit": "px",
                },
            ],
        })

        # Cart
        schema.append({
            "name": "t:settings_schema.cart.name",
            "settings": [
                {
                    "type": "select",
                    "id": "cart_type",
                    "label": "t:settings_schema.cart.settings.cart_type.label",
                    "options": [
                        {"value": "drawer", "label": "Drawer"},
                        {"value": "page", "label": "Page"},
                    ],
                    "default": m.cart.style,
                },
                {
                    "type": "checkbox",
                    "id": "cart_notification",
                    "label": "t:settings_schema.cart.settings.cart_notification.label",
                    "default": True,
                },
            ],
        })

        # Search
        schema.append({
            "name": "t:settings_schema.search.name",
            "settings": [
                {
                    "type": "checkbox",
                    "id": "predictive_search",
                    "label": "t:settings_schema.search.settings.predictive_search.label",
                    "default": m.search.predictive,
                },
                {
                    "type": "checkbox",
                    "id": "show_search_images",
                    "label": "t:settings_schema.search.settings.show_images.label",
                    "default": m.search.show_images,
                },
                {
                    "type": "checkbox",
                    "id": "show_search_prices",
                    "label": "t:settings_schema.search.settings.show_prices.label",
                    "default": m.search.show_prices,
                },
            ],
        })

        # Enable/disable features that have global toggle
        schema.append({
            "name": "t:settings_schema.features.name",
            "settings": [
                {"type": "header", "content": "t:settings_schema.features.settings.product.content"},
                {
                    "type": "checkbox",
                    "id": "show_vendor",
                    "label": "t:settings_schema.features.settings.show_vendor.label",
                    "default": m.product.show_vendor,
                },
                {
                    "type": "checkbox",
                    "id": "recently_viewed",
                    "label": "t:settings_schema.features.settings.recently_viewed.label",
                    "default": m.features.recently_viewed,
                },
            ],
        })

        # Social media
        schema.append({
            "name": "t:settings_schema.social.name",
            "settings": [
                {"type": "url", "id": "social_facebook", "label": "Facebook", "default": ""},
                {"type": "url", "id": "social_instagram", "label": "Instagram", "default": ""},
                {"type": "url", "id": "social_twitter", "label": "Twitter", "default": ""},
                {"type": "url", "id": "social_tiktok", "label": "TikTok", "default": ""},
                {"type": "url", "id": "social_youtube", "label": "YouTube", "default": ""},
                {"type": "url", "id": "social_pinterest", "label": "Pinterest", "default": ""},
            ],
        })

        # Favicon
        schema.append({
            "name": "t:settings_schema.favicon.name",
            "settings": [
                {"type": "image_picker", "id": "favicon", "label": "Favicon"},
            ],
        })

        return json.dumps(schema, indent=2) + "\n"

    def settings_data_json(self) -> str:
        """Generate settings_data.json with defaults for all presets."""
        m = self.manifest

        data: Dict[str, Any] = {
            "current": "Default",
            "presets": {},
        }

        for i, preset in enumerate(m.presets):
            name = preset.name
            data["presets"][name] = {
                "settings": {
                    "colors": {
                        "primary": preset.palette.primary,
                        "secondary": preset.palette.secondary,
                        "accent": preset.palette.accent,
                        "background": preset.palette.background,
                        "surface": preset.palette.surface,
                        "text": preset.palette.text,
                        "text_muted": preset.palette.text_muted,
                        "border": preset.palette.border,
                    },
                    "heading_font": preset.typography.heading_font,
                    "body_font": preset.typography.body_font,
                    "base_font_size": preset.typography.base_font_size,
                    "heading_scale": preset.typography.heading_scale,
                    "body_line_height": preset.typography.body_line_height,
                    "max_width": 1440,
                    "grid_gap": preset.spacing.grid_gap,
                    "section_padding": preset.spacing.section_padding,
                    "cart_type": m.cart.style,
                    "predictive_search": m.search.predictive,
                    "show_search_images": m.search.show_images,
                    "show_search_prices": m.search.show_prices,
                    "show_vendor": m.product.show_vendor,
                    "recently_viewed": m.features.recently_viewed,
                },
                "sections": {
                    "header-group": {
                        "type": "header-group",
                        "settings": {},
                        "blocks": {},
                    },
                    "footer-group": {
                        "type": "footer-group",
                        "settings": {},
                        "blocks": {},
                    },
                },
                "content_for_index": [],
            }

            if i == m.default_preset:
                data["current"] = name

        return json.dumps(data, indent=2) + "\n"
