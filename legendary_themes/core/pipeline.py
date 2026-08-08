"""
Main generation pipeline — the public entry point.
"""
from __future__ import annotations

import os
import json
import zipfile
from pathlib import Path
from typing import Optional, Dict

from .manifest import ThemeManifest
from .composer import ThemeComposer


def generate_theme(
    manifest: ThemeManifest,
    output_dir: str,
    zip_output: bool = False,
    run_audit: bool = True,
) -> Dict[str, str]:
    """
    Generate a complete Shopify theme from a manifest.

    Args:
        manifest: Validated ThemeManifest instance
        output_dir: Directory to write theme files into
        zip_output: Whether to also create a .zip package
        run_audit: Whether to generate an audit report

    Returns:
        Dict of file_path -> content for all generated files
    """
    composer = ThemeComposer(manifest)
    files = composer.compose()

    # Write files
    output_path = Path(output_dir)
    for rel_path, content in files.items():
        full_path = output_path / rel_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding="utf-8")

    # Generate audit report
    if run_audit:
        report = composer.audit_report()
        report_path = output_path / "AUDIT_REPORT.md"
        report_path.write_text(report, encoding="utf-8")

    # Create zip
    if zip_output:
        zip_path = output_path.parent / f"{manifest.name.lower().replace(' ', '-')}.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for rel_path, content in files.items():
                zf.writestr(rel_path, content)

    return files


def generate_from_yaml(
    manifest_path: str,
    output_dir: str,
    **kwargs,
) -> Dict[str, str]:
    """Generate theme from a YAML manifest file."""
    manifest = ThemeManifest.from_yaml(manifest_path)
    return generate_theme(manifest, output_dir, **kwargs)
