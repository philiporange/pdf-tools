# pdf_tools

PDF manipulation and Markdown conversion toolkit. Extract page ranges from PDFs and convert them to Markdown using a simple Python API or command-line interface.

## Features

- Extract single pages or multiple page ranges from PDFs
- Convert PDF pages to Markdown
- Get page counts from PDF files
- Python API for programmatic use
- Command-line interface for quick operations
- Combine multiple page ranges in a single operation

## Installation

```bash
pip install -e .
```

Or install dependencies manually:

```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

Get page count:
```bash
pdftools count document.pdf
```

Extract single page:
```bash
pdftools extract document.pdf output.pdf 5
```

Extract page range:
```bash
pdftools extract document.pdf output.pdf 10-20
```

Extract multiple ranges:
```bash
pdftools extract document.pdf output.pdf 1-5 10-15 20
```

Convert pages to Markdown (stdout):
```bash
pdftools markdown document.pdf 1-10
```

Convert pages to Markdown file:
```bash
pdftools markdown document.pdf 1-10 -o output.md
```

Force overwrite existing files:
```bash
pdftools extract document.pdf output.pdf 1-5 --force
```

### Python API

```python
from pdf_tools import PDFTools

pdf = PDFTools()

# Get page count
count = pdf.get_page_count("document.pdf")

# Extract a single page range
pdf.extract_page_range(
    pdf_path="document.pdf",
    output_path="output.pdf",
    start_page=10,
    end_page=20,
)

# Extract multiple page ranges
pdf.extract_page_ranges(
    pdf_path="document.pdf",
    output_path="output.pdf",
    ranges=[(1, 5), (10, 15), (20, 20)],
)

# Convert pages to Markdown
markdown = pdf.markdown_from_range(
    pdf_path="document.pdf",
    start_page=1,
    end_page=10,
)

# Convert multiple ranges to Markdown
markdown = pdf.markdown_from_ranges(
    pdf_path="document.pdf",
    ranges=[(1, 5), (10, 15)],
)
```

## API Reference

### PDFTools

Main class providing PDF manipulation functionality.

#### Methods

**`get_page_count(pdf_path: PdfPath) -> int`**

Returns the total number of pages in a PDF.

**`extract_page_range(pdf_path, output_path, start_page, end_page, *, overwrite=False) -> Path`**

Extracts a single inclusive page range to a new PDF file. Page numbers are 1-indexed.

**`extract_page_ranges(pdf_path, output_path, *, ranges, overwrite=False) -> Path`**

Extracts multiple inclusive page ranges to a new PDF file. Ranges can overlap and are appended in order.

**`markdown_from_range(pdf_path, start_page, end_page) -> str`**

Converts a single page range to Markdown text.

**`markdown_from_ranges(pdf_path, *, ranges) -> str`**

Converts multiple page ranges to Markdown text.

## Dependencies

- click - Command-line interface
- markitdown - PDF to Markdown conversion
- PyPDF2 - PDF reading and manipulation
- reportlab - PDF generation support
