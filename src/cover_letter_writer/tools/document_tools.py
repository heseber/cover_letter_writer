"""Tools for reading and parsing various document formats."""

from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


def read_markdown_file(file_path: str) -> str:
    """
    Read and return the content of a Markdown file.

    Args:
        file_path: Path to the markdown file

    Returns:
        The text content of the markdown file

    Raises:
        FileNotFoundError: If the file doesn't exist
        IOError: If there's an error reading the file
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not path.is_file():
        raise IOError(f"Path is not a file: {file_path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        raise IOError(f"Error reading file {file_path}: {str(e)}")


def read_pdf_file(file_path: str) -> str:
    """
    Read and extract text content from a PDF file.

    Args:
        file_path: Path to the PDF file

    Returns:
        The extracted text content from the PDF

    Raises:
        FileNotFoundError: If the file doesn't exist
        IOError: If there's an error reading the file
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not path.is_file():
        raise IOError(f"Path is not a file: {file_path}")

    try:
        import pypdf

        with open(path, "rb") as f:
            pdf_reader = pypdf.PdfReader(f)
            text_content = []

            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    text_content.append(text)

            return "\n\n".join(text_content)
    except ImportError:
        raise ImportError(
            "pypdf is required to read PDF files. Install it with: pip install pypdf"
        )
    except Exception as e:
        raise IOError(f"Error reading PDF file {file_path}: {str(e)}")


def read_text_file(file_path: str) -> str:
    """
    Read and return the content of a plain text file.

    Args:
        file_path: Path to the text file

    Returns:
        The text content of the file

    Raises:
        FileNotFoundError: If the file doesn't exist
        IOError: If there's an error reading the file
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not path.is_file():
        raise IOError(f"Path is not a file: {file_path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        raise IOError(f"Error reading file {file_path}: {str(e)}")


def fetch_url_content(url: str, timeout: int = 30) -> str:
    """
    Fetch and extract text content from a URL.

    Args:
        url: The URL to fetch content from
        timeout: Request timeout in seconds (default: 30)

    Returns:
        The extracted text content from the URL

    Raises:
        ValueError: If the URL is invalid
        IOError: If there's an error fetching the content
    """
    # Validate URL
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: {url}")

    try:
        response = requests.get(
            url,
            timeout=timeout,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            },
        )
        response.raise_for_status()

        # Parse HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()

        # Get text content
        text = soup.get_text(separator="\n", strip=True)

        # Clean up whitespace
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return "\n".join(lines)

    except requests.RequestException as e:
        raise IOError(f"Error fetching URL {url}: {str(e)}")
    except Exception as e:
        raise IOError(f"Error processing content from {url}: {str(e)}")


def read_document(file_path: str) -> str:
    """
    Read a document and return its content, automatically detecting the file type.

    Supports: .txt, .md, .markdown, .pdf

    Args:
        file_path: Path to the document file

    Returns:
        The text content of the document

    Raises:
        ValueError: If the file type is not supported
        FileNotFoundError: If the file doesn't exist
        IOError: If there's an error reading the file
    """
    path = Path(file_path)
    extension = path.suffix.lower()

    if extension in [".txt", ".text"]:
        return read_text_file(file_path)
    elif extension in [".md", ".markdown"]:
        return read_markdown_file(file_path)
    elif extension == ".pdf":
        return read_pdf_file(file_path)
    else:
        raise ValueError(
            f"Unsupported file type: {extension}. "
            f"Supported types: .txt, .md, .markdown, .pdf"
        )


def is_url(string: str) -> bool:
    """
    Check if a string is a valid URL.

    Args:
        string: The string to check

    Returns:
        True if the string is a valid URL, False otherwise
    """
    try:
        result = urlparse(string)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def read_job_description(source: str) -> str:
    """
    Read job description from a file or URL.

    Args:
        source: File path or URL to the job description

    Returns:
        The text content of the job description

    Raises:
        ValueError: If the source is invalid
        FileNotFoundError: If the file doesn't exist
        IOError: If there's an error reading the content
    """
    if is_url(source):
        return fetch_url_content(source)
    else:
        return read_document(source)
