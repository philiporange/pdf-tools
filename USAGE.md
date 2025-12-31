The `pdf_tools` package provides a Python API and command-line interface for manipulating PDF files, including extracting page ranges and converting PDF content to Markdown. The core functionality is encapsulated in the `PDFTools` class.

### Initializing the PDFTools Class

The `PDFTools` class is the main entry point for all PDF operations. It can be initialized without arguments, which uses a default `MarkItDown` client for conversion, or with a custom `MarkItDown` instance.

*   To begin using the API, instantiate the `PDFTools` class.

```python
from pdf_tools import PDFTools

# Initialize the PDFTools utility
pdf_tools = PDFTools()
```

### Getting the Page Count of a PDF

The `get_page_count` method returns the total number of pages in a specified PDF file.

*   Provide the path to the PDF file to determine its length.

```python
# Assuming 'document.pdf' exists and has 10 pages
# count = pdf_tools.get_page_count("document.pdf")
# print(count)
# Expected output (if document.pdf has 10 pages): 10
```

### Extracting a Single Page Range to a New PDF

The `extract_page_range` method extracts a continuous, inclusive range of pages (1-indexed) from an input PDF and writes them to a new output PDF file.

*   Specify the input path, output path, and the 1-indexed start and end pages.
*   The `overwrite` flag (default `False`) prevents accidental overwriting of the output file.

```python
# Extract pages 10 through 20 (inclusive) from 'document.pdf' to 'output.pdf'
# output_path = pdf_tools.extract_page_range(
#     pdf_path="document.pdf",
#     output_path="output.pdf",
#     start_page=10,
#     end_page=20,
#     overwrite=True
# )
# print(f"Extracted to: {output_path}")
# Expected output: Extracted to: output.pdf
```

### Extracting Multiple Discontinuous Page Ranges

The `extract_page_ranges` method allows combining multiple page ranges (or single pages) into a single output PDF. The pages are appended in the order the ranges are provided.

*   Provide a sequence of `(start_page, end_page)` tuples to define the ranges.
*   This is useful for combining non-contiguous sections of a document.

```python
# Extract pages 1-5, then pages 10-15, and finally page 20
# ranges_to_extract = [(1, 5), (10, 15), (20, 20)]
# output_path = pdf_tools.extract_page_ranges(
#     pdf_path="document.pdf",
#     output_path="multi_range_output.pdf",
#     ranges=ranges_to_extract,
#     overwrite=True
# )
# print(f"Extracted to: {output_path}")
# Expected output: Extracted to: multi_range_output.pdf
```

### Converting a Single Page Range to Markdown

The `markdown_from_range` method converts the content of a specified, inclusive page range into a single string of Markdown text.

*   The method internally creates a temporary PDF containing only the requested pages and streams it to the `MarkItDown` converter.

```python
# Convert pages 1 through 10 to Markdown
# markdown_content = pdf_tools.markdown_from_range(
#     pdf_path="document.pdf",
#     start_page=1,
#     end_page=10,
# )
# print(markdown_content[:50] + "...")
# Expected output (example): # Document Title\n\nThis is the content of page 1...
```

### Converting Multiple Discontinuous Page Ranges to Markdown

The `markdown_from_ranges` method converts multiple non-contiguous page ranges into a single Markdown string.

*   Similar to extraction, provide a sequence of `(start_page, end_page)` tuples. The resulting Markdown will contain the content of these pages concatenated in order.

```python
# Convert pages 1-5 and 10-15 to Markdown
# ranges_to_convert = [(1, 5), (10, 15)]
# markdown_content = pdf_tools.markdown_from_ranges(
#     pdf_path="document.pdf",
#     ranges=ranges_to_convert,
# )
# print(f"Total Markdown length: {len(markdown_content)}")
# Expected output (example): Total Markdown length: 4500
```

### Command Line Interface Usage (CLI)

The package provides a command-line tool, `pdftools`, which mirrors the API functionality.

#### CLI: Getting Page Count

*   Use the `count` command followed by the PDF path.

```bash
# pdftools count document.pdf
# Expected output (if document.pdf has 10 pages): 10
```

#### CLI: Extracting Pages

*   Use the `extract` command, specifying the input PDF, output PDF, and one or more page ranges (e.g., `5`, `10-20`).
*   Use `--force` to overwrite the output file.

```bash
# Extract pages 1-5 and page 10 to output.pdf, forcing overwrite
# pdftools extract document.pdf output.pdf 1-5 10 --force
# Expected output: Extracted pages to: output.pdf
```

#### CLI: Converting Pages to Markdown

*   Use the `markdown` command, specifying the input PDF and page ranges.
*   By default, output is sent to standard output (stdout).

```bash
# Convert pages 1-3 to Markdown and print to console
# pdftools markdown document.pdf 1-3
# Expected output: [Markdown content of pages 1, 2, and 3]
```

*   Use the `-o` or `--output` flag to write the Markdown content to a file.

```bash
# Convert pages 5-10 to Markdown and save to output.md
# pdftools markdown document.pdf 5-10 -o output.md
# Expected output: Markdown written to: output.md
```