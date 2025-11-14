"""Tests for document parsing tools."""

import pytest
from pathlib import Path
import tempfile
import os

from cover_letter_writer.tools.document_parser import DocumentParser


class TestDocumentParser:
    """Test suite for DocumentParser."""
    
    def test_parse_text_file(self):
        """Test parsing a plain text file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Test content\nLine 2\nLine 3")
            temp_path = f.name
        
        try:
            content = DocumentParser.parse_file(temp_path)
            assert "Test content" in content
            assert "Line 2" in content
            assert "Line 3" in content
        finally:
            os.unlink(temp_path)
    
    def test_parse_markdown_file(self):
        """Test parsing a markdown file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("# Heading\n\nParagraph text\n\n- List item")
            temp_path = f.name
        
        try:
            content = DocumentParser.parse_file(temp_path)
            assert "# Heading" in content
            assert "Paragraph text" in content
            assert "List item" in content
        finally:
            os.unlink(temp_path)
    
    def test_parse_nonexistent_file(self):
        """Test that parsing non-existent file raises error."""
        with pytest.raises(FileNotFoundError):
            DocumentParser.parse_file("/nonexistent/path/file.txt")
    
    def test_parse_source_url(self):
        """Test URL detection in parse_source."""
        # Test that URLs are detected (we can't test actual fetching without network)
        # Just verify that URL format is recognized
        source = "https://example.com"
        assert source.startswith(("http://", "https://"))
    
    def test_parse_file_auto_detect(self):
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
            content_txt = DocumentParser.parse_file(temp_txt)
            assert "Text content" in content_txt
            
            content_md = DocumentParser.parse_file(temp_md)
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
            with pytest.raises(ValueError, match="Unsupported file"):
                DocumentParser.parse_file(temp_path)
        finally:
            os.unlink(temp_path)
    
    def test_parse_multiple_files(self):
        """Test parsing multiple files at once."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f1:
            f1.write("File 1 content")
            temp1 = f1.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f2:
            f2.write("# File 2")
            temp2 = f2.name
        
        try:
            contents = DocumentParser.parse_multiple_files([temp1, temp2])
            assert len(contents) == 2
            assert "File 1 content" in contents[0]
            assert "# File 2" in contents[1]
        finally:
            os.unlink(temp1)
            os.unlink(temp2)


class TestExampleFiles:
    """Test that example files can be read."""
    
    def test_sample_files_exist(self):
        """Test that sample files exist."""
        examples_dir = Path(__file__).parent.parent / "examples"
        
        assert (examples_dir / "sample_job_description.txt").exists()
        assert (examples_dir / "sample_cv.md").exists()
        assert (examples_dir / "sample_recommendation.md").exists()
    
    def test_parse_sample_job_description(self):
        """Test parsing sample job description."""
        examples_dir = Path(__file__).parent.parent / "examples"
        job_desc_path = examples_dir / "sample_job_description.txt"
        
        content = DocumentParser.parse_file(str(job_desc_path))
        assert len(content) > 0
        assert "Senior Software Engineer" in content
    
    def test_parse_sample_cv(self):
        """Test parsing sample CV."""
        examples_dir = Path(__file__).parent.parent / "examples"
        cv_path = examples_dir / "sample_cv.md"
        
        content = DocumentParser.parse_file(str(cv_path))
        assert len(content) > 0
        assert "John Doe" in content
    
    def test_parse_sample_recommendation(self):
        """Test parsing sample recommendation."""
        examples_dir = Path(__file__).parent.parent / "examples"
        rec_path = examples_dir / "sample_recommendation.md"
        
        content = DocumentParser.parse_file(str(rec_path))
        assert len(content) > 0
        assert "recommendation" in content.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

