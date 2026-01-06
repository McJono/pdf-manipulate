"""
Tests for validator utilities
"""

import pytest
from pathlib import Path
from src.utils.validators import sanitize_filename, is_valid_pdf, ensure_extension


class TestSanitizeFilename:
    """Test cases for sanitize_filename"""

    def test_simple_filename(self):
        """Test simple valid filename"""
        result = sanitize_filename("document.pdf")
        assert result == "document.pdf"

    def test_invalid_characters(self):
        """Test removal of invalid characters"""
        result = sanitize_filename("test/file:name*.pdf")
        assert "/" not in result
        assert ":" not in result
        assert "*" not in result

    def test_windows_invalid_chars(self):
        """Test removal of Windows invalid characters"""
        result = sanitize_filename('file<name>with|"invalid?.pdf')
        assert "<" not in result
        assert ">" not in result
        assert "|" not in result
        assert '"' not in result
        assert "?" not in result

    def test_multiple_spaces(self):
        """Test multiple spaces are replaced"""
        result = sanitize_filename("test    file.pdf")
        assert "    " not in result
        assert result == "test file.pdf"

    def test_whitespace_trim(self):
        """Test whitespace trimming"""
        result = sanitize_filename("  test.pdf  ")
        assert result == "test.pdf"

    def test_empty_filename(self):
        """Test empty filename gets default name"""
        result = sanitize_filename("")
        assert result == "unnamed"

    def test_max_length(self):
        """Test filename truncation"""
        long_name = "a" * 300 + ".pdf"
        result = sanitize_filename(long_name, max_length=255)
        assert len(result) <= 255
        assert result.endswith(".pdf")

    def test_preserve_extension(self):
        """Test extension is preserved when truncating"""
        long_name = "a" * 300 + ".pdf"
        result = sanitize_filename(long_name)
        assert result.endswith(".pdf")


class TestIsValidPDF:
    """Test cases for is_valid_pdf"""

    def test_nonexistent_file(self):
        """Test nonexistent file returns False"""
        assert not is_valid_pdf("/nonexistent/file.pdf")

    def test_wrong_extension(self):
        """Test file with wrong extension returns False"""
        # Create a temporary text file
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            path = Path(f.name)

        try:
            assert not is_valid_pdf(path)
        finally:
            path.unlink()

    def test_pdf_extension_but_invalid_content(self):
        """Test file with .pdf extension but invalid content"""
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            f.write(b"Not a PDF file")
            path = Path(f.name)

        try:
            assert not is_valid_pdf(path)
        finally:
            path.unlink()


class TestEnsureExtension:
    """Test cases for ensure_extension"""

    def test_adds_extension_when_missing(self):
        """Test adding extension to filename without one"""
        result = ensure_extension("document", ".pdf")
        assert result == "document.pdf"

    def test_preserves_existing_extension(self):
        """Test preserving existing extension"""
        result = ensure_extension("document.pdf", ".pdf")
        assert result == "document.pdf"

    def test_case_insensitive_check(self):
        """Test case-insensitive extension check"""
        result = ensure_extension("document.PDF", ".pdf")
        assert result == "document.PDF"  # Preserves original case

    def test_extension_without_dot(self):
        """Test handling extension without leading dot"""
        result = ensure_extension("document", "pdf")
        assert result == "document.pdf"

    def test_different_extensions(self):
        """Test with non-PDF extensions"""
        result = ensure_extension("image", ".jpg")
        assert result == "image.jpg"

    def test_multiple_dots_in_filename(self):
        """Test filename with multiple dots"""
        result = ensure_extension("my.document.backup", ".pdf")
        assert result == "my.document.backup.pdf"

    def test_empty_filename(self):
        """Test empty filename"""
        result = ensure_extension("", ".pdf")
        assert result == ".pdf"
