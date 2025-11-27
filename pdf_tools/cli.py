#!/usr/bin/env python3
"""Command-line interface for PDF manipulation and Markdown conversion.

This CLI exposes all functionality from the pdf_tools package including page
counting, page range extraction, and Markdown conversion from PDF pages.
"""

import argparse
import sys
from pathlib import Path

from pdf_tools import PDFTools


def parse_page_range(range_str: str) -> tuple[int, int]:
    """Parse a page range string like '1-5' or '10' into (start, end) tuple.

    Args:
        range_str: String in format 'N' or 'N-M' where N and M are page numbers

    Returns:
        Tuple of (start_page, end_page)

    Raises:
        ValueError: If range format is invalid
    """
    if "-" in range_str:
        parts = range_str.split("-")
        if len(parts) != 2:
            raise ValueError(f"Invalid range format: {range_str}")
        start, end = int(parts[0]), int(parts[1])
        return (start, end)
    else:
        page = int(range_str)
        return (page, page)


def cmd_count(args: argparse.Namespace) -> int:
    """Handle the 'count' subcommand to get page count."""
    try:
        pdf_tools = PDFTools()
        count = pdf_tools.get_page_count(args.pdf)
        print(count)
        return 0
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error counting pages: {e}", file=sys.stderr)
        return 1


def cmd_extract(args: argparse.Namespace) -> int:
    """Handle the 'extract' subcommand to extract page ranges."""
    try:
        # Parse all page ranges
        ranges = [parse_page_range(r) for r in args.ranges]

        pdf_tools = PDFTools()
        output_path = pdf_tools.extract_page_ranges(
            pdf_path=args.pdf,
            output_path=args.output,
            ranges=ranges,
            overwrite=args.force,
        )
        print(f"Extracted pages to: {output_path}")
        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except FileExistsError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("Use --force to overwrite existing files", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error extracting pages: {e}", file=sys.stderr)
        return 1


def cmd_markdown(args: argparse.Namespace) -> int:
    """Handle the 'markdown' subcommand to convert PDF pages to Markdown."""
    try:
        # Parse all page ranges
        ranges = [parse_page_range(r) for r in args.ranges]

        pdf_tools = PDFTools()
        markdown_content = pdf_tools.markdown_from_ranges(
            pdf_path=args.pdf,
            ranges=ranges,
        )

        # Output to file or stdout
        if args.output:
            output_path = Path(args.output)
            if output_path.exists() and not args.force:
                print(f"Error: {output_path} already exists", file=sys.stderr)
                print("Use --force to overwrite existing files", file=sys.stderr)
                return 1
            output_path.write_text(markdown_content)
            print(f"Markdown written to: {output_path}")
        else:
            print(markdown_content)

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error converting to markdown: {e}", file=sys.stderr)
        return 1


def main() -> int:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="PDF manipulation and Markdown conversion tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get page count
  %(prog)s count document.pdf

  # Extract single page
  %(prog)s extract document.pdf output.pdf 5

  # Extract page range
  %(prog)s extract document.pdf output.pdf 10-20

  # Extract multiple ranges
  %(prog)s extract document.pdf output.pdf 1-5 10-15 20

  # Convert pages to Markdown (output to stdout)
  %(prog)s markdown document.pdf 1-10

  # Convert pages to Markdown file
  %(prog)s markdown document.pdf 1-10 -o output.md

  # Force overwrite existing files
  %(prog)s extract document.pdf output.pdf 1-5 --force
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 'count' subcommand
    count_parser = subparsers.add_parser(
        "count",
        help="Get the number of pages in a PDF",
    )
    count_parser.add_argument(
        "pdf",
        help="Path to the PDF file",
    )

    # 'extract' subcommand
    extract_parser = subparsers.add_parser(
        "extract",
        help="Extract page ranges to a new PDF",
    )
    extract_parser.add_argument(
        "pdf",
        help="Path to the input PDF file",
    )
    extract_parser.add_argument(
        "output",
        help="Path to the output PDF file",
    )
    extract_parser.add_argument(
        "ranges",
        nargs="+",
        help="Page ranges to extract (e.g., '5' for page 5, '10-20' for pages 10 through 20)",
    )
    extract_parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="Overwrite output file if it exists",
    )

    # 'markdown' subcommand
    markdown_parser = subparsers.add_parser(
        "markdown",
        help="Convert PDF page ranges to Markdown",
    )
    markdown_parser.add_argument(
        "pdf",
        help="Path to the input PDF file",
    )
    markdown_parser.add_argument(
        "ranges",
        nargs="+",
        help="Page ranges to convert (e.g., '5' for page 5, '10-20' for pages 10 through 20)",
    )
    markdown_parser.add_argument(
        "-o", "--output",
        help="Output file path (if not specified, prints to stdout)",
    )
    markdown_parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="Overwrite output file if it exists",
    )

    args = parser.parse_args()

    # Show help if no command specified
    if not args.command:
        parser.print_help()
        return 1

    # Dispatch to appropriate handler
    if args.command == "count":
        return cmd_count(args)
    elif args.command == "extract":
        return cmd_extract(args)
    elif args.command == "markdown":
        return cmd_markdown(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
