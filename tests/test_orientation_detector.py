"""
Tests for orientation detection module.
"""

import pytest
from pathlib import Path
import tempfile

# Import will fail if dependencies aren't installed
try:
    from src.pdf_operations.orientation_detector import (
        OrientationDetector,
        detect_orientation,
        batch_detect_orientation
    )
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False


# Skip all tests if dependencies aren't available
pytestmark = pytest.mark.skipif(
    not DEPENDENCIES_AVAILABLE,
    reason="OCR dependencies not installed"
)


class TestOrientationDetector:
    """Tests for the OrientationDetector class"""
    
    def test_detector_initialization(self):
        """Test detector can be initialized"""
        detector = OrientationDetector()
        assert detector.confidence_threshold == OrientationDetector.DEFAULT_CONFIDENCE_THRESHOLD
        
        # Test with custom threshold
        detector = OrientationDetector(confidence_threshold=0.9)
        assert detector.confidence_threshold == 0.9
    
    def test_should_auto_rotate_logic(self):
        """Test the auto-rotate decision logic"""
        detector = OrientationDetector(confidence_threshold=0.8)
        
        # High confidence, needs rotation
        result = {'angle': 90, 'confidence': 0.85}
        assert detector.should_auto_rotate(result) is True
        
        # High confidence, no rotation needed
        result = {'angle': 0, 'confidence': 0.85}
        assert detector.should_auto_rotate(result) is False
        
        # Low confidence, needs rotation
        result = {'angle': 90, 'confidence': 0.75}
        assert detector.should_auto_rotate(result) is False
        
        # Low confidence, no rotation
        result = {'angle': 0, 'confidence': 0.75}
        assert detector.should_auto_rotate(result) is False
    
    def test_rotation_summary(self):
        """Test rotation summary generation"""
        detector = OrientationDetector(confidence_threshold=0.8)
        
        results = [
            {'angle': 0, 'confidence': 0.9},    # No rotation needed
            {'angle': 90, 'confidence': 0.85},  # High confidence rotation
            {'angle': 180, 'confidence': 0.75}, # Low confidence rotation
            {'angle': 270, 'confidence': 0.9},  # High confidence rotation
            {'angle': 0, 'confidence': 0.5},    # No rotation needed
        ]
        
        summary = detector.get_rotation_summary(results)
        
        assert summary['total_pages'] == 5
        assert summary['needs_rotation'] == 3
        assert summary['high_confidence'] == 2
        assert summary['low_confidence'] == 1
        assert summary['pages_to_rotate'] == [1, 3]
    
    def test_orientation_to_rotation_mapping(self):
        """Test that orientation codes map to correct rotation angles"""
        # Verify the mapping
        assert OrientationDetector.ORIENTATION_TO_ROTATION[0] == 0
        assert OrientationDetector.ORIENTATION_TO_ROTATION[1] == 270
        assert OrientationDetector.ORIENTATION_TO_ROTATION[2] == 180
        assert OrientationDetector.ORIENTATION_TO_ROTATION[3] == 90
    
    def test_create_default_result(self):
        """Test fallback result creation"""
        result = OrientationDetector._create_default_result("test_error")
        
        assert result['angle'] == 0
        assert result['confidence'] == 0.0
        assert result['method'] == 'fallback'
        assert result['error'] == "test_error"
    
    def test_file_not_found_error(self):
        """Test that FileNotFoundError is raised for missing files"""
        detector = OrientationDetector()
        
        with pytest.raises(FileNotFoundError):
            detector.detect_page_orientation("nonexistent.pdf")
    
    def test_convenience_functions_exist(self):
        """Test that convenience functions are available"""
        # Just verify they exist and can be called
        # (actual functionality requires a PDF file)
        assert callable(detect_orientation)
        assert callable(batch_detect_orientation)


class TestOrientationDetectorIntegration:
    """Integration tests that require actual PDF files"""
    
    @pytest.fixture
    def sample_pdf_path(self):
        """
        Fixture to create a simple test PDF.
        
        Note: This is a placeholder. In a real test environment,
        you'd create an actual PDF with text for testing.
        """
        # For now, just return None - actual PDF creation would go here
        return None
    
    def test_detect_with_sample_pdf(self, sample_pdf_path):
        """Test detection with a sample PDF"""
        if sample_pdf_path is None:
            pytest.skip("Sample PDF not available")
        
        detector = OrientationDetector()
        result = detector.detect_page_orientation(sample_pdf_path, 0)
        
        # Verify result structure
        assert 'angle' in result
        assert 'confidence' in result
        assert 'method' in result
        assert result['angle'] in [0, 90, 180, 270]
        assert 0.0 <= result['confidence'] <= 1.0
