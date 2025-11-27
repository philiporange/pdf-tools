#!/usr/bin/env python3
"""Extract page 200 from CompletePubQuizNightBook.pdf to test.pdf."""

from pathlib import Path
from pdf_tools import PDFTools

# Initialize PDF tools
pdf_tools = PDFTools()

# Source and destination paths
source_pdf = Path.home() / "Downloads" / "CompletePubQuizNightBook.pdf"
output_pdf = Path("test.pdf")

# Extract page 200 (single page, so start_page=200, end_page=200)
pdf_tools.extract_page_range(
    pdf_path=source_pdf,
    output_path=output_pdf,
    start_page=200,
    end_page=200,
    overwrite=True,
)

print(f"Successfully extracted page 200 to {output_pdf}")
