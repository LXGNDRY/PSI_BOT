"""
Theme manifest — the complete input specification for generating a theme.
Validated with Pydantic for type safety and rule enforcement.
"""
from __future__ import annotations

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


class ThemePalette(BaseModel):
    """Color palette definition."""
    primary: str = Field(..., description="Primary brand color (hex)")
    secondary: str = Field(..., description="Secondary color (hex)")
    accent: str = Field(..., description="Accent color (hex)")
    background: str = Field(..., description="Background color (hex)")
    surface: str = Field(..., description="Surface/card color (hex)")
    text: str = Field(..., description="Text color (hex)")
    text_muted: str = Field(..., description="Muted text color (hex)")
    border: str = Field(..., description="Border color (hex)")
    success: Optional[str] = None
    error: Optional[str] = None
    warning: Optional[str] = None


class ThemeTypography(BaseModel):
    """Typography configuration."""
    heading_font: str = Field(default="inter_n7", description="Shopify font ID for headings")
    body_font: str = Field(default="inter_n4", description="Shopify font ID for body")
    base_font_size: int = Field(default=16, ge=12, le=24)
    heading_scale: float = Field(default=1.25, ge=1.1, le=1.5)
    body_line_height: float = Field(default=1.6, ge=1.3, le=2.0)


class ThemeSpacing(BaseModel):
    """Spacing scale."""
    base_unit: int = Field(default=4, ge=2, le=8)
    section_padding: int = Field(default=64, ge=24, le=128)
    grid_gap: int = Field(default=24, ge=8, le=64)


class ThemePreset(BaseModel):
    """A named style preset (merchant can switch between presets)."""
    name: str
    palette: ThemePalette
    typography: ThemeTypography
    spacing: ThemeSpacing = Field(default_factory=ThemeSpacing)


class HeaderConfig(BaseModel):
    style: str = Field(default="standard", pattern="^(minimal|standard|mega_menu|stacked)$")
    sticky: bool = True
    show_search: bool = True
    show_cart: bool = True
    show_account: bool = True
    announcement_bar: bool = True


class ProductConfig(BaseModel):
    card_style: str = Field(default="classic", pattern="^(classic|reveal|minimal|editorial)$")
    image_ratio: str = Field(default="adapt", pattern="^(adapt|square|portrait|landscape|widescreen)$")
    show_vendor: bool = False
    show_rating: bool = False
    quick_add: bool = True
    quick_view: bool = False
    sticky_add_to_cart: bool = True
    swatches: bool = True
    layout: str = Field(default="split", pattern="^(split|stacked|centered|fullwidth)$")


class CartConfig(BaseModel):
    style: str = Field(default="drawer", pattern="^(drawer|page|both)$")
    ajax: bool = True
    show_savings: bool = True
    upsell_products: bool = True


class NavConfig(BaseModel):
    mobile_style: str = Field(default="drawer", pattern="^(drawer|fullscreen|bottom)$")
    mega_menu: bool = True
    multi_level: int = Field(default=3, ge=1, le=5)


class SearchConfig(BaseModel):
    predictive: bool = True
    show_images: bool = True
    show_prices: bool = True
    result_types: List[str] = Field(default_factory=lambda: ["product", "collection", "page", "article"])


class FiltersConfig(BaseModel):
    enabled: bool = True
    price_range: bool = True
    availability: bool = True
    product_type: bool = True
    vendor: bool = True
    variant_options: bool = True


class FeaturesConfig(BaseModel):
    """All toggleable features in the theme."""
    wishlist: bool = False
    recently_viewed: bool = True
    countdown_timer: bool = False
    image_hotspots: bool = False
    before_after_slider: bool = False
    testimonials: bool = True
    faq: bool = True
    logo_wall: bool = True
    lookbook: bool = False
    size_chart: bool = True
    breadcrumbs: bool = True
    tabs: bool = True
    accordion: bool = True


class PerformanceConfig(BaseModel):
    target_lighthouse_mobile: int = Field(default=85, ge=60, le=100)
    target_lighthouse_desktop: int = Field(default=95, ge=60, le=100)
    max_js_payload_kb: int = Field(default=80, ge=30, le=200)
    max_css_payload_kb: int = Field(default=35, ge=15, le=100)
    lazy_load_below_fold: bool = True
    preload_hero_image: bool = True
    image_format: str = Field(default="auto", pattern="^(auto|webp|avif)$")


class AccessibilityConfig(BaseModel):
    wcag_target: str = Field(default="AA", pattern="^(A|AA|AAA)$")
    reduced_motion: bool = True
    skip_link: bool = True
    focus_visible: bool = True
    keyboard_navigation: bool = True


class ThemeManifest(BaseModel):
    """The complete theme generation manifest."""
    name: str = Field(..., min_length=2, max_length=50)
    author: str = Field(default="PSI BOT")
    version: str = Field(default="1.0.0")
    vertical: str = Field(default="general", description="Business vertical")

    # Style
    presets: List[ThemePreset] = Field(min_length=1, max_length=6)
    default_preset: int = Field(default=0, ge=0)

    # Layout
    header: HeaderConfig = Field(default_factory=HeaderConfig)
    product: ProductConfig = Field(default_factory=ProductConfig)
    cart: CartConfig = Field(default_factory=CartConfig)
    nav: NavConfig = Field(default_factory=NavConfig)
    search: SearchConfig = Field(default_factory=SearchConfig)
    filters: FiltersConfig = Field(default_factory=FiltersConfig)

    # Features
    features: FeaturesConfig = Field(default_factory=FeaturesConfig)

    # Quality gates
    performance: PerformanceConfig = Field(default_factory=PerformanceConfig)
    accessibility: AccessibilityConfig = Field(default_factory=AccessibilityConfig)

    # Additional sections to include
    extra_sections: List[str] = Field(default_factory=list)

    # Per-template section configuration
    # Format: {"index": [{"type": "weareix-hero", "id": "hero", "settings": {...}}, ...]}
    sections: Optional[Dict[str, Any]] = None

    # Section group overrides
    header_section_type: str = "header"
    footer_section_type: str = "footer"
    header_group_sections: List[Dict[str, Any]] = Field(default_factory=list)
    footer_group_sections: List[Dict[str, Any]] = Field(default_factory=list)

    @field_validator("presets")
    @classmethod
    def presets_have_unique_names(cls, v: List[ThemePreset]) -> List[ThemePreset]:
        names = [p.name for p in v]
        if len(set(names)) != len(names):
            raise ValueError("Preset names must be unique")
        return v

    @classmethod
    def from_yaml(cls, path: str) -> "ThemeManifest":
        import yaml
        with open(path) as f:
            data = yaml.safe_load(f)
        return cls(**data)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ThemeManifest":
        return cls(**data)
