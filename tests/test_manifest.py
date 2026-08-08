"""Tests for manifest validation."""
import pytest
from legendary_themes.core.manifest import ThemeManifest, ThemePalette, ThemeTypography, ThemePreset


def test_minimal_valid_manifest():
    m = ThemeManifest(
        name="Test Theme",
        presets=[
            ThemePreset(
                name="Default",
                palette=ThemePalette(
                    primary="#000000", secondary="#ffffff", accent="#ff0000",
                    background="#ffffff", surface="#f5f5f5",
                    text="#000000", text_muted="#666666", border="#ddd"
                ),
                typography=ThemeTypography(),
            )
        ],
    )
    assert m.name == "Test Theme"
    assert len(m.presets) == 1


def test_manifest_requires_presets():
    with pytest.raises(Exception):
        ThemeManifest(name="Test", presets=[])


def test_preset_names_must_be_unique():
    with pytest.raises(Exception):
        ThemeManifest(
            name="Test",
            presets=[
                ThemePreset(name="Same", palette=ThemePalette(
                    primary="#000", secondary="#fff", accent="#f00",
                    background="#fff", surface="#f5f5f5",
                    text="#000", text_muted="#666", border="#ddd"
                ), typography=ThemeTypography()),
                ThemePreset(name="Same", palette=ThemePalette(
                    primary="#000", secondary="#fff", accent="#f00",
                    background="#fff", surface="#f5f5f5",
                    text="#000", text_muted="#666", border="#ddd"
                ), typography=ThemeTypography()),
            ],
        )
