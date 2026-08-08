"""
Theme Check runner — shells out to Shopify CLI theme check if available.
Falls back gracefully if CLI is not installed.
"""
from __future__ import annotations

import subprocess
import json
import os
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ThemeCheckResult:
    available: bool
    errors: List[dict]
    warnings: List[dict]
    suggestions: List[dict]
    raw_output: str = ""

    @property
    def passed(self) -> bool:
        return self.available and len(self.errors) == 0


def run_theme_check(theme_dir: str) -> ThemeCheckResult:
    """
    Run Shopify theme check on the generated theme.
    Returns a result with errors/warnings.
    If theme-check CLI is not available, returns available=False.
    """
    # Check if shopify CLI is available
    try:
        result = subprocess.run(
            ["shopify", "theme", "check", "--format", "json", theme_dir],
            capture_output=True,
            text=True,
            timeout=120,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return ThemeCheckResult(
            available=False,
            errors=[],
            warnings=[],
            suggestions=[],
        )

    try:
        data = json.loads(result.stdout) if result.stdout.strip() else {}
    except json.JSONDecodeError:
        return ThemeCheckResult(
            available=True,
            errors=[{"message": "Failed to parse theme check output", "raw": result.stdout}],
            warnings=[],
            suggestions=[],
            raw_output=result.stdout,
        )

    errors = data.get("errors", []) if isinstance(data, dict) else []
    warnings = data.get("warnings", []) if isinstance(data, dict) else []
    suggestions = data.get("suggestions", []) if isinstance(data, dict) else []

    return ThemeCheckResult(
        available=True,
        errors=errors,
        warnings=warnings,
        suggestions=suggestions,
        raw_output=result.stdout + result.stderr,
    )
