# Markdown to PDF Skill

A Claude Code skill for converting folders of Markdown files to a single PDF document using WeasyPrint for full CSS support.

## Research

See [research/2026-03-31-markdown-to-pdf/](../../research/2026-03-31-markdown-to-pdf/) for initial research on Python libraries.

See [research/2026-04-02-markdown-pdf-python-libraries/](../../research/2026-04-02-markdown-pdf-python-libraries/) for comparison of WeasyPrint vs alternatives.

## Implementation

### Files

```
skills/markdown-to-pdf/
├── SKILL.md           # Main skill instructions
├── REFERENCE.md       # WeasyPrint API reference
└── README.md          # This file

scripts/markdown-to-pdf/
├── md_to_pdf.py       # Conversion utility script
├── pyproject.toml     # minimal project setup
└── templates/
    └── default.css   # Default PDF styling
```

### Usage

```bash
# Basic usage
uv run ${CLAUDE_PLUGIN_ROOT}/scripts/markdown-to-pdf/md_to_pdf.py <folder> <output.pdf>

# With options
uv run ${CLAUDE_PLUGIN_ROOT}/scripts/markdown-to-pdf/md_to_pdf.py docs/ output.pdf \
  --title "Documentation" \
  --author "Team" \
  --css templates/default.css \
  --paper A4 \
  --sort-by name
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--title` | Folder name | PDF title |
| `--author` | Current user | PDF author |
| `--subject` | None | PDF subject |
| `--css` | script's templates/default.css (automatic) | Custom CSS file path |
| `--paper` | A4 | Paper size (A4, Letter, Legal) |
| `--sort-by` | name | Sort order (name, date) |
| `--no-recursive` | False | Exclude subdirectories |

## CSS Support

WeasyPrint provides full CSS3 support, including:

- `background-color` on table headers (the issue with markdown-pdf)
- Page breaks with `break-inside: avoid`
- Page numbers in `@page` margin boxes
- Custom fonts via `@font-face`
- Automatic bookmarks/TOC from headings

## Status

**Phase**: Rebuilt with WeasyPrint to fix table styling

## Why WeasyPrint?

The previous implementation used `markdown-pdf` which relies on PyMuPDF's Story API. That API has a bug where `background-color` on `<th>` elements causes scattered grey rectangles throughout the document.

WeasyPrint provides full CSS support without this limitation, making it the recommended choice for styled PDFs from Markdown.
