"""
Theme Store compliance rules engine.
Every rule returns a list of issues (empty = passes).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .manifest import ThemeManifest


@dataclass
class RuleIssue:
    severity: str  # "error" | "warning" | "info"
    rule_id: str
    message: str
    affected: Optional[str] = None


class ThemeStoreRules:
    """Static rules that every generated theme must pass."""

    REQUIRED_TEMPLATES = [
        "404", "article", "blog", "cart", "collection", "index",
        "list-collections", "page", "search", "password", "product",
        "gift_card", "page.contact",
    ]

    REQUIRED_SECTIONS = [
        "header", "footer", "main-product", "main-collection-product-grid",
        "featured-collection", "rich-text", "image-banner",
        "custom-liquid",
    ]

    MANDATORY_FEATURES = [
        "sections_everywhere", "discounts", "accelerated_checkout",
        "faceted_filtering", "gift_card", "focal_points", "social_image",
        "country_selector", "language_selector", "multi_level_menus",
        "newsletter", "pickup_availability", "recommendations",
        "complementary_products", "rich_product_media", "predictive_search",
        "selling_plans", "shop_pay_installments", "unit_pricing",
        "variant_images", "follow_on_shop",
    ]

    @classmethod
    def validate_manifest(cls, manifest: "ThemeManifest") -> List[RuleIssue]:
        """Run all manifest-level rules."""
        issues: List[RuleIssue] = []
        issues.extend(cls._check_presets(manifest))
        issues.extend(cls._check_performance_targets(manifest))
        issues.extend(cls._check_accessibility(manifest))
        issues.extend(cls._check_required_features(manifest))
        return issues

    @classmethod
    def _check_presets(cls, m: "ThemeManifest") -> List[RuleIssue]:
        issues = []
        if len(m.presets) < 1:
            issues.append(RuleIssue(
                "error", "R001",
                "Theme must have at least one preset"
            ))
        if len(m.presets) > 6:
            issues.append(RuleIssue(
                "warning", "R002",
                "Theme Store recommends max 6 presets"
            ))
        return issues

    @classmethod
    def _check_performance_targets(cls, m: "ThemeManifest") -> List[RuleIssue]:
        issues = []
        if m.performance.target_lighthouse_mobile < 60:
            issues.append(RuleIssue(
                "error", "R101",
                "Mobile Lighthouse target below Theme Store minimum (60)"
            ))
        if m.performance.target_lighthouse_mobile < 80:
            issues.append(RuleIssue(
                "warning", "R102",
                f"Mobile Lighthouse target ({m.performance.target_lighthouse_mobile}) "
                "is below premium target (85+)"
            ))
        if m.performance.max_js_payload_kb > 150:
            issues.append(RuleIssue(
                "warning", "R103",
                f"JS payload budget ({m.performance.max_js_payload_kb} KB) "
                "is high — premium themes target < 80 KB"
            ))
        return issues

    @classmethod
    def _check_accessibility(cls, m: "ThemeManifest") -> List[RuleIssue]:
        issues = []
        if not m.accessibility.skip_link:
            issues.append(RuleIssue(
                "error", "R201",
                "Skip-to-content link is required for WCAG compliance"
            ))
        if not m.accessibility.keyboard_navigation:
            issues.append(RuleIssue(
                "error", "R202",
                "Keyboard navigation is required for Theme Store"
            ))
        if m.accessibility.wcag_target == "A":
            issues.append(RuleIssue(
                "warning", "R203",
                "WCAG Level A is below Theme Store minimum (AA)"
            ))
        return issues

    @classmethod
    def _check_required_features(cls, m: "ThemeManifest") -> List[RuleIssue]:
        issues = []
        if not m.filters.enabled:
            issues.append(RuleIssue(
                "error", "R301",
                "Faceted search filtering is required for Theme Store"
            ))
        if not m.search.predictive:
            issues.append(RuleIssue(
                "warning", "R302",
                "Predictive search is strongly recommended for premium themes"
            ))
        if m.cart.style == "page" and not m.cart.ajax:
            issues.append(RuleIssue(
                "warning", "R303",
                "AJAX cart is recommended for better conversion UX"
            ))
        if m.nav.mega_menu and m.nav.multi_level < 3:
            issues.append(RuleIssue(
                "warning", "R304",
                "Mega menu with fewer than 3 levels may be unnecessary"
            ))
        return issues

    @classmethod
    def validate_output(cls, file_index: dict) -> List[RuleIssue]:
        """Validate the generated file structure."""
        issues: List[RuleIssue] = []
        # Check required directories
        for d in ["assets", "config", "layout", "locales", "sections", "snippets", "templates"]:
            if d not in file_index.get("dirs", []):
                issues.append(RuleIssue(
                    "error", "R401",
                    f"Missing required directory: {d}"
                ))
        # Check required layout file
        if "layout/theme.liquid" not in file_index.get("files", []):
            issues.append(RuleIssue(
                "error", "R402",
                "Missing required file: layout/theme.liquid"
            ))
        # Check required locale file
        if "locales/en.default.json" not in file_index.get("files", []):
            issues.append(RuleIssue(
                "error", "R403",
                "Missing required locale: locales/en.default.json"
            ))
        # Check required config files
        for f in ["config/settings_schema.json", "config/settings_data.json"]:
            if f not in file_index.get("files", []):
                issues.append(RuleIssue(
                    "error", "R404",
                    f"Missing required config file: {f}"
                ))
        return issues
