"""
PDF merging functionality
"""

from pathlib import Path
from typing import List, Union
import PyPDF2
from ..utils.logger import logger


class PDFMerger:
    """Manages PDF merging operations"""

    def __init__(self, preserve_metadata: bool = True, preserve_bookmarks: bool = True):
        """
        Initialize PDF merger.

        Args:
            preserve_metadata: Whether to preserve metadata from first PDF
            preserve_bookmarks: Whether to preserve bookmarks when merging
        """
        self.preserve_metadata = preserve_metadata
        self.preserve_bookmarks = preserve_bookmarks
        self.merger = PyPDF2.PdfMerger()

    def add_pdf(self, file_path: Union[str, Path], pages: Union[tuple, None] = None) -> None:
        """
        Add a PDF to the merge queue.

        Args:
            file_path: Path to PDF file
            pages: Optional tuple (start, end) for page range to include
        """
        try:
            if pages:
                self.merger.append(str(file_path), pages=pages)
            else:
                self.merger.append(str(file_path))
            logger.info(f"Added {file_path} to merge queue")
        except Exception as e:
            logger.error(f"Error adding {file_path} to merge: {e}")
            raise

    def merge(self, output_path: Union[str, Path]) -> bool:
        """
        Merge all PDFs in the queue and save to output file.

        Args:
            output_path: Path for the merged PDF

        Returns:
            True if successful, False otherwise
        """
        try:
            with open(output_path, "wb") as output_file:
                self.merger.write(output_file)
            logger.info(f"Merged PDF saved to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error merging PDFs: {e}")
            return False
        finally:
            self.merger.close()

    def reset(self) -> None:
        """Reset the merger, clearing all queued PDFs."""
        self.merger.close()
        self.merger = PyPDF2.PdfMerger()
        logger.info("Merger reset")


def merge_pdfs(
    input_files: List[Union[str, Path]],
    output_path: Union[str, Path],
    preserve_metadata: bool = True,
    preserve_bookmarks: bool = True,
) -> bool:
    """
    Merge multiple PDF files into one.

    Args:
        input_files: List of PDF file paths to merge
        output_path: Output file path for merged PDF
        preserve_metadata: Whether to preserve metadata
        preserve_bookmarks: Whether to preserve bookmarks

    Returns:
        True if successful, False otherwise
    """
    merger = PDFMerger(
        preserve_metadata=preserve_metadata,
        preserve_bookmarks=preserve_bookmarks
    )

    try:
        for file_path in input_files:
            merger.add_pdf(file_path)
        return merger.merge(output_path)
    except Exception as e:
        logger.error(f"Error in merge operation: {e}")
        return False


def merge_pdfs_with_order(
    files_in_order: List[Union[str, Path]],
    output_path: Union[str, Path]
) -> bool:
    """
    Merge PDFs in the specified order.

    Args:
        files_in_order: List of PDF paths in the order they should be merged
        output_path: Output file path

    Returns:
        True if successful, False otherwise
    """
    return merge_pdfs(files_in_order, output_path)
