"""
Legendary Theme Generator CLI — command-line interface for the Shopify theme engine.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from ..core.manifest import ThemeManifest
from ..core.pipeline import generate_theme
from ..audit.static_audit import audit_theme
from ..audit.theme_check import run_theme_check

console = Console()


@click.group()
@click.version_option(version="1.0.0", prog_name="legendary")
def cli():
    """Legendary Theme Generator — Premium Shopify OS 2.0 Theme Engine."""
    pass


@cli.command()
@click.argument('manifest', type=click.Path(exists=True, dir_okay=False))
@click.option('-o', '--output', 'output_dir', default='./theme-output',
              type=click.Path(), help='Output directory for generated theme')
@click.option('--zip/--no-zip', default=False, help='Also create a zip package')
@click.option('--skip-audit', is_flag=True, help='Skip static audit')
@click.option('--theme-check', is_flag=True, help='Run Shopify theme check')
def generate(manifest, output_dir, zip, skip_audit, theme_check):
    """Generate a Shopify theme from a manifest file."""
    console.print(Panel.fit(
        "[bold cyan]Legendary[/bold cyan] — Premium Shopify OS 2.0 Theme Generator",
        box=box.ROUNDED
    ))

    # Load manifest
    console.print(f"\n[dim]Loading manifest:[/dim] {manifest}")
    try:
        m = ThemeManifest.from_yaml(manifest)
    except Exception as e:
        console.print(f"[red]✗ Failed to parse manifest:[/red] {e}")
        sys.exit(1)

    console.print(f"  Theme: [bold]{m.name}[/bold] v{m.version}")
    console.print(f"  Presets: {len(m.presets)} ({', '.join(p.name for p in m.presets)})")
    console.print(f"  Vertical: {m.vertical}")

    # Generate
    console.print(f"\n[dim]Generating theme...[/dim]")
    try:
        files = generate_theme(m, output_dir, zip_output=zip, run_audit=not skip_audit)
    except ValueError as e:
        console.print(f"[red]✗ Validation failed:[/red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]✗ Generation failed:[/red] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    console.print(f"[green]✓ Generated {len(files)} files[/green] → {output_dir}/")

    # Static audit
    if not skip_audit:
        console.print(f"\n[dim]Running static audit...[/dim]")
        audit_result = audit_theme(
            output_dir,
            max_js_kb=m.performance.max_js_payload_kb,
            max_css_kb=m.performance.max_css_payload_kb,
        )

        # Summary table
        table = Table(title="Audit Summary", box=box.ROUNDED)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", justify="right")
        table.add_row("Files generated", str(audit_result.file_count))
        table.add_row("Total CSS", f"{audit_result.total_css_bytes / 1024:.1f} KB")
        table.add_row("Total JS", f"{audit_result.total_js_bytes / 1024:.1f} KB")
        table.add_row("Errors", f"[red]{len(audit_result.errors)}[/red]" if audit_result.errors else f"[green]{len(audit_result.errors)}[/green]")
        table.add_row("Warnings", f"[yellow]{len(audit_result.warnings)}[/yellow]")
        console.print(table)

        if audit_result.errors:
            console.print("\n[red]Errors:[/red]")
            for e in audit_result.errors[:10]:
                console.print(f"  [{e.rule_id}] {e.message} [dim]({e.file})[/dim]")

        if audit_result.warnings:
            console.print(f"\n[yellow]Warnings ({len(audit_result.warnings)}):[/yellow]")
            for w in audit_result.warnings[:5]:
                console.print(f"  [{w.rule_id}] {w.message} [dim]({w.file})[/dim]")

    # Theme Check
    if theme_check:
        console.print(f"\n[dim]Running Shopify theme check...[/dim]")
        tc_result = run_theme_check(output_dir)
        if not tc_result.available:
            console.print("[yellow]⚠ Shopify CLI theme-check not available[/yellow]")
            console.print("  Install with: [code]npm install -g @shopify/theme-check[/code]")
        else:
            console.print(f"  Errors: {len(tc_result.errors)}")
            console.print(f"  Warnings: {len(tc_result.warnings)}")
            console.print(f"  Suggestions: {len(tc_result.suggestions)}")

    # Done
    console.print(f"\n[bold green]✓ Theme generated successfully![/bold green]")
    console.print(f"  Output: [cyan]{output_dir}/[/cyan]")
    if zip:
        zip_path = str(Path(output_dir).parent / f"{m.name.lower().replace(' ', '-')}.zip")
        console.print(f"  Zip: [cyan]{zip_path}[/cyan]")


@cli.command()
@click.argument('manifest', type=click.Path(exists=True, dir_okay=False))
def validate(manifest):
    """Validate a manifest file without generating."""
    console.print(f"[dim]Validating manifest:[/dim] {manifest}")
    try:
        m = ThemeManifest.from_yaml(manifest)
        console.print(f"[green]✓ Valid![/green] {m.name} v{m.version}")
        console.print(f"  Presets: {len(m.presets)}")
        console.print(f"  Performance target: {m.performance.target_lighthouse_mobile} mobile / {m.performance.target_lighthouse_desktop} desktop")
    except Exception as e:
        console.print(f"[red]✗ Invalid:[/red] {e}")
        sys.exit(1)


@cli.command()
@click.argument('theme_dir', type=click.Path(exists=True, file_okay=False))
def audit(theme_dir):
    """Run static audit on an existing theme directory."""
    console.print(f"[dim]Auditing theme:[/dim] {theme_dir}")
    result = audit_theme(theme_dir)

    table = Table(title="Audit Results", box=box.ROUNDED)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", justify="right")
    table.add_row("Files", str(result.file_count))
    table.add_row("CSS", f"{result.total_css_bytes / 1024:.1f} KB")
    table.add_row("JS", f"{result.total_js_bytes / 1024:.1f} KB")
    table.add_row("Errors", f"[red]{len(result.errors)}[/red]" if result.errors else f"[green]0[/green]")
    table.add_row("Warnings", f"[yellow]{len(result.warnings)}[/yellow]")
    console.print(table)

    if result.errors:
        console.print("\n[red]Errors:[/red]")
        for e in result.errors:
            console.print(f"  [{e.rule_id}] {e.message} [dim]({e.file})[/dim]")

    if result.warnings:
        console.print(f"\n[yellow]Warnings ({len(result.warnings)}):[/yellow]")
        for w in result.warnings:
            console.print(f"  [{w.rule_id}] {w.message} [dim]({w.file})[/dim]")


@cli.command()
def list_sections():
    """List all available section types."""
    from ..core.section import SectionRegistry
    # Import to trigger registration
    from ..components import sections as _sections  # noqa: F401

    sections = SectionRegistry.all()
    table = Table(title=f"Available Sections ({len(sections)})", box=box.ROUNDED)
    table.add_column("Type", style="cyan")
    table.add_column("Name")
    table.add_column("Blocks", justify="right")
    table.add_column("Settings", justify="right")

    for name, cls in sorted(sections.items()):
        table.add_row(
            name,
            cls.name or name,
            str(len(cls.blocks)),
            str(len([s for s in cls.settings if getattr(s, 'id', None)])),
        )
    console.print(table)


@cli.command()
def list_snippets():
    """List all available snippet types."""
    from ..core.snippet import SnippetRegistry
    from ..components import snippets as _snippets  # noqa: F401

    snippets = SnippetRegistry.all()
    table = Table(title=f"Available Snippets ({len(snippets)})", box=box.ROUNDED)
    table.add_column("Name", style="cyan")
    table.add_column("Params")

    for name, snippet in sorted(snippets.items()):
        table.add_row(name, ", ".join(snippet.params) if snippet.params else "-")
    console.print(table)


if __name__ == '__main__':
    cli()
