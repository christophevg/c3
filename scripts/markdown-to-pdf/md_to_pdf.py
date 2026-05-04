#!/usr/bin/env python3
"""
Convert Markdown file(s) to a single PDF document using WeasyPrint.

This module provides full CSS support including background-color on table headers,
addressing the PyMuPDF Story API limitation in markdown-pdf.

Usage:
    python md_to_pdf.py <input> <output.pdf> [options]

Input can be:
    - A single .md file
    - A folder containing .md files

Options:
    --title TEXT        PDF title (default: file/folder name)
    --author TEXT       PDF author (default: current user)
    --subject TEXT      PDF subject
    --css PATH          Custom CSS file path
    --paper TEXT        Paper size: A4, Letter, Legal (default: A4)
    --sort-by TEXT      Sort order: name, date (default: name, folder mode only)
    --no-recursive      Don't include subdirectories (folder mode only)
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

from markdown_it import MarkdownIt


def collect_markdown_files(folder: Path, recursive: bool = True) -> list[Path]:
    """Collect all markdown files from a folder."""
    pattern = "**/*.md" if recursive else "*.md"
    return list(folder.glob(pattern))


def sort_files(files: list[Path], sort_by: str) -> list[Path]:
    """Sort files by name or modification date."""
    if sort_by == "date":
        return sorted(files, key=lambda f: f.stat().st_mtime)
    return sorted(files)


def markdown_to_html(markdown_content: str, md_parser: MarkdownIt) -> str:
    """Convert Markdown content to HTML."""
    return md_parser.render(markdown_content)


def create_html_document(
    sections: list[tuple[str, str]],  # [(title, html_content), ...]
    title: str,
    author: str,
    subject: str | None,
    css_path: Path | None,
) -> str:
    """Create a complete HTML document with metadata and sections."""

    # Build meta tags
    meta_tags = [
        f'<meta name="author" content="{author}">',
        f'<meta name="dcterms.created" content="{datetime.now().isoformat()}">',
    ]
    if subject:
        meta_tags.append(f'<meta name="description" content="{subject}">')

    # Build CSS link - resolve to absolute path for URI
    style_link = ""
    if css_path:
        abs_css_path = css_path.resolve()
        style_link = f'<link rel="stylesheet" href="{abs_css_path.as_uri()}">'

    # Build sections HTML
    sections_html = []
    for section_title, section_content in sections:
        sections_html.append(f"<section>\n{section_content}\n</section>")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    {chr(10).join(meta_tags)}
    {style_link}
</head>
<body>
{chr(10).join(sections_html)}
</body>
</html>"""
    return html


def create_pdf(
    files: list[Path],
    title: str,
    author: str,
    subject: str | None,
    paper_size: str,
    css_path: Path | None,
    output_path: Path,
) -> None:
    """Create PDF from markdown files using WeasyPrint."""
    from weasyprint import HTML, CSS

    # Initialize markdown parser with GFM extensions (tables, strikethrough)
    md = MarkdownIt("commonmark", {"html": True}).enable("table")

    # Convert each file to HTML
    sections = []
    for md_file in files:
        content = md_file.read_text(encoding="utf-8")
        html = markdown_to_html(content, md)
        sections.append((md_file.stem, html))

    # Create HTML document
    html_content = create_html_document(
        sections=sections,
        title=title,
        author=author,
        subject=subject,
        css_path=css_path,
    )

    # Base URL for resolving relative paths (images, links)
    base_url = files[0].parent if files else Path.cwd()

    # Create PDF
    html_doc = HTML(string=html_content, base_url=str(base_url))

    # Prepare stylesheets
    stylesheets = []
    if css_path and css_path.exists():
        stylesheets.append(CSS(filename=str(css_path)))

    # Paper size CSS
    paper_sizes = {
        "A4": "A4",
        "Letter": "Letter",
        "Legal": "Legal",
    }
    page_css = CSS(string=f"@page {{ size: {paper_sizes.get(paper_size, 'A4')}; margin: 2cm; }}")
    stylesheets.append(page_css)

    # Write PDF to file
    html_doc.write_pdf(target=str(output_path), stylesheets=stylesheets)


PAPER_SIZES = {
    "A4": "A4",
    "Letter": "Letter",
    "Legal": "Legal",
}


def main():
    parser = argparse.ArgumentParser(
        description="Convert Markdown file(s) to PDF using WeasyPrint"
    )
    parser.add_argument("input", help="Input .md file or folder containing .md files")
    parser.add_argument("output", help="Output PDF file path")
    parser.add_argument("--title", help="PDF title (default: file/folder name)")
    parser.add_argument("--author", help="PDF author")
    parser.add_argument("--subject", help="PDF subject")
    parser.add_argument("--css", help="Custom CSS file path (default: templates/default.css)")
    parser.add_argument(
        "--paper", choices=PAPER_SIZES.keys(), default="A4",
        help="Paper size (default: A4)"
    )
    parser.add_argument(
        "--sort-by", choices=["name", "date"], default="name",
        help="Sort order for folder mode (default: name)"
    )
    parser.add_argument(
        "--no-recursive", action="store_true",
        help="Don't include subdirectories (folder mode only)"
    )

    args = parser.parse_args()

    # Validate input
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input not found: {input_path}")
        sys.exit(1)

    # Determine if input is a file or folder
    if input_path.is_file():
        if not input_path.suffix.lower() == ".md":
            print(f"Error: Input file must be a .md file: {input_path}")
            sys.exit(1)
        files = [input_path]
        default_title = input_path.stem
        print(f"Processing single file: {input_path.name}")
    else:
        files = collect_markdown_files(input_path, recursive=not args.no_recursive)
        if not files:
            print(f"Error: No markdown files found in {input_path}")
            sys.exit(1)
        files = sort_files(files, args.sort_by)
        default_title = input_path.name
        print(f"Found {len(files)} markdown file(s)")
        print(f"Sorted by: {args.sort_by}")

    # Set defaults
    title = args.title or default_title
    author = args.author or Path.home().name

    # Determine CSS path - default to templates/default.css in script directory
    script_dir = Path(__file__).parent
    default_css = script_dir / "templates" / "default.css"

    if args.css:
        css_path = Path(args.css)
        if not css_path.exists():
            print(f"Warning: CSS file not found: {css_path}")
            css_path = None
    else:
        css_path = default_css
        if not css_path.exists():
            print(f"Warning: Default CSS not found: {css_path}")
            css_path = None

    # Create PDF
    output_path = Path(args.output)
    print(f"Creating PDF: {args.output}")
    print(f"  Title: {title}")
    print(f"  Paper: {args.paper}")

    try:
        create_pdf(
            files=files,
            title=title,
            author=author,
            subject=args.subject,
            paper_size=args.paper,
            css_path=css_path,
            output_path=output_path,
        )
    except ImportError:
        print("Error: weasyprint not installed.")
        print("Install with: pip install weasyprint")
        print("On macOS, you may also need: brew install pango")
        sys.exit(1)

    # Verify output
    if output_path.exists() and output_path.stat().st_size > 0:
        size_kb = output_path.stat().st_size / 1024
        print(f"Success: Created {args.output} ({size_kb:.1f} KB)")
    else:
        print(f"Error: Failed to create {args.output}")
        sys.exit(1)


if __name__ == "__main__":
    main()
