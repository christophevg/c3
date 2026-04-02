# API Reference: WeasyPrint

Reference documentation for WeasyPrint, the PDF rendering engine used by this skill.

## Installation

```bash
# macOS
brew install pango
pip install weasyprint

# Linux (Debian/Ubuntu)
apt install libpango-1.0-0 libpangocairo-1.0-0
pip install weasyprint
```

Dependencies: Python ≥ 3.10, Pango ≥ 1.44

## Core Classes

### HTML

Represents an HTML document for PDF conversion.

```python
from weasyprint import HTML

# From file
html = HTML('document.html')

# From URL
html = HTML('https://example.com/page.html')

# From string with base URL
html = HTML(string='<html>...</html>', base_url='/path/to/resources/')
```

**Parameters:**
- `filename`: Path to HTML file
- `url`: URL to fetch
- `string`: HTML content as string
- `base_url`: Base URL for resolving relative paths (images, links)

### CSS

Represents a CSS stylesheet.

```python
from weasyprint import CSS

# From file
css = CSS(filename='styles.css')

# From string
css = CSS(string='body { font-size: 12pt; }')
```

### Document

The rendered PDF document.

```python
# Write to file
html.write_pdf('output.pdf')

# Write with stylesheets
html.write_pdf('output.pdf', stylesheets=[CSS(filename='custom.css')])

# Get PDF as bytes
pdf_bytes = html.write_pdf()
```

## PDF Metadata

Metadata is extracted from HTML:

```html
<!DOCTYPE html>
<html>
<head>
  <title>Document Title</title>
  <meta name="author" content="Author Name">
  <meta name="description" content="Document subject/description">
  <meta name="keywords" content="keyword1, keyword2">
  <meta name="dcterms.created" content="2026-04-02">
</head>
<body>...</body>
</html>
```

| HTML Element | PDF Field |
|--------------|-----------|
| `<title>` | `/Title` |
| `<meta name=author>` | `/Author` |
| `<meta name=description>` | `/Subject` |
| `<meta name=keywords>` | `/Keywords` |
| `<meta name=dcterms.created>` | `/CreationDate` |

## CSS Support

### Page Setup

```css
@page {
  size: A4;           /* A4, Letter, Legal, or custom [width, height] */
  margin: 2cm;        /* Uniform margins */
  margin: 1cm 2cm;    /* Vertical, horizontal */
  margin: 1cm 2cm 3cm; /* Top, horizontal, bottom */
  
  @top-center {
    content: "Header Text";
  }
  
  @bottom-center {
    content: "Page " counter(page);
  }
}
```

### Table of Contents / Bookmarks

Bookmarks are generated automatically from headings. Control with CSS:

```css
/* Include heading level in bookmarks */
h1 { bookmark-level: 1; }
h2 { bookmark-level: 2; }
h3 { bookmark-level: 3; }

/* Exclude from bookmarks */
h1.title { bookmark-level: none; }

/* Custom bookmark label */
h2 { bookmark-label: content() " - Section"; }
```

### Page Breaks

```css
/* Force page break before */
h1 { page-break-before: always; }

/* Avoid breaking inside */
table, pre, figure { page-break-inside: avoid; }

/* Keep with next */
h2 { page-break-after: avoid; }
```

### Tables

WeasyPrint provides full CSS support for tables:

```css
/* Table header with background */
th {
  background-color: #2c3e50;
  color: white;
  font-weight: bold;
  padding: 12px;
}

/* Striped rows */
tr:nth-child(even) {
  background-color: #f8f9fa;
}

/* Repeat headers across pages */
thead {
  break-after: avoid;
}

/* Avoid breaking inside table */
table {
  break-inside: avoid;
}
```

### Fonts

```css
@font-face {
  font-family: 'CustomFont';
  src: url('fonts/custom.woff2') format('woff2');
}

body {
  font-family: 'CustomFont', sans-serif;
}
```

## Programmatic TOC Access

Access the bookmark/TOC structure programmatically:

```python
from weasyprint import HTML

document = HTML('document.html').render()
bookmarks = document.make_bookmark_tree()

def print_toc(bookmarks, indent=0):
    for bookmark in bookmarks:
        page = bookmark.destination[0]
        print(f"{'  ' * indent}{bookmark.label} (page {page})")
        print_toc(bookmark.children, indent + 1)

print_toc(bookmarks)
```

## Complete Example

```python
from pathlib import Path
from weasyprint import HTML, CSS
from markdown_it import MarkdownIt

# Convert Markdown to HTML
md = MarkdownIt("commonmark", {"html": True})

markdown_files = sorted(Path("docs").glob("*.md"))

html_content = """<!DOCTYPE html>
<html>
<head>
  <title>Documentation</title>
  <meta name="author" content="Team">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
"""

for md_file in markdown_files:
    html_content += md.render(md_file.read_text())

html_content += "</body></html>"

# Create PDF
HTML(string=html_content, base_url="docs/").write_pdf(
    "output.pdf",
    stylesheets=[CSS(filename="styles.css")]
)
```

## Dependencies

- **markdown-it-py**: Markdown to HTML conversion
- **WeasyPrint**: HTML/CSS to PDF conversion
- **Pango**: Text rendering (system library)

## Limitations

WeasyPrint has excellent CSS support but some limitations:

**Not Supported:**
- `box-shadow` (use `border` alternatives)
- 3D transforms
- `visibility: collapse` on tables
- Right-to-left/bidirectional text (limited support)

**Partially Supported:**
- JavaScript (not supported - documents must be static)
- Complex Grid layouts (basic support)
- Repeating table headers across pages (may have issues)