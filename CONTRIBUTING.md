# Contributing

Thanks for your interest in contributing to the Legendary Theme Generator.

## Getting started

### Setup

```bash
# Clone
git clone https://github.com/LXGNDRY/Legendary_Theme_Generator.git
cd Legendary_Theme_Generator

# Install dev dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Run tests

```bash
pytest
```

### Generate a test theme

```bash
legendary generate examples/streetwear.yaml -o /tmp/test-theme
```

## How to contribute

### Reporting bugs

Open an issue with:

1. What you expected to happen
2. What actually happened
3. Steps to reproduce
4. Your Python version and OS
5. A minimal manifest that triggers the bug (if applicable)

### Adding a new section

1. Read `docs/SECTION_GUIDE.md`
2. Add your section file to `legendary_themes/components/sections/`
3. Add tests in `tests/`
4. Generate a test theme and verify it works in Shopify
5. Open a PR

### Adding a new snippet

1. Add your snippet file to `legendary_themes/components/snippets/`
2. Make sure it has `styles` defined if it needs CSS
3. Add a test that verifies the snippet renders correctly
4. Open a PR

### Fixing a bug

1. Add a test that reproduces the bug
2. Fix the bug
3. Verify all tests pass
4. Open a PR

## Code style

### Python

- Target Python 3.10+
- Use type hints for all function signatures and return types
- Docstrings for all public functions, classes, and modules
- 4-space indentation, 100-char line length (soft)
- Prefer composition over inheritance
- Pydantic for data validation, never raw dicts when a schema is possible

### Liquid (generated output)

- Use `{%- -%}` strip tags for whitespace control
- `| escape` all user-facing text
- `{% render %}`, never `{% include %}`
- Semantic HTML (header, nav, main, article, section, footer)
- WCAG 2.1 AA accessibility requirements
- Mobile-first CSS
- No hardcoded color or spacing values — use design tokens

### JavaScript (generated output)

- Vanilla JS only — no frameworks
- Progressive enhancement — core functionality works without JS
- Module pattern: factory function that returns `{ init, destroy }`
- Event bus for cross-component communication
- Lazy hydration via `data-component` attribute
- No global scope pollution — everything under `window.LTG`

## Commit messages

Use conventional commits:

```
feat: add testimonials section
fix: resolve variant selector not updating price
docs: update manifest reference with accessibility fields
refactor: move CSS generation to separate module
test: add coverage for static audit rules
```

## Pull request checklist

Before opening a PR, make sure:

- [ ] All tests pass (`pytest`)
- [ ] New code has tests
- [ ] Generated theme passes static audit with 0 errors
- [ ] Generated theme works in a Shopify development store
- [ ] Documentation is updated (if applicable)
- [ ] No Dawn-derived patterns — the output must be structurally unique

## Design principles we enforce

1. **Manifest is everything.** No engine-side configuration. Everything comes from the manifest.
2. **No Dawn derivatives.** Generated themes must be structurally distinct.
3. **Generation-time enforcement.** Anything that can be validated should be validated before files are written.
4. **Progressive enhancement.** Browsing and purchasing work without JavaScript.
5. **Accessibility by default.** WCAG 2.1 AA is the baseline, not a stretch goal.
6. **Performance budgets.** CSS < 20KB, JS < 15KB. No creep.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
