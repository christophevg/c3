#!/usr/bin/env python3
"""
Simple Markdown to HTML converter for git-activity-report.

Handles the specific Markdown elements used in the report:
- Headers (# ## ###)
- Bold (**text**)
- Tables
- Lists (- item)
- Horizontal rules (---)
- Paragraphs
"""

import re
import sys


def convert_table(lines: list[str]) -> list[str]:
  """Convert Markdown table to HTML."""
  html = ["<table>"]

  for i, line in enumerate(lines):
    if not line.strip():
      continue

    cells = [c.strip() for c in line.split("|") if c.strip()]

    # Skip separator lines (|---|---|)
    if all(set(c) <= {"-", ":", " "} for c in cells):
      continue

    # Convert bold in cells
    cells = [re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', c) for c in cells]

    if i == 0:
      html.append("  <thead>")
      html.append("    <tr>")
      for cell in cells:
        html.append(f"      <th>{cell}</th>")
      html.append("    </tr>")
      html.append("  </thead>")
      html.append("  <tbody>")
    else:
      html.append("    <tr>")
      for cell in cells:
        html.append(f"      <td>{cell}</td>")
      html.append("    </tr>")

  html.append("  </tbody>")
  html.append("</table>")
  return html


def convert_markdown(md: str) -> str:
  """Convert Markdown to HTML."""
  lines = md.split("\n")
  html_lines = []
  i = 0

  while i < len(lines):
    line = lines[i]

    # Horizontal rule
    if line.strip() == "---":
      html_lines.append("<hr>")
      i += 1
      continue

    # Headers
    if line.startswith("### "):
      html_lines.append(f"<h3>{line[4:].strip()}</h3>")
      i += 1
      continue
    if line.startswith("## "):
      html_lines.append(f"<h2>{line[3:].strip()}</h2>")
      i += 1
      continue
    if line.startswith("# "):
      html_lines.append(f"<h1>{line[2:].strip()}</h1>")
      i += 1
      continue

    # Table detection
    if "|" in line and i + 1 < len(lines) and "|" in lines[i + 1]:
      # Collect table lines
      table_lines = []
      while i < len(lines) and "|" in lines[i]:
        table_lines.append(lines[i])
        i += 1
      html_lines.extend(convert_table(table_lines))
      continue

    # List items
    if line.startswith("- "):
      html_lines.append(f"<li>{line[2:].strip()}</li>")
      i += 1
      continue

    # Empty line
    if not line.strip():
      html_lines.append("")
      i += 1
      continue

    # Bold text
    line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)

    # Regular paragraph
    if line.strip():
      html_lines.append(f"<p>{line}</p>")

    i += 1

  html = "\n".join(html_lines)

  # Wrap consecutive <li> in <ul>
  html = re.sub(r'(<li>.*?</li>\n)+', lambda m: f"<ul>\n{m.group(0)}</ul>\n", html)

  return html


def wrap_email(html: str, title: str = "Activity Report") -> str:
  """Wrap HTML in email-friendly structure with styling."""
  return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
      color: #333;
      max-width: 800px;
      margin: 0 auto;
      padding: 20px;
    }}
    h1 {{
      color: #2c3e50;
      border-bottom: 2px solid #3498db;
      padding-bottom: 10px;
    }}
    h2 {{
      color: #34495e;
      margin-top: 30px;
    }}
    h3 {{
      color: #7f8c8d;
      margin-top: 20px;
    }}
    table {{
      border-collapse: collapse;
      width: 100%;
      margin: 15px 0;
    }}
    th, td {{
      border: 1px solid #ddd;
      padding: 10px 12px;
      text-align: left;
    }}
    th {{
      background-color: #3498db;
      color: white;
    }}
    tr:nth-child(even) {{
      background-color: #f9f9f9;
    }}
    ul {{
      padding-left: 20px;
      margin: 10px 0;
    }}
    li {{
      margin: 5px 0;
    }}
    hr {{
      border: none;
      border-top: 1px solid #eee;
      margin: 20px 0;
    }}
    .footer {{
      color: #888;
      font-size: 0.9em;
      font-style: italic;
    }}
  </style>
</head>
<body>
{html}
</body>
</html>"""


def main():
  md = sys.stdin.read()
  html = convert_markdown(md)
  full_html = wrap_email(html)
  print(full_html)


if __name__ == "__main__":
  main()