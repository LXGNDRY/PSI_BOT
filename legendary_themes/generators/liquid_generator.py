"""
Layout generator — produces theme.liquid, the master layout file.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.manifest import ThemeManifest


class LayoutGenerator:
    """Generates layout/theme.liquid."""

    def __init__(self, manifest: "ThemeManifest"):
        self.manifest = manifest

    def generate(self) -> str:
        m = self.manifest
        preset = m.presets[m.default_preset]

        return f"""<!doctype html>
<html class="no-js" lang="{{{{ request.locale.iso_code }}}}" dir="{{{{ request.locale.is_rtl | default: false | replace: 'true', 'rtl' | replace: 'false', 'ltr' }}}}">
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="{preset.palette.primary}">

  <title>{{{{ page_title }}}}</title>
  <meta name="description" content="{{{{ page_description | truncate: 160 }}}}">
  <link rel="canonical" href="{{{{ canonical_url }}}}">

  {{{{ content_for_header }}}}

  <meta property="og:title" content="{{{{ page_title }}}}">
  <meta property="og:description" content="{{{{ page_description | truncate: 160 }}}}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{{{{ canonical_url }}}}">
  <meta property="og:image" content="{{{{ page_image | image_url: width: 1200 }}}}">
  <meta property="og:site_name" content="{{{{ shop.name }}}}">
  <meta name="twitter:card" content="summary_large_image">

  <link rel="preconnect" href="https://cdn.shopify.com" crossorigin>
  <link rel="preconnect" href="https://shopify.dev" crossorigin>

  {{{{ settings.heading_font | font_face: font_display: 'swap' }}}}
  {{{{ settings.body_font | font_face: font_display: 'swap' }}}}

  <link rel="stylesheet" href="{{{{ 'base.css' | asset_url }}}}">
  <link rel="stylesheet" href="{{{{ 'component-card.css' | asset_url }}}}">
  <link rel="stylesheet" href="{{{{ 'component-button.css' | asset_url }}}}">

  <script>
    document.documentElement.className = document.documentElement.className.replace('no-js', 'js');
  </script>
</head>
<body class="template--{{{{ template.name }}}} template--{{{{ template.suffix | default: 'default' }}}}">
  <a class="skip-link visually-hidden" href="#MainContent">
    {{{{ 'general.accessibility.skip_to_content' | t }}}}
  </a>

  {{{{ content_for_layout }}}}

  <script src="{{{{ 'global.js' | asset_url }}}}" defer></script>
</body>
</html>
"""
