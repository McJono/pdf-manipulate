"""
Integration tests for PDF Manipulate workflows

These tests verify that different components work together correctly
in end-to-end scenarios.
"""

import os
import tempfile
import shutil
from pathlib import Path
import pytest

# Skip all tests if PyPDF2 is not available
pytest.importorskip("PyPDF2")

from src.config.manager import ConfigManager
from src.naming.parser import TemplateParser
from src.pdf_operations.loader import PDFLoader
from src.pdf_operations.rotation import PDFRotator
from src.pdf_operations.merger import PDFMerger
from src.utils.validators import sanitize_filename


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests"""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    # Cleanup
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def sample_pdf_path(temp_dir):
    """Create a simple test PDF file"""
    try:
        from PyPDF2 import PdfWriter
        from PyPDF2.generic import RectangleObject
        
        pdf_path = os.path.join(temp_dir, "test_sample.pdf")
        writer = PdfWriter()
        
        # Add a simple blank page
        writer.add_blank_page(width=612, height=792)  # US Letter size
        
        with open(pdf_path, "wb") as f:
            writer.write(f)
        
        return pdf_path
    except Exception as e:
        pytest.skip(f"Could not create test PDF: {e}")


@pytest.fixture
def multiple_pdfs(temp_dir):
    """Create multiple test PDF files"""
    try:
        from PyPDF2 import PdfWriter
        
        pdf_paths = []
        for i in range(3):
            pdf_path = os.path.join(temp_dir, f"test_doc_{i+1}.pdf")
            writer = PdfWriter()
            
            # Add pages
            for _ in range(i + 1):  # Different number of pages for each PDF
                writer.add_blank_page(width=612, height=792)
            
            with open(pdf_path, "wb") as f:
                writer.write(f)
            
            pdf_paths.append(pdf_path)
        
        return pdf_paths
    except Exception as e:
        pytest.skip(f"Could not create test PDFs: {e}")


@pytest.mark.integration
class TestAutoRotationWorkflow:
    """Test the complete auto-rotation workflow"""
    
    def test_load_and_rotate_pdf(self, sample_pdf_path, temp_dir):
        """Test loading a PDF and rotating it"""
        # Load PDF
        loader = PDFLoader()
        metadata = loader.load(sample_pdf_path)
        
        assert metadata is not None
        assert metadata["page_count"] >= 1
        
        # Rotate PDF
        rotator = PDFRotator()
        output_path = os.path.join(temp_dir, "rotated_output.pdf")
        
        # Rotate first page by 90 degrees
        success = rotator.rotate_pdf(
            sample_pdf_path,
            output_path,
            {0: 90}  # Rotate page 0 by 90 degrees
        )
        
        assert success is True
        assert os.path.exists(output_path)
        
        # Verify the output
        rotated_metadata = loader.load(output_path)
        assert rotated_metadata["page_count"] == metadata["page_count"]
    
    def test_batch_rotation_workflow(self, multiple_pdfs, temp_dir):
        """Test batch rotation of multiple PDFs"""
        loader = PDFLoader()
        rotator = PDFRotator()
        
        output_dir = os.path.join(temp_dir, "rotated")
        os.makedirs(output_dir, exist_ok=True)
        
        # Process each PDF
        results = []
        for pdf_path in multiple_pdfs:
            metadata = loader.load(pdf_path)
            assert metadata is not None
            
            # Rotate all pages by 180 degrees
            output_path = os.path.join(
                output_dir,
                f"rotated_{os.path.basename(pdf_path)}"
            )
            
            rotations = {i: 180 for i in range(metadata["page_count"])}
            success = rotator.rotate_pdf(pdf_path, output_path, rotations)
            results.append(success)
        
        # All should succeed
        assert all(results)
        assert len(os.listdir(output_dir)) == len(multiple_pdfs)


@pytest.mark.integration
class TestMergeWorkflow:
    """Test the complete merge workflow"""
    
    def test_merge_multiple_pdfs(self, multiple_pdfs, temp_dir):
        """Test merging multiple PDFs end-to-end"""
        # Load PDFs and get metadata
        loader = PDFLoader()
        total_pages = 0
        
        for pdf_path in multiple_pdfs:
            metadata = loader.load(pdf_path)
            assert metadata is not None
            total_pages += metadata["page_count"]
        
        # Merge PDFs
        merger = PDFMerger()
        output_path = os.path.join(temp_dir, "merged_output.pdf")
        
        success = merger.merge(multiple_pdfs, output_path)
        assert success is True
        assert os.path.exists(output_path)
        
        # Verify merged PDF
        merged_metadata = loader.load(output_path)
        assert merged_metadata is not None
        assert merged_metadata["page_count"] == total_pages
    
    def test_merge_with_naming_template(self, multiple_pdfs, temp_dir):
        """Test merging with intelligent naming"""
        # Use naming template to generate output filename
        parser = TemplateParser()
        filename = parser.parse(
            "{date}_merged_{name}.pdf",
            user_variables={"name": "documents"}
        )
        
        # Ensure it's sanitized
        filename = sanitize_filename(filename)
        output_path = os.path.join(temp_dir, filename)
        
        # Merge
        merger = PDFMerger()
        success = merger.merge(multiple_pdfs, output_path)
        
        assert success is True
        assert os.path.exists(output_path)
        assert filename.endswith(".pdf")
        assert "merged_documents" in filename


@pytest.mark.integration
class TestNamingAndSavingWorkflow:
    """Test the naming and saving workflow"""
    
    def test_complete_naming_workflow(self, sample_pdf_path, temp_dir):
        """Test complete naming workflow with templates"""
        # Load configuration
        config = ConfigManager()
        
        # Get naming template from config
        templates = config.get("naming.templates", ["{date}_{name}"])
        assert len(templates) > 0
        
        # Parse template
        parser = TemplateParser()
        filename = parser.parse(
            templates[0],
            user_variables={"name": "test_document"}
        )
        
        # Sanitize
        filename = sanitize_filename(filename)
        
        # Ensure .pdf extension
        if not filename.lower().endswith(".pdf"):
            filename += ".pdf"
        
        output_path = os.path.join(temp_dir, filename)
        
        # Copy/save the file
        shutil.copy(sample_pdf_path, output_path)
        
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0
    
    def test_date_arithmetic_in_naming(self, sample_pdf_path, temp_dir):
        """Test date arithmetic in naming templates"""
        parser = TemplateParser()
        
        # Test with date offset
        filename = parser.parse(
            "{date+7}_invoice_{name}.pdf",
            user_variables={"name": "client_abc"}
        )
        
        filename = sanitize_filename(filename)
        output_path = os.path.join(temp_dir, filename)
        
        # Save file
        shutil.copy(sample_pdf_path, output_path)
        
        assert os.path.exists(output_path)
        assert "invoice_client_abc" in filename.lower()


@pytest.mark.integration
class TestErrorHandlingScenarios:
    """Test error handling in various scenarios"""
    
    def test_invalid_pdf_handling(self, temp_dir):
        """Test handling of invalid PDF files"""
        # Create a non-PDF file
        invalid_path = os.path.join(temp_dir, "not_a_pdf.pdf")
        with open(invalid_path, "w") as f:
            f.write("This is not a PDF file")
        
        # Try to load it
        loader = PDFLoader()
        metadata = loader.load(invalid_path)
        
        # Should return None or raise appropriate error
        assert metadata is None or "error" in str(metadata).lower()
    
    def test_missing_file_handling(self, temp_dir):
        """Test handling of missing files"""
        missing_path = os.path.join(temp_dir, "does_not_exist.pdf")
        
        loader = PDFLoader()
        metadata = loader.load(missing_path)
        
        # Should handle gracefully
        assert metadata is None
    
    def test_merge_with_nonexistent_file(self, sample_pdf_path, temp_dir):
        """Test merge with one nonexistent file"""
        merger = PDFMerger()
        
        missing_path = os.path.join(temp_dir, "missing.pdf")
        output_path = os.path.join(temp_dir, "output.pdf")
        
        # Try to merge existing and nonexistent files
        success = merger.merge(
            [sample_pdf_path, missing_path],
            output_path
        )
        
        # Should fail gracefully
        assert success is False or not os.path.exists(output_path)
    
    def test_invalid_rotation_angle(self, sample_pdf_path, temp_dir):
        """Test handling of invalid rotation angles"""
        rotator = PDFRotator()
        output_path = os.path.join(temp_dir, "rotated.pdf")
        
        # Try invalid angle (should be 0, 90, 180, or 270)
        # The rotator should either reject this or normalize it
        rotations = {0: 45}  # Invalid angle
        
        # This might succeed (if normalized) or fail gracefully
        result = rotator.rotate_pdf(sample_pdf_path, output_path, rotations)
        
        # Either way, it shouldn't crash
        assert isinstance(result, bool)
    
    def test_disk_space_validation(self, temp_dir):
        """Test that disk space is validated before operations"""
        from src.utils.validators import check_disk_space
        
        # Check that we can validate disk space
        has_space = check_disk_space(temp_dir, 1024)  # 1KB required
        
        # Should return a boolean
        assert isinstance(has_space, bool)
        # Temp dir should have at least 1KB available
        assert has_space is True


@pytest.mark.integration
class TestConfigurationIntegration:
    """Test configuration integration with workflows"""
    
    def test_config_driven_merge(self, multiple_pdfs, temp_dir):
        """Test merge using configuration settings"""
        config = ConfigManager()
        
        # Get merge settings
        preserve_bookmarks = config.get("merge.preserve_bookmarks", True)
        
        # Merge with config settings
        merger = PDFMerger()
        output_path = os.path.join(temp_dir, "config_merge.pdf")
        
        success = merger.merge(
            multiple_pdfs,
            output_path,
            preserve_bookmarks=preserve_bookmarks
        )
        
        assert success is True
        assert os.path.exists(output_path)
    
    def test_config_driven_naming(self, temp_dir):
        """Test naming using configuration templates"""
        config = ConfigManager()
        
        # Get default template from config
        default_template = config.get(
            "naming.default_template",
            "{date}_{name}"
        )
        
        # Use it to generate a filename
        parser = TemplateParser()
        filename = parser.parse(
            default_template,
            user_variables={"name": "test"}
        )
        
        assert filename is not None
        assert len(filename) > 0
