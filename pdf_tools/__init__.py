"""PDF manipulation and Markdown conversion toolkit.

Extract page ranges from PDFs and convert them to Markdown using
the PDFTools class or the pdftools command-line interface.
"""

from .pdf_tools import PDFTools, PageRange, PdfPath

__version__ = "0.1.0"
__all__ = ["PDFTools", "PageRange", "PdfPath"]
