"""
PDF loading and validation functionality
"""

from pathlib import Path
from typing import Dict, List, Optional, Union

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False
    
from ..utils.logger import logger
from ..utils.validators import is_valid_pdf


def _require_pypdf2():
    """Raise error if PyPDF2 is not available"""
    if not PYPDF2_AVAILABLE:
        raise ImportError(
            "PyPDF2 is required for PDF operations.\n"
            "Install it with: pip install -r requirements.txt"
        )


class PDFDocument:
    """Represents a loaded PDF document"""

    def __init__(self, file_path: Union[str, Path]):
        """
        Initialize PDF document.

        Args:
            file_path: Path to PDF file

        Raises:
            ImportError: If PyPDF2 is not installed
            FileNotFoundError: If file doesn't exist
            ValueError: If file is not a valid PDF
        """
        _require_pypdf2()
        
        self.file_path = Path(file_path)

        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if not is_valid_pdf(self.file_path):
            raise ValueError(f"Invalid PDF file: {file_path}")

        self.reader: Optional[PyPDF2.PdfReader] = None
        self.metadata: Dict = {}
        self._load()

    def _load(self) -> None:
        """Load the PDF file."""
        try:
            with open(self.file_path, "rb") as f:
                self.reader = PyPDF2.PdfReader(f)
                self._extract_metadata()
            logger.info(f"Loaded PDF: {self.file_path}")
        except Exception as e:
            logger.error(f"Error loading PDF {self.file_path}: {e}")
            raise

    def _extract_metadata(self) -> None:
        """Extract metadata from PDF."""
        if self.reader and self.reader.metadata:
            self.metadata = {
                "title": self.reader.metadata.get("/Title", ""),
                "author": self.reader.metadata.get("/Author", ""),
                "subject": self.reader.metadata.get("/Subject", ""),
                "creator": self.reader.metadata.get("/Creator", ""),
                "producer": self.reader.metadata.get("/Producer", ""),
                "creation_date": self.reader.metadata.get("/CreationDate", ""),
            }

    @property
    def page_count(self) -> int:
        """Get the number of pages in the PDF."""
        if self.reader:
            return len(self.reader.pages)
        return 0

    @property
    def file_size(self) -> int:
        """Get file size in bytes."""
        return self.file_path.stat().st_size

    @property
    def file_name(self) -> str:
        """Get file name without extension."""
        return self.file_path.stem

    def get_page(self, page_num: int) -> Optional[PyPDF2.PageObject]:
        """
        Get a specific page from the PDF.

        Args:
            page_num: Page number (0-indexed)

        Returns:
            Page object or None if invalid page number
        """
        if self.reader and 0 <= page_num < self.page_count:
            return self.reader.pages[page_num]
        return None

    def get_page_dimensions(self, page_num: int) -> Optional[Dict[str, float]]:
        """
        Get dimensions of a specific page.

        Args:
            page_num: Page number (0-indexed)

        Returns:
            Dictionary with width and height, or None if invalid page
        """
        page = self.get_page(page_num)
        if page:
            box = page.mediabox
            return {
                "width": float(box.width),
                "height": float(box.height),
            }
        return None

    def __repr__(self) -> str:
        """String representation of PDF document."""
        return f"PDFDocument('{self.file_path}', pages={self.page_count})"


def load_pdf(file_path: Union[str, Path]) -> PDFDocument:
    """
    Load a PDF file.

    Args:
        file_path: Path to PDF file

    Returns:
        PDFDocument instance

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file is not a valid PDF
    """
    return PDFDocument(file_path)


def load_multiple_pdfs(file_paths: List[Union[str, Path]]) -> List[PDFDocument]:
    """
    Load multiple PDF files.

    Args:
        file_paths: List of paths to PDF files

    Returns:
        List of PDFDocument instances (skips invalid files)
    """
    documents = []
    for file_path in file_paths:
        try:
            doc = load_pdf(file_path)
            documents.append(doc)
        except (FileNotFoundError, ValueError) as e:
            logger.warning(f"Skipping {file_path}: {e}")
    return documents
