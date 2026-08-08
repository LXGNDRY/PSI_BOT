"""
Wearix Newsletter Section — black background, centered, inline input+button.

Wearix pattern:
- Full-width black section
- Centered heading + subheading
- Pill-shaped email input with submit button inside/next to it
- Minimal, high-contrast
"""
from __future__ import annotations

from ...core.section import Section, SectionPreset, SectionRegistry
from ...core.setting import (
    Text, Checkbox, Header,
)


class WearixNewsletterSection(Section):
    type = "wearix-newsletter"
    name = "Wearix newsletter"
    tag = "section"
    class_name = "wearix-newsletter"

    settings = [
        Header("Content"),
        Text("heading", label="Heading", default="Join the Wearix community"),
        Text("subheading", label="Subheading",
             default="Be the first to know about new drops, exclusive offers, and style guides."),
        Text("placeholder", label="Email placeholder", default="Enter your email"),
        Text("button_text", label="Button text", default="Subscribe"),
        Checkbox("success_message", label="Show success message", default=True),
    ]

    blocks = []

    presets = [
        SectionPreset(
            name="Newsletter",
            settings={
                "heading": "Join the Wearix community",
                "subheading": "Be the first to know about new drops, exclusive offers, and style guides.",
                "button_text": "Subscribe",
            },
            blocks=[],
        ),
    ]

    styles = """
.wearix-newsletter {
    padding: 100px 24px;
    background: #000;
    color: #fff;
    text-align: center;
}

.wearix-newsletter__inner {
    max-width: 600px;
    margin: 0 auto;
}

.wearix-newsletter__heading {
    font-size: clamp(1.75rem, 4vw, 2.5rem);
    font-weight: 500;
    letter-spacing: -0.02em;
    margin: 0 0 16px 0;
    color: #fff;
}

.wearix-newsletter__subheading {
    font-size: 16px;
    line-height: 1.6;
    color: rgba(255, 255, 255, 0.7);
    margin: 0 0 40px 0;
}

.wearix-newsletter__form {
    display: flex;
    gap: 8px;
    max-width: 480px;
    margin: 0 auto;
}

.wearix-newsletter__input {
    flex: 1;
    min-width: 0;
    padding: 14px 20px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 50px;
    background: rgba(255, 255, 255, 0.05);
    color: #fff;
    font-size: 14px;
    font-family: inherit;
    outline: none;
    transition: border-color 0.2s ease;
}

.wearix-newsletter__input::placeholder {
    color: rgba(255, 255, 255, 0.4);
}

.wearix-newsletter__input:focus {
    border-color: rgba(255, 255, 255, 0.6);
}

.wearix-newsletter__submit {
    padding: 14px 28px;
    background: #fff;
    color: #000;
    border: none;
    border-radius: 50px;
    font-size: 14px;
    font-weight: 500;
    font-family: inherit;
    cursor: pointer;
    transition: all 0.2s ease;
    white-space: nowrap;
}

.wearix-newsletter__submit:hover {
    background: #e5e5e5;
}

.wearix-newsletter__submit:focus-visible {
    outline: 2px solid #fff;
    outline-offset: 2px;
}

@media (max-width: 480px) {
    .wearix-newsletter {
        padding: 60px 24px;
    }
    .wearix-newsletter__form {
        flex-direction: column;
    }
    .wearix-newsletter__submit {
        width: 100%;
    }
}
"""

    def render(self, settings, blocks):
        return f'''
<section class="wearix-newsletter">
  <div class="wearix-newsletter__inner container">
    {{% if section.settings.heading != blank %}}
      <h2 class="wearix-newsletter__heading">{{{{ section.settings.heading | escape }}}}</h2>
    {{% endif %}}
    {{% if section.settings.subheading != blank %}}
      <p class="wearix-newsletter__subheading">{{{{ section.settings.subheading | escape }}}}</p>
    {{% endif %}}

    <form class="wearix-newsletter__form" action="{{{{ routes.newsletter_url }}}}" method="post" accept-charset="UTF-8">
      <input type="hidden" name="form_type" value="customer">
      <input type="hidden" name="utf8" value="✓">
      <input type="hidden" name="contact[tags]" value="newsletter">
      <label for="newsletter-email" class="visually-hidden">{{{{ "Email address" | t }}}}</label>
      <input
        type="email"
        id="newsletter-email"
        class="wearix-newsletter__input"
        name="contact[email]"
        placeholder="{{{{ section.settings.placeholder | escape }}}}"
        autocorrect="off"
        autocapitalize="off"
        required>
      <button type="submit" class="wearix-newsletter__submit">
        {{{{ section.settings.button_text | escape }}}}
      </button>
    </form>
  </div>
</section>
'''


SectionRegistry.register(WearixNewsletterSection)
