# C3 Scripts

All scripts in these folders can be run using

```console
uv --directory script-folder-name run script.py
```

## The Scripts

# markdown-to-pdf

**script**: md_to_pdf.py

Takes a Markdown file and produces a PDF.

```console
% uv --directory markdown-to-pdf run md_to_pdf.py --help
usage: md_to_pdf.py [-h] [--title TITLE] [--author AUTHOR] [--subject SUBJECT]
                    [--css CSS] [--paper {A4,Letter,Legal}] [--sort-by {name,date}]
                    [--no-recursive]
                    input output

Convert Markdown file(s) to PDF using WeasyPrint

positional arguments:
  input                 Input .md file or folder containing .md files
  output                Output PDF file path

options:
  -h, --help            show this help message and exit
  --title TITLE         PDF title (default: file/folder name)
  --author AUTHOR       PDF author
  --subject SUBJECT     PDF subject
  --css CSS             Custom CSS file path (default: templates/default.css)
  --paper {A4,Letter,Legal}
                        Paper size (default: A4)
  --sort-by {name,date}
                        Sort order for folder mode (default: name)
  --no-recursive        Don't include subdirectories (folder mode only)
```
