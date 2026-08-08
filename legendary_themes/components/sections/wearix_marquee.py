"""
Wearix Marquee Section — infinite scrolling text ticker.
Typically used between sections for brand slogans or promotional text.
"""
from __future__ import annotations

from ...core.section import Section, SectionPreset, SectionRegistry
from ...core.setting import (
    Text, Header, Checkbox, Range, Color,
)


class WearixMarqueeSection(Section):
    type = "wearix-marquee"
    name = "Wearix marquee"
    tag = "section"
    class_name = "wearix-marquee"

    settings = [
        Header("Content"),
        Text("text", label="Marquee text",
             default="NEW DROP  •  FREE SHIPPING OVER $100  •  PREMIUM QUALITY  •  "),
        Checkbox("repeat", label="Repeat text", default=True),
        Range("repeat_count", label="Repeat count", min=2, max=12, default=6, unit=""),
        Header("Appearance"),
        Checkbox("invert", label="Dark background", default=False),
        Range("speed", label="Speed", min=10, max=60, default=25, unit="s"),
    ]

    blocks = []

    presets = [
        SectionPreset(
            name="Wearix marquee",
            settings={
                "text": "NEW DROP  •  FREE SHIPPING OVER $100  •  PREMIUM QUALITY  •  ",
                "repeat": True,
                "repeat_count": 6,
                "invert": False,
                "speed": 25,
            },
            blocks=[],
        ),
        SectionPreset(
            name="Dark marquee",
            settings={
                "text": "WEARIX  •  PREMIUM WEAR  •  MODERN LIVING  •  ",
                "invert": True,
                "repeat": True,
                "repeat_count": 6,
                "speed": 30,
            },
            blocks=[],
        ),
    ]

    styles = """
.wearix-marquee {
    overflow: hidden;
    white-space: nowrap;
    padding: 20px 0;
    border-top: 1px solid #e5e5e5;
    border-bottom: 1px solid #e5e5e5;
    background: #fff;
}

.wearix-marquee--invert {
    background: #000;
    color: #fff;
    border-color: #000;
}

.wearix-marquee__track {
    display: inline-flex;
    align-items: center;
    animation: marquee-scroll 25s linear infinite;
    will-change: transform;
}

.wearix-marquee__item {
    display: inline-block;
    padding: 0 24px;
    font-size: clamp(1.25rem, 3vw, 2rem);
    font-weight: 500;
    letter-spacing: -0.01em;
    white-space: nowrap;
}

@keyframes marquee-scroll {
    from { transform: translateX(0); }
    to { transform: translateX(-50%); }
}

@media (prefers-reduced-motion: reduce) {
    .wearix-marquee__track {
        animation: none;
    }
}
"""

    def render(self, settings, blocks):
        invert = " wearix-marquee--invert" if settings.get("invert") else ""
        speed = settings.get("speed", 25)
        repeat = int(settings.get("repeat_count", 6))
        items = "".join(
            f'<span class="wearix-marquee__item">{{{{ section.settings.text | escape }}}}</span>'
            for _ in range(repeat)
        )
        return f'''
<div class="wearix-marquee{invert}">
  <div class="wearix-marquee__track" style="animation-duration: {speed}s">
    {items}
  </div>
</div>
'''


SectionRegistry.register(WearixMarqueeSection)
