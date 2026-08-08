"""
Header section — the most complex section in any theme.
Includes: logo, navigation, search, cart, account, mobile menu.
"""
from ...core.section import Section, SectionPreset, SectionRegistry
from ...core.setting import (
    Text, ImagePicker, Select, SelectOption, Checkbox, LinkList, Header, Color,
)
from ...core.block import Block


class HeaderSection(Section):
    type = "header"
    name = "Header"
    tag = "header"
    class_name = "header"
    limit = 1  # Only one header per page
    available_on = []  # Used in section group, not directly added to templates

    settings = [
        Header("Layout"),
        Select(
            "layout", label="Header layout",
            options=[
                SelectOption("minimal", "Minimal"),
                SelectOption("standard", "Standard"),
                SelectOption("centered", "Centered"),
                SelectOption("stacked", "Stacked"),
            ],
            default="standard",
        ),
        Checkbox("sticky", label="Enable sticky header", default=True),
        Checkbox("show_search", label="Show search icon", default=True),
        Checkbox("show_cart", label="Show cart icon", default=True),
        Checkbox("show_account", label="Show account icon", default=True),
        Header("Logo"),
        ImagePicker("logo", label="Logo image"),
        Text("logo_width", label="Logo width (px)", default="120"),
        Select("logo_position", label="Logo position",
               options=[
                   SelectOption("left", "Left"),
                   SelectOption("center", "Center"),
               ],
               default="left"),
        Header("Menu"),
        LinkList("menu", label="Main menu", default="main-menu"),
        Checkbox("show_mega_menu", label="Enable mega menu", default=True),
        Header("Cart"),
        Select("cart_style", label="Cart type",
               options=[
                   SelectOption("drawer", "Drawer"),
                   SelectOption("page", "Page"),
               ],
               default="drawer"),
    ]

    blocks = []  # Header doesn't use blocks by default (it's a section group child)

    presets = [
        SectionPreset(name="Header", settings={
            "layout": "standard",
            "sticky": True,
            "show_search": True,
            "show_cart": True,
            "show_account": True,
            "menu": "main-menu",
            "cart_style": "drawer",
        }),
    ]

    template = """
{%- comment -%} Header section {%- endcomment -%}
<header class="header header--{{ section.settings.layout }} {% if section.settings.sticky %}header--sticky{% endif %}" {{ section.shopify_attributes }}>
  <div class="header__inner">
    <div class="header__left">
      <button
        type="button"
        class="header__menu-toggle"
        aria-label="{{ 'sections.header.menu' | t }}"
        aria-controls="mobile-menu"
        aria-expanded="false"
        data-action="toggle-menu"
      >
        {%- render 'icon-menu' -%}
      </button>

      {%- if section.settings.show_search -%}
        <button
          type="button"
          class="header__icon header__search-btn"
          aria-label="{{ 'sections.header.search' | t }}"
          data-action="toggle-search"
        >
          {%- render 'icon-search' -%}
        </button>
      {%- endif -%}
    </div>

    <div class="header__center">
      <a href="{{ routes.root_url }}" class="header__logo" aria-label="{{ shop.name | escape }}">
        {%- if section.settings.logo -%}
          {{ section.settings.logo | image_url: width: 300 | image_tag:
            alt: shop.name | escape,
            width: section.settings.logo_width | default: 120,
            heights: 'auto'
          }}
        {%- else -%}
          <h1 class="header__logo-text">{{ shop.name }}</h1>
        {%- endif -%}
      </a>
    </div>

    <div class="header__right">
      {%- if section.settings.show_account -%}
        <a href="{{ routes.account_url }}" class="header__icon" aria-label="{{ 'sections.header.account' | t }}">
          {%- render 'icon-account' -%}
        </a>
      {%- endif -%}

      {%- if section.settings.show_cart -%}
        <a
          href="{% if section.settings.cart_style == 'drawer' %}#{% else %}{{ routes.cart_url }}{% endif %}"
          class="header__icon header__cart"
          aria-label="{{ 'sections.header.cart' | t }}"
          {% if section.settings.cart_style == 'drawer' %}data-action="toggle-cart" aria-controls="cart-drawer"{% endif %}
        >
          {%- render 'icon-cart' -%}
          <span class="header__cart-count" data-cart-count>{{ cart.item_count }}</span>
        </a>
      {%- endif -%}
    </div>
  </div>

  {%- if section.settings.layout != 'minimal' -%}
    <nav class="header__nav" aria-label="{{ 'sections.header.navigation' | t }}">
      {%- assign _menu = section.settings.menu -%}
      {%- if _menu -%}
        <ul class="header__nav-list">
          {%- for link in _menu.links -%}
            <li class="header__nav-item {% if link.links.size > 0 %}has-submenu{% endif %}">
              <a
                href="{{ link.url }}"
                class="header__nav-link"
                {% if link.links.size > 0 %}
                  aria-haspopup="true"
                  aria-expanded="false"
                {% endif %}
              >
                {{ link.title }}
                {%- if link.links.size > 0 -%}
                  {%- render 'icon-chevron-down' -%}
                {%- endif -%}
              </a>
              {%- if link.links.size > 0 -%}
                <div class="header__submenu" role="menu">
                  <ul>
                    {%- for sublink in link.links -%}
                      <li role="none">
                        <a href="{{ sublink.url }}" role="menuitem">{{ sublink.title }}</a>
                      </li>
                    {%- endfor -%}
                  </ul>
                </div>
              {%- endif -%}
            </li>
          {%- endfor -%}
        </ul>
      {%- endif -%}
    </nav>
  {%- endif -%}
</header>

{% comment %}Mobile menu drawer{% endcomment %}
<div
  id="mobile-menu"
  class="mobile-menu"
  hidden
  aria-hidden="true"
  role="dialog"
  aria-label="{{ 'sections.header.mobile_menu' | t }}"
>
  <div class="mobile-menu__header">
    <button
      type="button"
      class="mobile-menu__close"
      aria-label="{{ 'sections.header.close_menu' | t }}"
      data-action="close-menu"
    >
      {%- render 'icon-close' -%}
    </button>
  </div>
  <nav class="mobile-menu__nav" aria-label="{{ 'sections.header.mobile_navigation' | t }}">
    {%- if _menu -%}
      <ul class="mobile-menu__list">
        {%- for link in _menu.links -%}
          <li class="mobile-menu__item">
            <a href="{{ link.url }}" class="mobile-menu__link">{{ link.title }}</a>
          </li>
        {%- endfor -%}
      </ul>
    {%- endif -%}
  </nav>
</div>
    """

    styles = """
.header {
  position: relative;
  z-index: 100;
  background: var(--color-background, #fff);
  border-bottom: 1px solid var(--color-border, #eee);
}

.header--sticky {
  position: sticky;
  top: 0;
}

.header__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  max-width: var(--max-width, 1440px);
  margin: 0 auto;
  gap: 1rem;
}

.header__left,
.header__right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
}

.header__right {
  justify-content: flex-end;
}

.header__center {
  flex: 1;
  text-align: center;
}

.header--standard .header__center {
  flex: 0 0 auto;
  text-align: left;
}

.header__logo {
  display: inline-flex;
  align-items: center;
  text-decoration: none;
  color: inherit;
}

.header__logo img {
  max-width: 100%;
  height: auto;
}

.header__logo-text {
  font-family: var(--font-heading-family);
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
}

.header__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  color: var(--color-text);
  background: none;
  border: none;
  cursor: pointer;
  text-decoration: none;
  position: relative;
}

.header__menu-toggle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  background: none;
  border: none;
  cursor: pointer;
  color: var(--color-text);
}

.header__cart-count {
  position: absolute;
  top: 0.25rem;
  right: 0.25rem;
  min-width: 1.125rem;
  height: 1.125rem;
  padding: 0 0.25rem;
  background: var(--color-accent, #e53935);
  color: #fff;
  font-size: 0.625rem;
  font-weight: 600;
  border-radius: 999px;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

.header__nav {
  border-top: 1px solid var(--color-border, #eee);
  padding: 0 1.5rem;
  max-width: var(--max-width, 1440px);
  margin: 0 auto;
}

.header__nav-list {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2rem;
  list-style: none;
  margin: 0;
  padding: 0;
  flex-wrap: wrap;
}

.header__nav-link {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.875rem 0;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-text);
  text-decoration: none;
}

.header__nav-link:hover {
  color: var(--color-accent);
}

.header__submenu {
  position: absolute;
  top: 100%;
  left: 0;
  min-width: 200px;
  background: var(--color-background, #fff);
  border: 1px solid var(--color-border, #eee);
  padding: 0.5rem 0;
  opacity: 0;
  visibility: hidden;
  transition: all 0.2s ease;
  z-index: 10;
}

.header__nav-item:hover .header__submenu {
  opacity: 1;
  visibility: visible;
}

.header__submenu ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.header__submenu a {
  display: block;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  color: var(--color-text);
  text-decoration: none;
}

.header__submenu a:hover {
  background: var(--color-surface, #f5f5f5);
}

/* Mobile menu */
.mobile-menu {
  position: fixed;
  inset: 0;
  z-index: 200;
  background: var(--color-background, #fff);
  transform: translateX(-100%);
  transition: transform 0.3s ease;
  max-width: 320px;
  width: 85vw;
}

.mobile-menu[hidden] {
  display: block;
  visibility: hidden;
}

.mobile-menu:not([hidden]) {
  transform: translateX(0);
}

.mobile-menu__header {
  display: flex;
  justify-content: flex-end;
  padding: 1rem;
  border-bottom: 1px solid var(--color-border, #eee);
}

.mobile-menu__close {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  color: var(--color-text);
}

.mobile-menu__nav {
  padding: 1rem;
}

.mobile-menu__list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.mobile-menu__link {
  display: block;
  padding: 0.875rem 0;
  font-size: 1rem;
  color: var(--color-text);
  text-decoration: none;
  border-bottom: 1px solid var(--color-border, #eee);
}

@media (min-width: 1024px) {
  .header__menu-toggle {
    display: none;
  }
}

@media (max-width: 1023px) {
  .header__nav {
    display: none;
  }
  .header--standard .header__center {
    flex: 1;
    text-align: center;
  }
}

@media (prefers-reduced-motion: reduce) {
  .mobile-menu { transition: none; }
  .header__submenu { transition: none; }
}
    """

    scripts = """
// Header behavior: mobile menu toggle, search toggle, cart drawer
(function() {
  const header = document.getElementById('shopify-section-' + __section_id);
  if (!header) return;

  const menuToggle = header.querySelector('[data-action="toggle-menu"]');
  const closeMenu = header.querySelector('[data-action="close-menu"]');
  const mobileMenu = header.querySelector('.mobile-menu');
  const searchBtn = header.querySelector('[data-action="toggle-search"]');
  const cartBtn = header.querySelector('[data-action="toggle-cart"]');

  menuToggle?.addEventListener('click', () => {
    if (!mobileMenu) return;
    const isOpen = !mobileMenu.hasAttribute('hidden');
    if (isOpen) {
      mobileMenu.setAttribute('hidden', '');
      mobileMenu.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    } else {
      mobileMenu.removeAttribute('hidden');
      mobileMenu.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      const closeBtn = mobileMenu.querySelector('.mobile-menu__close');
      closeBtn?.focus();
    }
  });

  closeMenu?.addEventListener('click', () => {
    mobileMenu?.setAttribute('hidden', '');
    mobileMenu?.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    menuToggle?.focus();
  });

  // Close on escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !mobileMenu?.hasAttribute('hidden')) {
      mobileMenu.setAttribute('hidden', '');
      mobileMenu.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
      menuToggle?.focus();
    }
  });
})();
    """


SectionRegistry.register(HeaderSection)
