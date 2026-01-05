"""
PDF rotation functionality
"""

from pathlib import Path
from typing import List, Optional, Union

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

from ..utils.logger import logger


def _require_pypdf2():
    """Raise error if PyPDF2 is not available"""
    if not PYPDF2_AVAILABLE:
        raise ImportError(
            "PyPDF2 is required for PDF rotation.\n"
            "Install it with: pip install -r requirements.txt"
        )


class RotationManager:
    """Manages PDF rotation operations"""

    VALID_ANGLES = [0, 90, 180, 270]

    @staticmethod
    def rotate_page(
        page: "PyPDF2.PageObject", angle: int
    ) -> "PyPDF2.PageObject":
        """
        Rotate a PDF page.

        Args:
            page: PDF page object
            angle: Rotation angle (90, 180, or 270 degrees clockwise)

        Returns:
            Rotated page object

        Raises:
            ImportError: If PyPDF2 is not installed
            ValueError: If angle is not valid
        """
        _require_pypdf2()
        
        if angle not in RotationManager.VALID_ANGLES:
            raise ValueError(f"Invalid rotation angle: {angle}. Must be one of {RotationManager.VALID_ANGLES}")

        if angle == 0:
            return page

        # PyPDF2 rotates clockwise
        page.rotate(angle)
        return page

    @staticmethod
    def rotate_pdf(
        input_path: Union[str, Path],
        output_path: Union[str, Path],
        angle: int,
        pages: Optional[List[int]] = None,
    ) -> bool:
        """
        Rotate entire PDF or specific pages.

        Args:
            input_path: Input PDF file path
            output_path: Output PDF file path
            angle: Rotation angle (90, 180, or 270 degrees clockwise)
            pages: List of page numbers to rotate (0-indexed). If None, rotate all pages.

        Returns:
            True if successful, False otherwise
            
        Raises:
            ImportError: If PyPDF2 is not installed
        """
        _require_pypdf2()
        
        try:
            reader = PyPDF2.PdfReader(str(input_path))
            writer = PyPDF2.PdfWriter()

            for i, page in enumerate(reader.pages):
                # Rotate page if it's in the list or if rotating all pages
                if pages is None or i in pages:
                    page.rotate(angle)
                writer.add_page(page)

            # Write to output file
            with open(output_path, "wb") as output_file:
                writer.write(output_file)

            logger.info(f"Rotated PDF saved to {output_path}")
            return True

        except Exception as e:
            logger.error(f"Error rotating PDF: {e}")
            return False

    @staticmethod
    def auto_detect_orientation(page: "PyPDF2.PageObject") -> dict:
        """
        Detect page orientation using OCR.
        
        Note: This is a deprecated method. Use orientation_detector module instead.

        Args:
            page: PDF page object

        Returns:
            Dictionary with 'angle' (suggested rotation) and 'confidence' (0-1)
        """
        logger.warning(
            "auto_detect_orientation is deprecated. "
            "Use src.pdf_operations.orientation_detector module instead."
        )
        return {
            "angle": 0,
            "confidence": 0.0,
            "method": "deprecated"
        }


def rotate_left(page: "PyPDF2.PageObject") -> "PyPDF2.PageObject":
    """
    Rotate page 90 degrees counter-clockwise.

    Args:
        page: PDF page object

    Returns:
        Rotated page object
        
    Raises:
        ImportError: If PyPDF2 is not installed
    """
    return RotationManager.rotate_page(page, 270)


def rotate_right(page: "PyPDF2.PageObject") -> "PyPDF2.PageObject":
    """
    Rotate page 90 degrees clockwise.

    Args:
        page: PDF page object

    Returns:
        Rotated page object
        
    Raises:
        ImportError: If PyPDF2 is not installed
    """
    return RotationManager.rotate_page(page, 90)


def rotate_180(page: "PyPDF2.PageObject") -> "PyPDF2.PageObject":
    """
    Rotate page 180 degrees.

    Args:
        page: PDF page object

    Returns:
        Rotated page object
        
    Raises:
        ImportError: If PyPDF2 is not installed
    """
    return RotationManager.rotate_page(page, 180)
