"""
Tests for naming template parser
"""

import pytest
from src.naming.parser import TemplateParser, parse_template
from datetime import datetime, timedelta


class TestTemplateParser:
    """Test cases for TemplateParser"""

    def test_simple_template(self):
        """Test simple template without variables"""
        parser = TemplateParser()
        result = parser.parse("document.pdf")
        assert result == "document.pdf"

    def test_name_variable(self):
        """Test {name} variable substitution"""
        parser = TemplateParser()
        result = parser.parse("{name}.pdf", user_variables={"name": "test"})
        assert result == "test.pdf"

    def test_filename_variable(self):
        """Test {filename} variable substitution"""
        parser = TemplateParser()
        result = parser.parse("{filename}_processed.pdf", filename="original")
        assert result == "original_processed.pdf"

    def test_date_variable(self):
        """Test {date} variable"""
        parser = TemplateParser()
        result = parser.parse("{date}_document.pdf")
        today = datetime.now().strftime("%Y-%m-%d")
        assert result == f"{today}_document.pdf"

    def test_date_with_offset(self):
        """Test {date+N} and {date-N}"""
        parser = TemplateParser()

        # Test positive offset
        result = parser.parse("{date+7}_document.pdf")
        future_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        assert result == f"{future_date}_document.pdf"

        # Test negative offset
        result = parser.parse("{date-30}_document.pdf")
        past_date = (datetime.now() + timedelta(days=-30)).strftime("%Y-%m-%d")
        assert result == f"{past_date}_document.pdf"

    def test_counter(self):
        """Test {counter} variable"""
        parser = TemplateParser()
        result = parser.parse("document_{counter}.pdf")
        assert result == "document_000.pdf"

        parser.increment_counter()
        result = parser.parse("document_{counter}.pdf")
        assert result == "document_001.pdf"

    def test_counter_with_padding(self):
        """Test {counter:N} with custom padding"""
        parser = TemplateParser()
        result = parser.parse("document_{counter:5}.pdf")
        assert result == "document_00000.pdf"

    def test_timestamp(self):
        """Test {timestamp} variable"""
        parser = TemplateParser()
        result = parser.parse("{timestamp}_document.pdf")
        # Just check it contains expected format parts
        assert "_document.pdf" in result
        assert len(result) > len("_document.pdf")

    def test_complex_template(self):
        """Test template with multiple variables"""
        parser = TemplateParser()
        result = parser.parse(
            "Invoice_{date}_{name}.pdf",
            user_variables={"name": "AcmeCorp"}
        )
        today = datetime.now().strftime("%Y-%m-%d")
        assert result == f"Invoice_{today}_AcmeCorp.pdf"

    def test_sanitization(self):
        """Test filename sanitization"""
        parser = TemplateParser()
        result = parser.parse(
            "{name}.pdf",
            user_variables={"name": "test/file:name*"}
        )
        assert "/" not in result
        assert ":" not in result
        assert "*" not in result

    def test_validate_template(self):
        """Test template validation"""
        parser = TemplateParser()

        # Valid templates
        assert parser.validate_template("{date}_{name}.pdf")
        assert parser.validate_template("{counter:3}_{filename}.pdf")

        # Invalid template (unbalanced braces)
        assert not parser.validate_template("{date_{name}.pdf")

    def test_parse_template_convenience(self):
        """Test convenience function"""
        result = parse_template(
            "{date}_{name}.pdf",
            name="test"
        )
        today = datetime.now().strftime("%Y-%m-%d")
        assert result == f"{today}_test.pdf"
