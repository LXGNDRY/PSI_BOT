"""Announcement bar section — rotating message bar at top of page."""
from ...core.section import Section, SectionPreset, SectionRegistry
from ...core.setting import (
    Text, Select, SelectOption, Checkbox, Color, Url, Header,
)


class AnnouncementBarSection(Section):
    type = "announcement-bar"
    name = "Announcement bar"
    tag = "section"
    class_name = "announcement-bar"
    limit = 1
    available_on = []  # Section group only

    settings = [
        Header("Content"),
        Text("message", label="Message", default="Free shipping on orders over $100"),
        Checkbox("enable_link", label="Enable link", default=False),
        Url("link_url", label="Link URL"),
        Text("link_text", label="Link text", default="Learn more"),
        Header("Style"),
        Select("text_alignment", label="Text alignment",
               options=[
                   SelectOption("left", "Left"),
                   SelectOption("center", "Center"),
                   SelectOption("right", "Right"),
               ],
               default="center"),
        Color("background_color", label="Background color", default="#111111"),
        Color("text_color", label="Text color", default="#ffffff"),
        Header("Settings"),
        Checkbox("enable_close", label="Allow customers to close", default=True),
        Checkbox("auto_rotate", label="Auto-rotate messages", default=False),
    ]

    presets = [
        SectionPreset(name="Announcement bar", settings={
            "message": "Free shipping on orders over $100",
            "text_alignment": "center",
            "background_color": "#111111",
            "text_color": "#ffffff",
            "enable_close": True,
        }),
    ]

    template = """
{%- comment -%} Announcement bar section {%- endcomment -%}
{%- if section.settings.message != '' -%}
  <div
    class="announcement-bar"
    {{ section.shopify_attributes }}
    style="background: {{ section.settings.background_color }}; color: {{ section.settings.text_color }}; text-align: {{ section.settings.text_alignment }};"
    data-announcement-bar
  >
    <div class="announcement-bar__inner">
      <p class="announcement-bar__message">
        {{ section.settings.message }}
        {%- if section.settings.enable_link and section.settings.link_url -%}
          <a href="{{ section.settings.link_url }}" class="announcement-bar__link" style="color: inherit;">
            {{ section.settings.link_text }}
          </a>
        {%- endif -%}
      </p>
      {%- if section.settings.enable_close -%}
        <button
          type="button"
          class="announcement-bar__close"
          aria-label="{{ 'general.close' | t }}"
          data-action="close"
          style="color: inherit;"
        >
          {%- render 'icon-close' -%}
        </button>
      {%- endif -%}
    </div>
  </div>
{%- endif -%}
    """

    styles = """
.announcement-bar {
  font-size: 0.8125rem;
  padding: 0.5rem 1.5rem;
  position: relative;
}

.announcement-bar[hidden] {
  display: none;
}

.announcement-bar__inner {
  max-width: var(--max-width, 1440px);
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  position: relative;
}

.announcement-bar__message {
  margin: 0;
}

.announcement-bar__link {
  text-decoration: underline;
  margin-left: 0.5rem;
  font-weight: 500;
}

.announcement-bar__close {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  display: inline-flex;
  align-items: center;
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
}

.announcement-bar__close:focus-visible {
  outline: 2px solid currentColor;
  outline-offset: 2px;
  border-radius: 2px;
}
    """

    scripts = """
// Announcement bar close behavior
(function() {
  const bar = document.querySelector('[data-announcement-bar]');
  if (!bar) return;

  const closeBtn = bar.querySelector('[data-action="close"]');
  if (!closeBtn) return;

  const storageKey = 'announcement_bar_closed_' + {{ section.id | json }};

  if (localStorage.getItem(storageKey) === 'true') {
    bar.setAttribute('hidden', '');
    return;
  }

  closeBtn.addEventListener('click', () => {
    bar.setAttribute('hidden', '');
    localStorage.setItem(storageKey, 'true');
  });
})();
    """


SectionRegistry.register(AnnouncementBarSection)
