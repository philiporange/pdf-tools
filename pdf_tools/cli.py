"""Command-line interface for PDF manipulation and Markdown conversion.

This CLI exposes all functionality from the pdf_tools package including page
counting, page range extraction, and Markdown conversion from PDF pages.
"""

import click
from pathlib import Path

from . import __version__
from .pdf_tools import PDFTools


def parse_page_range(range_str: str) -> tuple[int, int]:
    """Parse a page range string like '1-5' or '10' into (start, end) tuple."""
    if "-" in range_str:
        parts = range_str.split("-")
        if len(parts) != 2:
            raise click.ClickException(f"Invalid range format: {range_str}")
        start, end = int(parts[0]), int(parts[1])
        return (start, end)
    else:
        page = int(range_str)
        return (page, page)


@click.group()
@click.version_option(version=__version__)
def cli():
    """PDF manipulation and Markdown conversion tool."""
    pass


@cli.command()
@click.argument("pdf", type=click.Path(exists=True))
def count(pdf: str):
    """Get the number of pages in a PDF."""
    try:
        pdf_tools = PDFTools()
        page_count = pdf_tools.get_page_count(pdf)
        click.echo(page_count)
    except Exception as e:
        raise click.ClickException(str(e))


@cli.command()
@click.argument("pdf", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
@click.argument("ranges", nargs=-1, required=True)
@click.option("-f", "--force", is_flag=True, help="Overwrite output file if it exists")
def extract(pdf: str, output: str, ranges: tuple[str, ...], force: bool):
    """Extract page ranges to a new PDF.

    RANGES can be single pages (5) or ranges (10-20).
    """
    try:
        parsed_ranges = [parse_page_range(r) for r in ranges]
        pdf_tools = PDFTools()
        output_path = pdf_tools.extract_page_ranges(
            pdf_path=pdf,
            output_path=output,
            ranges=parsed_ranges,
            overwrite=force,
        )
        click.echo(f"Extracted pages to: {output_path}")
    except FileExistsError as e:
        click.echo(f"Error: {e}", err=True)
        click.echo("Use --force to overwrite existing files", err=True)
        raise SystemExit(1)
    except Exception as e:
        raise click.ClickException(str(e))


@cli.command()
@click.argument("pdf", type=click.Path(exists=True))
@click.argument("ranges", nargs=-1, required=True)
@click.option("-o", "--output", type=click.Path(), help="Output file path")
@click.option("-f", "--force", is_flag=True, help="Overwrite output file if it exists")
def markdown(pdf: str, ranges: tuple[str, ...], output: str, force: bool):
    """Convert PDF page ranges to Markdown.

    RANGES can be single pages (5) or ranges (10-20).
    Output goes to stdout unless -o is specified.
    """
    try:
        parsed_ranges = [parse_page_range(r) for r in ranges]
        pdf_tools = PDFTools()
        markdown_content = pdf_tools.markdown_from_ranges(
            pdf_path=pdf,
            ranges=parsed_ranges,
        )

        if output:
            output_path = Path(output)
            if output_path.exists() and not force:
                click.echo(f"Error: {output_path} already exists", err=True)
                click.echo("Use --force to overwrite existing files", err=True)
                raise SystemExit(1)
            output_path.write_text(markdown_content)
            click.echo(f"Markdown written to: {output_path}")
        else:
            click.echo(markdown_content)
    except Exception as e:
        raise click.ClickException(str(e))


if __name__ == "__main__":
    cli()
