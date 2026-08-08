"""
Static audit — validates generated theme files without running Shopify CLI.
Checks: JSON validity, bundle size, file structure, Liquid patterns, accessibility basics.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class AuditFinding:
    severity: str  # "error" | "warning" | "info"
    rule_id: str
    message: str
    file: str = ""


@dataclass
class StaticAuditResult:
    findings: List[AuditFinding] = field(default_factory=list)
    file_count: int = 0
    total_css_bytes: int = 0
    total_js_bytes: int = 0
    total_liquid_bytes: int = 0

    @property
    def errors(self) -> List[AuditFinding]:
        return [f for f in self.findings if f.severity == "error"]

    @property
    def warnings(self) -> List[AuditFinding]:
        return [f for f in self.findings if f.severity == "warning"]

    @property
    def passed(self) -> bool:
        return len(self.errors) == 0


def audit_theme(output_dir: str, max_js_kb: int = 150, max_css_kb: int = 60) -> StaticAuditResult:
    """Run static audits on a generated theme directory."""
    result = StaticAuditResult()
    files = _list_files(output_dir)
    result.file_count = len(files)

    # 1. Required directories
    _check_required_dirs(output_dir, result)

    # 2. Required files
    _check_required_files(files, result)

    # 3. JSON validity
    _check_json_validity(output_dir, files, result)

    # 4. Bundle size
    _check_bundle_sizes(output_dir, files, result, max_js_kb, max_css_kb)

    # 5. Liquid checks
    _check_liquid_patterns(output_dir, files, result)

    # 6. Accessibility basics
    _check_accessibility_basics(output_dir, files, result)

    # 7. Performance basics
    _check_performance_basics(output_dir, files, result)

    # 8. Hardcoded strings check
    _check_hardcoded_strings(output_dir, files, result)

    return result


def _list_files(output_dir: str) -> List[str]:
    result = []
    for root, _, filenames in os.walk(output_dir):
        for f in filenames:
            rel = os.path.relpath(os.path.join(root, f), output_dir)
            result.append(rel)
    return result


def _check_required_dirs(output_dir: str, result: StaticAuditResult):
    required = ["assets", "config", "layout", "locales", "sections", "snippets", "templates"]
    for d in required:
        if not os.path.isdir(os.path.join(output_dir, d)):
            result.findings.append(AuditFinding(
                "error", "SA001", f"Missing required directory: {d}", d
            ))


def _check_required_files(files: List[str], result: StaticAuditResult):
    required = [
        "layout/theme.liquid",
        "config/settings_schema.json",
        "config/settings_data.json",
        "locales/en.default.json",
        "templates/index.json",
        "templates/product.json",
        "templates/collection.json",
        "templates/cart.json",
        "templates/page.json",
        "templates/search.json",
        "templates/404.json",
        "templates/blog.json",
        "templates/article.json",
        "templates/list-collections.json",
        "templates/password.json",
        "templates/gift_card.liquid",
    ]
    for f in required:
        if f not in files:
            result.findings.append(AuditFinding(
                "error", "SA002", f"Missing required file: {f}", f
            ))


def _check_json_validity(output_dir: str, files: List[str], result: StaticAuditResult):
    json_files = [f for f in files if f.endswith('.json') and f.startswith(('config/', 'templates/', 'sections/'))]
    for f in json_files:
        path = os.path.join(output_dir, f)
        try:
            with open(path) as fh:
                json.load(fh)
        except json.JSONDecodeError as e:
            result.findings.append(AuditFinding(
                "error", "SA003", f"Invalid JSON: {e}", f
            ))


def _check_bundle_sizes(output_dir: str, files: List[str],
                       result: StaticAuditResult, max_js_kb: int, max_css_kb: int):
    js_files = [f for f in files if f.endswith('.js') and f.startswith('assets/')]
    css_files = [f for f in files if f.endswith('.css') and f.startswith('assets/')]

    for f in js_files:
        size = os.path.getsize(os.path.join(output_dir, f))
        result.total_js_bytes += size

    for f in css_files:
        size = os.path.getsize(os.path.join(output_dir, f))
        result.total_css_bytes += size

    js_kb = result.total_js_bytes / 1024
    css_kb = result.total_css_bytes / 1024

    if js_kb > max_js_kb:
        result.findings.append(AuditFinding(
            "warning", "SA101",
            f"Total JS ({js_kb:.1f} KB) exceeds budget ({max_js_kb} KB)"
        ))

    if css_kb > max_css_kb:
        result.findings.append(AuditFinding(
            "warning", "SA102",
            f"Total CSS ({css_kb:.1f} KB) exceeds budget ({max_css_kb} KB)"
        ))


def _check_liquid_patterns(output_dir: str, files: List[str], result: StaticAuditResult):
    liquid_files = [f for f in files if f.endswith('.liquid')]

    # Check theme.liquid has required objects
    theme_liquid = os.path.join(output_dir, "layout/theme.liquid")
    if os.path.exists(theme_liquid):
        with open(theme_liquid) as f:
            content = f.read()
        if "content_for_header" not in content:
            result.findings.append(AuditFinding(
                "error", "SA201",
                "layout/theme.liquid missing {{ content_for_header }}",
                "layout/theme.liquid"
            ))
        if "content_for_layout" not in content:
            result.findings.append(AuditFinding(
                "error", "SA202",
                "layout/theme.liquid missing {{ content_for_layout }}",
                "layout/theme.liquid"
            ))
        if "<html" not in content.lower() or "lang=" not in content.lower():
            result.findings.append(AuditFinding(
                "warning", "SA203",
                "<html> tag missing lang attribute",
                "layout/theme.liquid"
            ))

    # Check for deprecated include tags
    for f in liquid_files:
        path = os.path.join(output_dir, f)
        with open(path) as fh:
            content = fh.read()
        if re.search(r'{%\s*include\s+', content):
            result.findings.append(AuditFinding(
                "warning", "SA204",
                "Uses deprecated {% include %} (use {% render %} instead)",
                f
            ))
        if "jQuery" in content or "$(" in content:
            result.findings.append(AuditFinding(
                "warning", "SA205",
                f"Potential jQuery dependency detected",
                f
            ))


def _check_accessibility_basics(output_dir: str, files: List[str], result: StaticAuditResult):
    theme_liquid = os.path.join(output_dir, "layout/theme.liquid")
    if os.path.exists(theme_liquid):
        with open(theme_liquid) as f:
            content = f.read()
        if "skip-link" not in content and "skip_link" not in content and "skip to content" not in content.lower():
            result.findings.append(AuditFinding(
                "warning", "SA301",
                "Skip-to-content link not found in layout",
                "layout/theme.liquid"
            ))

    # Check that all image_picker sections have alt text support (image_tag auto-includes it)
    section_files = [f for f in files if f.startswith('sections/') and f.endswith('.liquid')]
    for f in section_files:
        path = os.path.join(output_dir, f)
        with open(path) as fh:
            content = fh.read()
        # Check for aria labels on buttons without visible text
        buttons_no_text = re.findall(r'<button[^>]*>\s*{%-?\s*render\s+\'icon', content)
        if buttons_no_text and 'aria-label' not in content:
            result.findings.append(AuditFinding(
                "warning", "SA302",
                f"Icon buttons may lack aria-label",
                f
            ))


def _check_performance_basics(output_dir: str, files: List[str], result: StaticAuditResult):
    theme_liquid = os.path.join(output_dir, "layout/theme.liquid")
    if os.path.exists(theme_liquid):
        with open(theme_liquid) as f:
            content = f.read()
        # Check for render-blocking JS
        scripts = re.findall(r'<script[^>]*>', content)
        for script in scripts:
            if 'src=' in script and 'defer' not in script and 'async' not in script:
                result.findings.append(AuditFinding(
                    "warning", "SA401",
                    f"Render-blocking script without defer/async",
                    "layout/theme.liquid"
                ))


def _check_hardcoded_strings(output_dir: str, files: List[str], result: StaticAuditResult):
    """Check for visible text that isn't using translation filter."""
    # Simplified check: look for patterns of hardcoded user-visible text
    # This is a heuristic, not a precise check
    section_files = [f for f in files if f.startswith('sections/') and f.endswith('.liquid')]
    snippet_files = [f for f in files if f.startswith('snippets/') and f.endswith('.liquid')]
    liquid_files = section_files + snippet_files

    for f in liquid_files:
        path = os.path.join(output_dir, f)
        with open(path) as fh:
            content = fh.read()
        # Look for plain text inside HTML elements that isn't using | t
        # This is intentionally lenient to avoid false positives
        matches = re.findall(r'>([A-Z][a-zA-Z\s]{5,})<', content)
        hardcoded = [m.strip() for m in matches if '| t' not in content[max(0, content.find(m)-50):content.find(m)+50]]
        if len(hardcoded) > 3:
            result.findings.append(AuditFinding(
                "info", "SA501",
                f"Potential hardcoded strings: {', '.join(hardcoded[:3])}",
                f
            ))
