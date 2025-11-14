"""Tools for document processing."""

from cover_letter_writer.tools.document_parser import DocumentParser
from cover_letter_writer.tools.pdf_reader import PDFReaderTool, read_pdf
from cover_letter_writer.tools.web_scraper import WebScraperTool, scrape_web_page

__all__ = [
    "DocumentParser",
    "PDFReaderTool",
    "read_pdf",
    "WebScraperTool",
    "scrape_web_page",
]
