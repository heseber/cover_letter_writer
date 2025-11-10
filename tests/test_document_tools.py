"""Tests for document parsing tools."""

import pytest
from pathlib import Path
import tempfile
import os

from cover_letter_writer.tools.document_tools import (
    read_text_file,
    read_markdown_file,
    is_url,
    read_document,
)


class TestDocumentTools:
    """Test suite for document tools."""
    
    def test_read_text_file(self):
        """Test reading a plain text file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Test content\nLine 2\nLine 3")
            temp_path = f.name
        
        try:
            content = read_text_file(temp_path)
            assert "Test content" in content
            assert "Line 2" in content
            assert "Line 3" in content
        finally:
            os.unlink(temp_path)
    
    def test_read_markdown_file(self):
        """Test reading a markdown file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("# Heading\n\nParagraph text\n\n- List item")
            temp_path = f.name
        
        try:
            content = read_markdown_file(temp_path)
            assert "# Heading" in content
            assert "Paragraph text" in content
            assert "List item" in content
        finally:
            os.unlink(temp_path)
    
    def test_read_nonexistent_file(self):
        """Test that reading non-existent file raises error."""
        with pytest.raises(FileNotFoundError):
            read_text_file("/nonexistent/path/file.txt")
    
    def test_is_url(self):
        """Test URL detection."""
        assert is_url("https://example.com") is True
        assert is_url("http://example.com/path") is True
        assert is_url("/path/to/file.txt") is False
        assert is_url("file.txt") is False
        assert is_url("") is False
    
    def test_read_document_auto_detect(self):
        """Test automatic file type detection."""
        # Test with .txt file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Text content")
            temp_txt = f.name
        
        # Test with .md file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("# Markdown")
            temp_md = f.name
        
        try:
            content_txt = read_document(temp_txt)
            assert "Text content" in content_txt
            
            content_md = read_document(temp_md)
            assert "# Markdown" in content_md
        finally:
            os.unlink(temp_txt)
            os.unlink(temp_md)
    
    def test_unsupported_file_type(self):
        """Test that unsupported file types raise error."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xyz', delete=False) as f:
            f.write("Content")
            temp_path = f.name
        
        try:
            with pytest.raises(ValueError, match="Unsupported file type"):
                read_document(temp_path)
        finally:
            os.unlink(temp_path)


class TestExampleFiles:
    """Test that example files can be read."""
    
    def test_sample_files_exist(self):
        """Test that sample files exist."""
        examples_dir = Path(__file__).parent.parent / "examples"
        
        assert (examples_dir / "sample_job_description.txt").exists()
        assert (examples_dir / "sample_cv.md").exists()
        assert (examples_dir / "sample_recommendation.md").exists()
    
    def test_read_sample_job_description(self):
        """Test reading sample job description."""
        examples_dir = Path(__file__).parent.parent / "examples"
        job_desc_path = examples_dir / "sample_job_description.txt"
        
        content = read_document(str(job_desc_path))
        assert len(content) > 0
        assert "Senior Software Engineer" in content
    
    def test_read_sample_cv(self):
        """Test reading sample CV."""
        examples_dir = Path(__file__).parent.parent / "examples"
        cv_path = examples_dir / "sample_cv.md"
        
        content = read_document(str(cv_path))
        assert len(content) > 0
        assert "John Doe" in content
    
    def test_read_sample_recommendation(self):
        """Test reading sample recommendation."""
        examples_dir = Path(__file__).parent.parent / "examples"
        rec_path = examples_dir / "sample_recommendation.md"
        
        content = read_document(str(rec_path))
        assert len(content) > 0
        assert "recommendation" in content.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

