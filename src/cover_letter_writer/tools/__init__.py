"""Tools package for Cover Letter Writer."""

from cover_letter_writer.tools.document_tools import (
    read_document,
    read_job_description,
    read_markdown_file,
    read_pdf_file,
    read_text_file,
    fetch_url_content,
    is_url,
)

__all__ = [
    "read_document",
    "read_job_description",
    "read_markdown_file",
    "read_pdf_file",
    "read_text_file",
    "fetch_url_content",
    "is_url",
]

