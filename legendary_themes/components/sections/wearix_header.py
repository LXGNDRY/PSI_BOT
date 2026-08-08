"""
Wearix Header Section — minimalist transparent header that becomes solid on scroll.

Wearix pattern:
- Logo left (WEARIX, bold uppercase)
- Nav links center (Home, About, Shop, Blog, Contact)
- Right: search icon + "Shop all items" pill button
- Transparent on hero (white text), becomes white solid (black text) on scroll
- Sticky positioning
- Mobile menu drawer
"""
from __future__ import annotations

from ...core.section import Section, SectionPreset, SectionRegistry
from ...core.setting import (
    Text, ImagePicker, Select, SelectOption, Checkbox, LinkList, Header, Color,
)


class WearixHeaderSection(Section):
    type = "wearix-header"
    name = "Wearix header"
    tag = "header"
    class_name = "wearix-header"
    limit = 1
    available_on = []  # Section group only

    settings = [
        Header("Logo"),
        ImagePicker("logo", label="Logo image"),
        Text("logo_text", label="Logo text (if no image)", default="WEARIX"),
        Text("logo_width", label="Logo width (px)", default="120"),

        Header("Navigation"),
        LinkList("main_menu", label="Main menu", default="main-menu"),
        Select("layout", label="Layout style",
               options=[
                   SelectOption("standard", "Standard (logo left, nav center, actions right)"),
                   SelectOption("centered", "Centered (logo above nav)"),
               ], default="standard"),
        Checkbox("transparent_on_hero", label="Transparent on hero", default=True),
        Checkbox("sticky", label="Sticky on scroll", default=True),

        Header("Icons / Actions"),
        Checkbox("show_search", label="Show search icon", default=True),
        Checkbox("show_cart", label="Show cart icon", default=True),
        Checkbox("show_account", label="Show account icon", default=True),
        Checkbox("show_cta", label="Show CTA button", default=True),
        Text("cta_text", label="CTA button text", default="Shop all items"),
        Text("cta_link", label="CTA button link", default="/collections/all"),

        Header("Mobile"),
        Checkbox("mobile_menu", label="Mobile menu drawer", default=True),
    ]

    blocks = []

    presets = [
        SectionPreset(
            name="Wearix header",
            settings={
                "logo_text": "WEARIX",
                "layout": "standard",
                "transparent_on_hero": True,
                "sticky": True,
                "show_search": True,
                "show_cart": True,
                "show_account": True,
                "show_cta": True,
                "cta_text": "Shop all items",
            },
            blocks=[],
        ),
    ]

    styles = """
.wearix-header {
    position: sticky;
    top: 0;
    z-index: 100;
    background: #fff;
    border-bottom: 1px solid #e5e5e5;
    transition: background 0.3s ease, border-color 0.3s ease;
}

.wearix-header--transparent {
    background: transparent;
    border-bottom: 1px solid rgba(255, 255, 255, 0.15);
    color: #fff;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
}

.wearix-header--transparent .wearix-header__logo,
.wearix-header--transparent .wearix-header__nav a,
.wearix-header--transparent .wearix-header__icon {
    color: #fff;
}

.wearix-header--transparent .wearix-header__cta {
    background: #fff;
    color: #000;
}

.wearix-header--scrolled {
    background: #fff !important;
    border-bottom-color: #e5e5e5 !important;
    color: #000 !important;
}

.wearix-header--scrolled .wearix-header__logo,
.wearix-header--scrolled .wearix-header__nav a,
.wearix-header--scrolled .wearix-header__icon {
    color: #000 !important;
}

.wearix-header__inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 72px;
    padding: 0 24px;
    max-width: 1440px;
    margin: 0 auto;
}

.wearix-header__logo {
    font-size: 20px;
    font-weight: 700;
    letter-spacing: -0.02em;
    text-decoration: none;
    color: #000;
}

.wearix-header__logo img {
    height: 32px;
    width: auto;
}

.wearix-header__nav {
    display: flex;
    gap: 32px;
    align-items: center;
    list-style: none;
    padding: 0;
    margin: 0;
}

.wearix-header__nav a {
    font-size: 14px;
    font-weight: 500;
    color: #000;
    text-decoration: none;
    transition: opacity 0.2s ease;
    position: relative;
}

.wearix-header__nav a:hover {
    opacity: 0.6;
}

.wearix-header__actions {
    display: flex;
    align-items: center;
    gap: 20px;
}

.wearix-header__icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    color: #000;
    text-decoration: none;
    position: relative;
    background: none;
    border: none;
    padding: 0;
    cursor: pointer;
}

.wearix-header__icon svg {
    width: 20px;
    height: 20px;
}

.wearix-header__cart-count {
    position: absolute;
    top: -4px;
    right: -8px;
    background: #000;
    color: #fff;
    font-size: 10px;
    font-weight: 600;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.wearix-header--transparent .wearix-header__cart-count {
    background: #fff;
    color: #000;
}

.wearix-header__cta {
    display: inline-block;
    padding: 10px 20px;
    background: #000;
    color: #fff;
    font-size: 13px;
    font-weight: 500;
    text-decoration: none;
    border-radius: 50px;
    transition: all 0.2s ease;
    white-space: nowrap;
}

.wearix-header__cta:hover {
    opacity: 0.9;
}

.wearix-header__mobile-toggle {
    display: none;
    background: none;
    border: none;
    cursor: pointer;
    padding: 4px;
    color: #000;
}

.wearix-header__mobile-toggle svg {
    width: 24px;
    height: 24px;
}

@media (max-width: 900px) {
    .wearix-header__nav,
    .wearix-header__cta {
        display: none;
    }
    .wearix-header__mobile-toggle {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .wearix-header__inner {
        height: 60px;
        padding: 0 16px;
    }
}
"""

    scripts = """
document.addEventListener('DOMContentLoaded', () => {
  const header = document.querySelector('.wearix-header');
  if (!header) return;

  // Sticky / scroll behavior
  if (header.classList.contains('wearix-header--transparent')) {
    const onScroll = () => {
      if (window.scrollY > 50) {
        header.classList.add('wearix-header--scrolled');
      } else {
        header.classList.remove('wearix-header--scrolled');
      }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }
});
"""

    def render(self, settings, blocks):
        transparent = " wearix-header--transparent" if settings.get("transparent_on_hero") else ""
        sticky = " wearix-header--sticky" if settings.get("sticky") else ""
        return f'''
<header class="wearix-header{transparent}{sticky}" role="banner">
  <div class="wearix-header__inner">
    <a href="{{{{ routes.root_url }}}}" class="wearix-header__logo">
      {{% if section.settings.logo != blank %}}
        <img src="{{{{ section.settings.logo | img_url: '300x' }}}}"
             alt="{{{{ section.settings.logo_text | escape }}}}"
             width="{{{{ section.settings.logo_width }}}}" height="32" style="height: 32px; width: auto;">
      {{% else %}}
        {{{{ section.settings.logo_text | escape }}}}
      {{% endif %}}
    </a>

    <nav class="wearix-header__nav" role="navigation" aria-label="Main navigation">
      {{% for link in section.settings.main_menu.links %}}
        <a href="{{{{ link.url }}}}">{{{{ link.title | escape }}}}</a>
      {{% endfor %}}
    </nav>

    <div class="wearix-header__actions">
      {{% if section.settings.show_search %}}
        <button type="button" class="wearix-header__icon" aria-label="Search">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <circle cx="11" cy="11" r="8"/>
            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
        </button>
      {{% endif %}}
      {{% if section.settings.show_account %}}
        <a href="{{{{ routes.account_url }}}}" class="wearix-header__icon" aria-label="Account">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
            <circle cx="12" cy="7" r="4"/>
          </svg>
        </a>
      {{% endif %}}
      {{% if section.settings.show_cart %}}
        <a href="{{{{ routes.cart_url }}}}" class="wearix-header__icon" aria-label="Cart">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="9" cy="21" r="1"/>
            <circle cx="20" cy="21" r="1"/>
            <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>
          </svg>
          {{% if cart.item_count > 0 %}}
            <span class="wearix-header__cart-count">{{{{ cart.item_count }}}}</span>
          {{% endif %}}
        </a>
      {{% endif %}}
      {{% if section.settings.show_cta %}}
        <a href="{{{{ section.settings.cta_link }}}}" class="wearix-header__cta">
          {{{{ section.settings.cta_text | escape }}}}
        </a>
      {{% endif %}}
      {{% if section.settings.mobile_menu %}}
        <button type="button" class="wearix-header__mobile-toggle" aria-label="Open menu" aria-expanded="false">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <line x1="3" y1="12" x2="21" y2="12"/>
            <line x1="3" y1="6" x2="21" y2="6"/>
            <line x1="3" y1="18" x2="21" y2="18"/>
          </svg>
        </button>
      {{% endif %}}
    </div>
  </div>
</header>
'''


SectionRegistry.register(WearixHeaderSection)
