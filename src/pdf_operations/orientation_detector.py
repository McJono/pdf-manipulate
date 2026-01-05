"""
OCR-based PDF orientation detection module.

This module uses Tesseract OCR to detect the orientation of PDF pages
and suggest the correct rotation angle.
"""

import io
from pathlib import Path
from typing import Dict, List, Optional, Union
import tempfile

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

try:
    from pdf2image import convert_from_path
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import pytesseract
    PYTESSERACT_AVAILABLE = True
except ImportError:
    PYTESSERACT_AVAILABLE = False

from ..utils.logger import logger


def _require_ocr_dependencies():
    """Raise error if required OCR dependencies are not available"""
    missing = []
    if not PYPDF2_AVAILABLE:
        missing.append("PyPDF2")
    if not PDF2IMAGE_AVAILABLE:
        missing.append("pdf2image")
    if not PIL_AVAILABLE:
        missing.append("Pillow")
    if not PYTESSERACT_AVAILABLE:
        missing.append("pytesseract")
    
    if missing:
        raise ImportError(
            f"Missing required dependencies for OCR: {', '.join(missing)}\n"
            "Install them with: pip install -r requirements.txt\n"
            "Also ensure tesseract-ocr is installed on your system:\n"
            "  Ubuntu/Debian: sudo apt-get install tesseract-ocr\n"
            "  macOS: brew install tesseract\n"
            "  Windows: download from https://github.com/UB-Mannheim/tesseract/wiki"
        )


class OrientationDetector:
    """
    Detects the orientation of PDF pages using OCR.
    
    Uses Tesseract OCR to analyze text orientation and suggest
    the correct rotation angle for misoriented pages.
    """
    
    # Confidence threshold for automatic rotation
    DEFAULT_CONFIDENCE_THRESHOLD = 0.80
    
    # Mapping from Tesseract orientation codes to rotation angles
    # Tesseract returns: 0=0°, 1=90°, 2=180°, 3=270° (clockwise)
    # We need to rotate counter-clockwise, so we invert
    ORIENTATION_TO_ROTATION = {
        0: 0,    # Already correct
        1: 270,  # Rotate 270° clockwise = 90° counter-clockwise
        2: 180,  # Rotate 180°
        3: 90,   # Rotate 90° clockwise = 270° counter-clockwise
    }
    
    def __init__(self, confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD):
        """
        Initialize the orientation detector.
        
        Args:
            confidence_threshold: Minimum confidence (0-1) for automatic rotation
        """
        _require_ocr_dependencies()
        self.confidence_threshold = confidence_threshold
    
    def detect_page_orientation(
        self,
        pdf_path: Union[str, Path],
        page_number: int = 0,
        dpi: int = 150
    ) -> Dict[str, Union[int, float, str]]:
        """
        Detect the orientation of a specific PDF page.
        
        Args:
            pdf_path: Path to the PDF file
            page_number: Page number to analyze (0-indexed)
            dpi: DPI for rendering the page (higher = more accurate but slower)
        
        Returns:
            Dictionary with:
                - angle: Suggested rotation angle (0, 90, 180, 270)
                - confidence: Confidence score (0-1)
                - method: Detection method used
                - orientation: Tesseract orientation code
                - script_confidence: Tesseract script detection confidence
        
        Raises:
            ImportError: If required dependencies are not installed
            FileNotFoundError: If PDF file doesn't exist
            ValueError: If page number is invalid
        """
        _require_ocr_dependencies()
        
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        try:
            # Convert PDF page to image
            logger.debug(f"Converting page {page_number} to image at {dpi} DPI")
            images = convert_from_path(
                str(pdf_path),
                dpi=dpi,
                first_page=page_number + 1,
                last_page=page_number + 1
            )
            
            if not images:
                logger.warning(f"No image generated for page {page_number}")
                return self._create_default_result("no_image")
            
            image = images[0]
            
            # Run OCR orientation detection
            logger.debug(f"Running OCR orientation detection on page {page_number}")
            osd = pytesseract.image_to_osd(image, output_type=pytesseract.Output.DICT)
            
            # Extract orientation information
            # Tesseract returns:
            # - orientation: detected orientation (0, 90, 180, 270)
            # - rotate: degrees to rotate clockwise to fix orientation
            # - orientation_conf: confidence in orientation detection
            orientation = osd.get('orientation', 0)
            orientation_confidence = osd.get('orientation_conf', 0.0) / 100.0  # Convert to 0-1
            rotate = osd.get('rotate', 0)
            script = osd.get('script', 'Unknown')
            script_confidence = osd.get('script_conf', 0.0) / 100.0
            
            # Use the 'rotate' value directly - it's what we need to apply
            # to fix the orientation (clockwise degrees)
            angle = rotate
            
            logger.info(
                f"Page {page_number}: detected orientation={orientation}, "
                f"rotate={rotate}, angle={angle}, confidence={orientation_confidence:.2%}"
            )
            
            return {
                'angle': angle,
                'confidence': orientation_confidence,
                'method': 'tesseract_osd',
                'orientation': orientation,
                'rotate_suggestion': rotate,
                'script': script,
                'script_confidence': script_confidence
            }
            
        except pytesseract.TesseractError as e:
            logger.error(f"Tesseract error on page {page_number}: {e}")
            return self._create_default_result(f"tesseract_error: {e}")
        
        except Exception as e:
            logger.error(f"Error detecting orientation for page {page_number}: {e}")
            return self._create_default_result(f"error: {e}")
    
    def detect_pdf_orientation(
        self,
        pdf_path: Union[str, Path],
        dpi: int = 150,
        max_pages: Optional[int] = None
    ) -> List[Dict[str, Union[int, float, str]]]:
        """
        Detect orientation for all pages in a PDF.
        
        Args:
            pdf_path: Path to the PDF file
            dpi: DPI for rendering pages
            max_pages: Maximum number of pages to process (None = all pages)
        
        Returns:
            List of orientation detection results, one per page
        
        Raises:
            ImportError: If required dependencies are not installed
            FileNotFoundError: If PDF file doesn't exist
        """
        _require_ocr_dependencies()
        
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        # Get page count
        try:
            reader = PyPDF2.PdfReader(str(pdf_path))
            total_pages = len(reader.pages)
        except Exception as e:
            logger.error(f"Error reading PDF {pdf_path}: {e}")
            return []
        
        # Limit pages if requested
        pages_to_process = min(total_pages, max_pages) if max_pages else total_pages
        
        logger.info(f"Detecting orientation for {pages_to_process} pages in {pdf_path.name}")
        
        results = []
        for page_num in range(pages_to_process):
            logger.debug(f"Processing page {page_num + 1}/{pages_to_process}")
            result = self.detect_page_orientation(pdf_path, page_num, dpi)
            results.append(result)
        
        return results
    
    def should_auto_rotate(self, detection_result: Dict) -> bool:
        """
        Determine if a page should be automatically rotated based on detection.
        
        Args:
            detection_result: Result from detect_page_orientation()
        
        Returns:
            True if the page should be rotated automatically
        """
        angle = detection_result.get('angle', 0)
        confidence = detection_result.get('confidence', 0.0)
        
        # Only rotate if:
        # 1. Rotation is needed (angle != 0)
        # 2. Confidence is above threshold
        return angle != 0 and confidence >= self.confidence_threshold
    
    def get_rotation_summary(self, results: List[Dict]) -> Dict[str, Union[int, List[int]]]:
        """
        Generate a summary of rotation suggestions.
        
        Args:
            results: List of detection results from detect_pdf_orientation()
        
        Returns:
            Dictionary with:
                - total_pages: Total number of pages analyzed
                - needs_rotation: Number of pages that need rotation
                - high_confidence: Number of pages with high confidence
                - low_confidence: Number of pages with low confidence
                - pages_to_rotate: List of page numbers that should be rotated
        """
        total_pages = len(results)
        needs_rotation = sum(1 for r in results if r.get('angle', 0) != 0)
        high_confidence = sum(1 for r in results if self.should_auto_rotate(r))
        low_confidence = needs_rotation - high_confidence
        
        pages_to_rotate = [
            i for i, r in enumerate(results)
            if self.should_auto_rotate(r)
        ]
        
        return {
            'total_pages': total_pages,
            'needs_rotation': needs_rotation,
            'high_confidence': high_confidence,
            'low_confidence': low_confidence,
            'pages_to_rotate': pages_to_rotate
        }
    
    @staticmethod
    def _create_default_result(reason: str) -> Dict:
        """
        Create a default result when detection fails.
        
        Args:
            reason: Reason for failure
        
        Returns:
            Default detection result
        """
        return {
            'angle': 0,
            'confidence': 0.0,
            'method': 'fallback',
            'error': reason
        }


def detect_orientation(
    pdf_path: Union[str, Path],
    page_number: int = 0,
    confidence_threshold: float = OrientationDetector.DEFAULT_CONFIDENCE_THRESHOLD
) -> Dict:
    """
    Convenience function to detect orientation of a single page.
    
    Args:
        pdf_path: Path to the PDF file
        page_number: Page number to analyze (0-indexed)
        confidence_threshold: Minimum confidence for automatic rotation
    
    Returns:
        Orientation detection result
    """
    detector = OrientationDetector(confidence_threshold)
    return detector.detect_page_orientation(pdf_path, page_number)


def batch_detect_orientation(
    pdf_path: Union[str, Path],
    confidence_threshold: float = OrientationDetector.DEFAULT_CONFIDENCE_THRESHOLD,
    max_pages: Optional[int] = None
) -> List[Dict]:
    """
    Convenience function to detect orientation for all pages in a PDF.
    
    Args:
        pdf_path: Path to the PDF file
        confidence_threshold: Minimum confidence for automatic rotation
        max_pages: Maximum number of pages to process
    
    Returns:
        List of orientation detection results
    """
    detector = OrientationDetector(confidence_threshold)
    return detector.detect_pdf_orientation(pdf_path, max_pages=max_pages)
