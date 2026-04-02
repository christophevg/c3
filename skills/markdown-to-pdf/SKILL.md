---
name: converting-markdown-to-pdf
description: Converts folders of Markdown files to a single PDF document with table of contents, CSS styling, and image support. Use when the user asks to convert markdown to PDF, generate PDFs from documentation folders, create reports from markdown, or bundle markdown files into a single document.
---

# Converting Markdown to PDF

Convert a folder of Markdown files into a single, professionally formatted PDF document using WeasyPrint for full CSS support.

## Skill Location

All file paths in this skill are relative to the skill's base directory. When the skill is invoked, the base directory is provided in the context:

```
Base directory for this skill: <path-to-skill>
```

Use this base directory to resolve paths like:
- `$SKILL_DIR/requirements.txt` — Python dependencies
- `$SKILL_DIR/scripts/md_to_pdf.py` — Conversion script
- `$SKILL_DIR/templates/default.css` — Default CSS styling

In command examples below, `$SKILL_DIR` represents this base directory path.

## Prerequisites

This skill requires a Python virtual environment with WeasyPrint installed.

### Environment Setup

Before running the conversion script, ensure a pyenv virtual environment is active:

**Option 1: Use existing environment**
```bash
# Check if an environment is active
pyenv version-name

# If not, activate one
pyenv activate <env-name>
```

**Option 2: Create dedicated environment**
```bash
# Create a dedicated environment for this skill
pyenv virtualenv 3.11 md-to-pdf

# Activate it
pyenv activate md-to-pdf

# Install dependencies
pip install -r $SKILL_DIR/requirements.txt
```

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
- [ ] Step 1: Verify pyenv environment is active
- [ ] Step 2: Install dependencies if needed
- [ ] Step 3: Validate input folder exists
- [ ] Step 4: Configure PDF options
- [ ] Step 5: Generate PDF
- [ ] Step 6: Verify output created
```

**Step 1: Verify environment**

Check that a pyenv environment is active:
```bash
pyenv version-name
```

If the command fails or returns "system", ask the user which environment to use. Offer `md-to-pdf` as the default:

```
No pyenv virtual environment is active. Would you like to:
1. Create a new environment named 'md-to-pdf'
2. Use an existing environment (specify name)
```

**Step 2: Check and install dependencies**

Check if WeasyPrint is installed in the active environment:
```bash
python -c "import weasyprint" 2>&1
```

If dependencies are missing, ask the user which environment to use:

```
The current environment '<name>' doesn't have the required dependencies (WeasyPrint). Would you like to:
1. Install dependencies in the current environment '<name>'
2. Create/use a dedicated 'md-to-pdf' environment
3. Use an existing environment (specify name)
```

Wait for the user's choice before proceeding with installation.

To install dependencies:
```bash
pip install -r $SKILL_DIR/requirements.txt
```

**Step 3: Validate input folder**

Confirm the folder exists and contains `.md` files:
```bash
ls -la <folder>/*.md
```

**Step 4: Configure PDF options**

| Option | Default | Description |
|--------|---------|-------------|
| `--title` | Folder name | PDF title |
| `--author` | Current user | PDF author |
| `--subject` | None | PDF subject |
| `--css` | templates/default.css | Custom CSS file path (defaults to skill's stylesheet) |
| `--paper` | A4 | Paper size (A4, Letter, Legal) |

The default stylesheet provides professional formatting with:
- Condensed typography for efficient use of space
- Styled table headers with background colors
- Page numbers in footer
- Proper code block and blockquote styling

**Step 5: Generate PDF**

```bash
python $SKILL_DIR/scripts/md_to_pdf.py <folder> <output.pdf> --title "Title"
```

**Step 6: Verify output**

```bash
ls -la <output.pdf>
# Should show file size > 0
```

## Quick Start

```bash
# Activate/create environment
pyenv activate md-to-pdf 2>/dev/null || pyenv virtualenv 3.11 md-to-pdf && pyenv activate md-to-pdf

# Install dependencies
pip install -r $SKILL_DIR/requirements.txt

# Convert
python $SKILL_DIR/scripts/md_to_pdf.py docs/ output.pdf --title "Documentation"
```

## Advanced Usage

### Custom CSS Styling

To override the default stylesheet with a custom one:

```bash
python $SKILL_DIR/scripts/md_to_pdf.py docs/ output.pdf --css custom.css
```

WeasyPrint provides full CSS3 support including:
- `background-color` on table headers
- Page breaks with `break-inside: avoid`
- Page numbers in `@page` margin boxes
- Custom fonts via `@font-face`

### Single File Mode

```bash
python $SKILL_DIR/scripts/md_to_pdf.py document.md output.pdf
```

### Date-based Ordering

```bash
python $SKILL_DIR/scripts/md_to_pdf.py docs/ output.pdf --sort-by date
```

## Troubleshooting

**Problem: "No pyenv virtual environment is active"**

Create or activate one:
```bash
pyenv virtualenv 3.11 md-to-pdf
pyenv activate md-to-pdf
pip install -r $SKILL_DIR/requirements.txt
```

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
- [templates/default.css](templates/default.css) — Default compact styling
- [requirements.txt](requirements.txt) — Python dependencies