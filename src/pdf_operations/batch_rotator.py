"""
Batch PDF auto-rotation processor.

This module provides functionality for processing multiple PDFs,
detecting their orientation, and automatically rotating them.
"""

from pathlib import Path
from typing import List, Dict, Optional, Union, Callable
from dataclasses import dataclass
from datetime import datetime
import shutil

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

from .orientation_detector import OrientationDetector
from .rotation import RotationManager
from ..utils.logger import logger


@dataclass
class PageRotationTask:
    """Represents a single page rotation task"""
    pdf_path: Path
    page_number: int
    current_angle: int
    suggested_angle: int
    confidence: float
    auto_rotate: bool = False  # Whether this should be auto-rotated
    status: str = "pending"  # pending, rotated, skipped, error
    error_message: Optional[str] = None
    
    @property
    def needs_rotation(self) -> bool:
        """Check if this page needs rotation"""
        return self.suggested_angle != 0


@dataclass
class PDFRotationJob:
    """Represents a PDF file rotation job"""
    pdf_path: Path
    pages: List[PageRotationTask]
    status: str = "pending"  # pending, processing, completed, error
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    @property
    def total_pages(self) -> int:
        return len(self.pages)
    
    @property
    def pages_needing_rotation(self) -> int:
        return sum(1 for p in self.pages if p.needs_rotation)
    
    @property
    def high_confidence_pages(self) -> int:
        return sum(1 for p in self.pages if p.auto_rotate)


class BatchRotationProcessor:
    """
    Processes multiple PDFs for automatic rotation.
    
    Detects orientation, categorizes pages by confidence,
    and can automatically rotate high-confidence pages.
    """
    
    def __init__(
        self,
        confidence_threshold: float = 0.80,
        backup_originals: bool = True,
        output_suffix: str = "_rotated"
    ):
        """
        Initialize the batch processor.
        
        Args:
            confidence_threshold: Minimum confidence for auto-rotation (0-1)
            backup_originals: Whether to backup original files before rotation
            output_suffix: Suffix to add to output filenames
        """
        if not PYPDF2_AVAILABLE:
            raise ImportError(
                "PyPDF2 is required for batch rotation.\n"
                "Install it with: pip install -r requirements.txt"
            )
        
        self.detector = OrientationDetector(confidence_threshold)
        self.confidence_threshold = confidence_threshold
        self.backup_originals = backup_originals
        self.output_suffix = output_suffix
        self.jobs: List[PDFRotationJob] = []
        
        # Callback for progress updates
        self.progress_callback: Optional[Callable] = None
    
    def add_pdf(self, pdf_path: Union[str, Path]) -> PDFRotationJob:
        """
        Add a PDF to the processing queue.
        
        Args:
            pdf_path: Path to the PDF file
        
        Returns:
            PDFRotationJob object
        
        Raises:
            FileNotFoundError: If PDF file doesn't exist
        """
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        logger.info(f"Analyzing {pdf_path.name}...")
        
        # Detect orientation for all pages
        detection_results = self.detector.detect_pdf_orientation(pdf_path)
        
        # Create page tasks
        pages = []
        for page_num, result in enumerate(detection_results):
            task = PageRotationTask(
                pdf_path=pdf_path,
                page_number=page_num,
                current_angle=0,
                suggested_angle=result['angle'],
                confidence=result['confidence'],
                auto_rotate=self.detector.should_auto_rotate(result)
            )
            pages.append(task)
        
        job = PDFRotationJob(pdf_path=pdf_path, pages=pages)
        self.jobs.append(job)
        
        logger.info(
            f"Added {pdf_path.name}: {job.total_pages} pages, "
            f"{job.pages_needing_rotation} need rotation, "
            f"{job.high_confidence_pages} high confidence"
        )
        
        return job
    
    def add_multiple_pdfs(self, pdf_paths: List[Union[str, Path]]) -> List[PDFRotationJob]:
        """
        Add multiple PDFs to the processing queue.
        
        Args:
            pdf_paths: List of PDF file paths
        
        Returns:
            List of PDFRotationJob objects
        """
        jobs = []
        for pdf_path in pdf_paths:
            try:
                job = self.add_pdf(pdf_path)
                jobs.append(job)
            except Exception as e:
                logger.error(f"Error adding {pdf_path}: {e}")
        
        return jobs
    
    def add_directory(
        self,
        directory: Union[str, Path],
        recursive: bool = False,
        pattern: str = "*.pdf"
    ) -> List[PDFRotationJob]:
        """
        Add all PDFs from a directory to the processing queue.
        
        Args:
            directory: Directory path
            recursive: Whether to search recursively
            pattern: File pattern to match (default: *.pdf)
        
        Returns:
            List of PDFRotationJob objects
        """
        directory = Path(directory)
        if not directory.is_dir():
            raise ValueError(f"Not a directory: {directory}")
        
        # Find PDF files
        if recursive:
            pdf_files = list(directory.rglob(pattern))
        else:
            pdf_files = list(directory.glob(pattern))
        
        logger.info(f"Found {len(pdf_files)} PDF files in {directory}")
        
        return self.add_multiple_pdfs(pdf_files)
    
    def process_all(
        self,
        auto_rotate_high_confidence: bool = True,
        output_dir: Optional[Path] = None
    ) -> Dict[str, int]:
        """
        Process all PDFs in the queue.
        
        Args:
            auto_rotate_high_confidence: Automatically rotate high-confidence pages
            output_dir: Output directory (None = same as input)
        
        Returns:
            Summary statistics dictionary
        """
        total_files = len(self.jobs)
        total_pages = sum(job.total_pages for job in self.jobs)
        total_rotated = 0
        total_skipped = 0
        total_errors = 0
        
        logger.info(f"Processing {total_files} PDFs ({total_pages} total pages)...")
        
        for job_idx, job in enumerate(self.jobs):
            if self.progress_callback:
                self.progress_callback(job_idx, total_files, job)
            
            job.status = "processing"
            job.start_time = datetime.now()
            
            try:
                result = self._process_job(job, auto_rotate_high_confidence, output_dir)
                total_rotated += result['rotated']
                total_skipped += result['skipped']
                job.status = "completed"
            except Exception as e:
                logger.error(f"Error processing {job.pdf_path}: {e}")
                job.status = "error"
                total_errors += 1
            
            job.end_time = datetime.now()
        
        summary = {
            'total_files': total_files,
            'total_pages': total_pages,
            'pages_rotated': total_rotated,
            'pages_skipped': total_skipped,
            'errors': total_errors
        }
        
        logger.info(f"Batch processing complete: {summary}")
        
        return summary
    
    def _process_job(
        self,
        job: PDFRotationJob,
        auto_rotate: bool,
        output_dir: Optional[Path]
    ) -> Dict[str, int]:
        """Process a single PDF rotation job"""
        
        # Determine which pages to rotate
        if auto_rotate:
            pages_to_rotate = [
                task.page_number
                for task in job.pages
                if task.auto_rotate
            ]
        else:
            # Don't auto-rotate any pages
            pages_to_rotate = []
        
        if not pages_to_rotate:
            logger.info(f"No pages to auto-rotate in {job.pdf_path.name}")
            return {'rotated': 0, 'skipped': job.total_pages}
        
        # Backup original if requested
        if self.backup_originals:
            backup_path = job.pdf_path.with_suffix('.pdf.bak')
            shutil.copy2(job.pdf_path, backup_path)
            logger.debug(f"Backed up to {backup_path}")
        
        # Determine output path
        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / job.pdf_path.name
        else:
            # Add suffix to filename
            stem = job.pdf_path.stem
            output_path = job.pdf_path.with_name(f"{stem}{self.output_suffix}.pdf")
        
        # Read PDF
        reader = PyPDF2.PdfReader(str(job.pdf_path))
        writer = PyPDF2.PdfWriter()
        
        # Process each page
        rotated_count = 0
        for page_num, page in enumerate(reader.pages):
            task = job.pages[page_num]
            
            if page_num in pages_to_rotate:
                # Rotate this page
                angle = task.suggested_angle
                page.rotate(angle)
                task.status = "rotated"
                rotated_count += 1
                logger.debug(f"Rotated page {page_num + 1} by {angle}°")
            else:
                task.status = "skipped"
            
            writer.add_page(page)
        
        # Write output
        with open(output_path, 'wb') as f:
            writer.write(f)
        
        logger.info(f"Saved rotated PDF to {output_path}")
        
        return {
            'rotated': rotated_count,
            'skipped': job.total_pages - rotated_count
        }
    
    def get_summary(self) -> Dict:
        """
        Get a summary of all jobs in the queue.
        
        Returns:
            Summary statistics
        """
        return {
            'total_jobs': len(self.jobs),
            'total_pages': sum(job.total_pages for job in self.jobs),
            'pages_needing_rotation': sum(job.pages_needing_rotation for job in self.jobs),
            'high_confidence_pages': sum(job.high_confidence_pages for job in self.jobs),
            'jobs': [
                {
                    'file': job.pdf_path.name,
                    'pages': job.total_pages,
                    'needs_rotation': job.pages_needing_rotation,
                    'high_confidence': job.high_confidence_pages,
                    'status': job.status
                }
                for job in self.jobs
            ]
        }
    
    def print_summary(self):
        """Print a human-readable summary"""
        summary = self.get_summary()
        
        print("\n" + "="*60)
        print("Batch Rotation Summary")
        print("="*60)
        print(f"Total files: {summary['total_jobs']}")
        print(f"Total pages: {summary['total_pages']}")
        print(f"Pages needing rotation: {summary['pages_needing_rotation']}")
        print(f"High confidence pages: {summary['high_confidence_pages']}")
        print()
        
        print("Files:")
        for job_info in summary['jobs']:
            print(f"  {job_info['file']}: {job_info['pages']} pages, "
                  f"{job_info['needs_rotation']} need rotation, "
                  f"{job_info['high_confidence']} high confidence "
                  f"[{job_info['status']}]")
        print("="*60 + "\n")
