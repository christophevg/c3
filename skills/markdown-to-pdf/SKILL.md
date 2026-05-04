---
name: converting-markdown-to-pdf
description: Converts folders of Markdown files to a single PDF document with table of contents, CSS styling, and image support. Use when the user asks to convert markdown to PDF, generate PDFs from documentation folders, create reports from markdown, or bundle markdown files into a single document.
---

# Converting Markdown to PDF

Convert a folder of Markdown files into a single, professionally formatted PDF document using WeasyPrint for full CSS support.

## Prerequisites

### System Dependencies (macOS)

WeasyPrint requires Pango:

```bash
brew install pango
```

### System Dependencies (Linux)

```bash
apt install libpango-1.0-0 libpangocairo-1.0-0
```

## Workflow

Copy this checklist and track progress:

```
Markdown to PDF Progress:
- [ ] Step 1: Validate input folder exists
- [ ] Step 2: Configure PDF options
- [ ] Step 3: Generate PDF
- [ ] Step 4: Verify output created
```

**Step 1: Validate input folder**

Confirm the folder exists and contains `.md` files:
```bash
ls -la <folder>/*.md
```

**Step 2: Configure PDF options**

| Option | Default | Description |
|--------|---------|-------------|
| `--title` | Folder name | PDF title |
| `--author` | Current user | PDF author |
| `--subject` | None | PDF subject |
| `--css` | script's templates/default.css (automatic resolution) | Custom CSS file path |
| `--paper` | A4 | Paper size (A4, Letter, Legal) |

The default stylesheet is automatically applied from the script's templates/ folder. It provides professional formatting with:
- Condensed typography for efficient use of space
- Styled table headers with background colors
- Page numbers in footer
- Proper code block and blockquote styling

**Step 3: Generate PDF**

The script is in the C3 scripts folder and can be executed using `uv`:

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/scripts/markdown-to-pdf/md_to_pdf.py <folder> <output.pdf> --title "Title"
```

**Step 4: Verify output**

```bash
ls -la <output.pdf>
# Should show file size > 0
```

## Advanced Usage

### Custom CSS Styling

To override the default stylesheet with a custom one:

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/scripts/markdown-to-pdf/md_to_pdf.py docs/ output.pdf --css custom.css
```

WeasyPrint provides full CSS3 support including:
- `background-color` on table headers
- Page breaks with `break-inside: avoid`
- Page numbers in `@page` margin boxes
- Custom fonts via `@font-face`

### Single File Mode

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/scripts/markdown-to-pdf/md_to_pdf.py document.md output.pdf
```

### Date-based Ordering

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/scripts/markdown-to-pdf/md_to_pdf.py docs/ output.pdf --sort-by date
```

## Troubleshooting

**Problem: Images not appearing**

Images must use relative paths from the markdown file location.

**Problem: Installation fails on macOS**

```bash
brew install pango
pip install weasyprint
```

**Problem: Tables not rendering correctly**

Ensure the script uses `.enable('table')` on the Markdown parser. This is included by default.

## Reference

- [REFERENCE.md](REFERENCE.md) — WeasyPrint API documentation
- [templates/default.css](../../scripts/markdown-to-pdf/templates/default.css) — Default compact styling
- [pyproject.toml](../../scripts/markdown-to-pdf/pyproject.toml) — Python dependencies
