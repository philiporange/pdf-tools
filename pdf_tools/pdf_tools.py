"""PDF tooling focused on page slicing and Markdown extraction.

This module wraps PyPDF2 for page counting and range-based PDF writing, and it
uses MarkItDown's current API to convert selected page ranges to Markdown. The
class keeps all PDF work in memory when possible so it can target subsets of
large files without rewriting the originals.
"""

from __future__ import annotations

import io
from pathlib import Path
from typing import Sequence, Tuple, Union

from PyPDF2 import PdfReader, PdfWriter
from markitdown import MarkItDown
from markitdown._stream_info import StreamInfo


PdfPath = Union[str, Path]
PageRange = Tuple[int, int]


class PDFTools:
    """Utility class for PDF page operations and Markdown conversion."""

    def __init__(self, markitdown_client: MarkItDown | None = None) -> None:
        """
        Args:
            markitdown_client: Optional MarkItDown instance. When omitted, a
            default MarkItDown() is created with built-in converters enabled.
        """
        self._markitdown = markitdown_client or MarkItDown()

    def get_page_count(self, pdf_path: PdfPath) -> int:
        """Return the number of pages in a PDF."""
        path = Path(pdf_path)
        if not path.is_file():
            raise FileNotFoundError(f"PDF not found: {path}")

        with path.open("rb") as handle:
            reader = PdfReader(handle)
            return len(reader.pages)

    def extract_page_range(
        self,
        pdf_path: PdfPath,
        output_path: PdfPath,
        start_page: int,
        end_page: int,
        *,
        overwrite: bool = False,
    ) -> Path:
        """Write a single inclusive page range to a new PDF."""
        return self.extract_page_ranges(
            pdf_path,
            output_path,
            ranges=[(start_page, end_page)],
            overwrite=overwrite,
        )

    def extract_page_ranges(
        self,
        pdf_path: PdfPath,
        output_path: PdfPath,
        *,
        ranges: Sequence[PageRange],
        overwrite: bool = False,
    ) -> Path:
        """
        Write one or more inclusive page ranges into a new PDF at output_path.

        Page numbers are 1-indexed. Ranges can overlap; pages are appended in
        the order provided. Raises ValueError for invalid ranges and
        FileExistsError when overwrite is False and output already exists.
        """
        if len(ranges) == 0:
            raise ValueError("At least one page range is required.")

        source_path = Path(pdf_path)
        destination = Path(output_path)

        if destination.exists() and not overwrite:
            raise FileExistsError(f"Refusing to overwrite existing file: {destination}")

        with source_path.open("rb") as handle:
            reader = PdfReader(handle)
            page_count = len(reader.pages)
            writer = PdfWriter()

            for start_page, end_page in ranges:
                self._validate_range(start_page, end_page, page_count)
                for page_index in range(start_page - 1, end_page):
                    writer.add_page(reader.pages[page_index])

            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open("wb") as output_file:
                writer.write(output_file)

        return destination

    def markdown_from_range(
        self,
        pdf_path: PdfPath,
        start_page: int,
        end_page: int,
    ) -> str:
        """Convert a single inclusive page range to Markdown."""
        return self.markdown_from_ranges(pdf_path, ranges=[(start_page, end_page)])

    def markdown_from_ranges(
        self,
        pdf_path: PdfPath,
        *,
        ranges: Sequence[PageRange],
    ) -> str:
        """
        Convert selected page ranges to Markdown using MarkItDown.

        The method builds an in-memory PDF containing the requested pages in
        order, then streams it to MarkItDown.convert_stream with a StreamInfo
        hint to ensure the PDF converter is chosen.
        """
        if len(ranges) == 0:
            raise ValueError("At least one page range is required.")

        source_path = Path(pdf_path)
        with source_path.open("rb") as handle:
            reader = PdfReader(handle)
            page_count = len(reader.pages)
            writer = PdfWriter()

            for start_page, end_page in ranges:
                self._validate_range(start_page, end_page, page_count)
                for page_index in range(start_page - 1, end_page):
                    writer.add_page(reader.pages[page_index])

            buffer = io.BytesIO()
            writer.write(buffer)
            buffer.seek(0)

        result = self._markitdown.convert_stream(
            buffer,
            stream_info=StreamInfo(extension=".pdf"),
        )
        return result.markdown

    @staticmethod
    def _validate_range(start_page: int, end_page: int, page_count: int) -> None:
        if start_page < 1 or end_page < 1:
            raise ValueError("Page numbers must be >= 1.")
        if start_page > end_page:
            raise ValueError("start_page must be <= end_page.")
        if end_page > page_count:
            raise ValueError(
                f"end_page {end_page} exceeds total page count {page_count}."
            )
