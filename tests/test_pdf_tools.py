"""Tests for PDFTools covering page counting, slicing, and Markdown extraction."""

import sys
from pathlib import Path

import pytest
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pdf_tools import PDFTools


def _create_pdf(path: Path, pages: int) -> Path:
    c = canvas.Canvas(str(path), pagesize=letter)
    for idx in range(pages):
        c.drawString(72, 720, f"Page {idx + 1} content")
        c.showPage()
    c.save()
    return path


def test_page_count(tmp_path: Path) -> None:
    pdf_path = _create_pdf(tmp_path / "sample.pdf", pages=3)
    tools = PDFTools()

    assert tools.get_page_count(pdf_path) == 3


def test_extract_page_range(tmp_path: Path) -> None:
    source_pdf = _create_pdf(tmp_path / "source.pdf", pages=4)
    output_pdf = tmp_path / "slice.pdf"
    tools = PDFTools()

    tools.extract_page_range(source_pdf, output_pdf, start_page=2, end_page=3)

    assert output_pdf.exists()
    assert tools.get_page_count(output_pdf) == 2
    markdown = tools.markdown_from_range(output_pdf, start_page=1, end_page=1)
    assert "Page 2 content" in markdown
    assert "Page 1 content" not in markdown


def test_markdown_from_ranges_selects_pages(tmp_path: Path) -> None:
    pdf_path = _create_pdf(tmp_path / "ranges.pdf", pages=3)
    tools = PDFTools()

    markdown = tools.markdown_from_ranges(pdf_path, ranges=[(2, 2)])

    assert "Page 2 content" in markdown
    assert "Page 1 content" not in markdown
    assert "Page 3 content" not in markdown
