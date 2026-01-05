"""
PDF Preview Generation Module

This module handles the generation of thumbnail and full-size previews
for PDF pages. It includes caching for performance optimization.
"""

import os
from io import BytesIO
from pathlib import Path
from typing import Optional, Tuple, Dict
from PIL import Image
import logging

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

try:
    from pdf2image import convert_from_path
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False

logger = logging.getLogger(__name__)


class PreviewCache:
    """Simple in-memory cache for preview images."""
    
    def __init__(self, max_size: int = 50):
        """
        Initialize the preview cache.
        
        Args:
            max_size: Maximum number of previews to cache
        """
        self.cache: Dict[str, Image.Image] = {}
        self.max_size = max_size
        self.access_order: list = []
    
    def get(self, key: str) -> Optional[Image.Image]:
        """
        Get a cached preview.
        
        Args:
            key: Cache key (usually file_path:page_num:size)
            
        Returns:
            Cached image or None if not found
        """
        if key in self.cache:
            # Update access order (LRU)
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key]
        return None
    
    def put(self, key: str, image: Image.Image) -> None:
        """
        Add a preview to the cache.
        
        Args:
            key: Cache key
            image: Image to cache
        """
        if key in self.cache:
            # Update existing
            self.access_order.remove(key)
        elif len(self.cache) >= self.max_size:
            # Remove least recently used
            lru_key = self.access_order.pop(0)
            del self.cache[lru_key]
        
        self.cache[key] = image
        self.access_order.append(key)
    
    def clear(self) -> None:
        """Clear all cached previews."""
        self.cache.clear()
        self.access_order.clear()


class PDFPreviewGenerator:
    """Generates thumbnail and full-size previews for PDF pages."""
    
    def __init__(self, cache_size: int = 50):
        """
        Initialize the preview generator.
        
        Args:
            cache_size: Number of previews to cache
        """
        if not PYMUPDF_AVAILABLE and not PDF2IMAGE_AVAILABLE:
            raise ImportError(
                "Preview generation requires either PyMuPDF or pdf2image.\n"
                "Install with: pip install PyMuPDF pdf2image"
            )
        
        self.cache = PreviewCache(max_size=cache_size)
        self.prefer_pymupdf = PYMUPDF_AVAILABLE
    
    def generate_thumbnail(
        self,
        pdf_path: str,
        page_number: int = 0,
        max_size: Tuple[int, int] = (200, 200),
        use_cache: bool = True
    ) -> Optional[Image.Image]:
        """
        Generate a thumbnail preview of a PDF page.
        
        Args:
            pdf_path: Path to the PDF file
            page_number: Page number (0-indexed)
            max_size: Maximum thumbnail dimensions (width, height)
            use_cache: Whether to use cached thumbnails
            
        Returns:
            PIL Image object or None if generation fails
        """
        # Check cache
        cache_key = f"{pdf_path}:{page_number}:thumb:{max_size[0]}x{max_size[1]}"
        if use_cache:
            cached = self.cache.get(cache_key)
            if cached:
                return cached
        
        # Generate new thumbnail
        try:
            if self.prefer_pymupdf:
                image = self._generate_with_pymupdf(pdf_path, page_number, dpi=72)
            else:
                image = self._generate_with_pdf2image(pdf_path, page_number, dpi=72)
            
            if image:
                # Resize to thumbnail
                image.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Cache it
                if use_cache:
                    self.cache.put(cache_key, image)
                
                return image
        except Exception as e:
            logger.error(f"Failed to generate thumbnail for {pdf_path} page {page_number}: {e}")
            return None
    
    def generate_preview(
        self,
        pdf_path: str,
        page_number: int = 0,
        dpi: int = 150,
        use_cache: bool = True
    ) -> Optional[Image.Image]:
        """
        Generate a full-size preview of a PDF page.
        
        Args:
            pdf_path: Path to the PDF file
            page_number: Page number (0-indexed)
            dpi: Resolution for rendering
            use_cache: Whether to use cached previews
            
        Returns:
            PIL Image object or None if generation fails
        """
        # Check cache
        cache_key = f"{pdf_path}:{page_number}:preview:{dpi}"
        if use_cache:
            cached = self.cache.get(cache_key)
            if cached:
                return cached
        
        # Generate new preview
        try:
            if self.prefer_pymupdf:
                image = self._generate_with_pymupdf(pdf_path, page_number, dpi)
            else:
                image = self._generate_with_pdf2image(pdf_path, page_number, dpi)
            
            if image and use_cache:
                self.cache.put(cache_key, image)
            
            return image
        except Exception as e:
            logger.error(f"Failed to generate preview for {pdf_path} page {page_number}: {e}")
            return None
    
    def _generate_with_pymupdf(
        self,
        pdf_path: str,
        page_number: int,
        dpi: int = 150
    ) -> Optional[Image.Image]:
        """
        Generate preview using PyMuPDF (faster).
        
        Args:
            pdf_path: Path to the PDF file
            page_number: Page number (0-indexed)
            dpi: Resolution for rendering
            
        Returns:
            PIL Image object or None
        """
        if not PYMUPDF_AVAILABLE:
            return None
        
        try:
            doc = fitz.open(pdf_path)
            if page_number >= len(doc):
                logger.warning(f"Page {page_number} does not exist in {pdf_path}")
                doc.close()
                return None
            
            page = doc[page_number]
            
            # Calculate zoom factor from DPI
            zoom = dpi / 72  # 72 is the default DPI
            mat = fitz.Matrix(zoom, zoom)
            
            # Render page to pixmap
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to PIL Image
            img_data = pix.tobytes("ppm")
            image = Image.open(BytesIO(img_data))
            
            doc.close()
            return image
        except Exception as e:
            logger.error(f"PyMuPDF preview generation failed: {e}")
            return None
    
    def _generate_with_pdf2image(
        self,
        pdf_path: str,
        page_number: int,
        dpi: int = 150
    ) -> Optional[Image.Image]:
        """
        Generate preview using pdf2image (fallback).
        
        Args:
            pdf_path: Path to the PDF file
            page_number: Page number (0-indexed)
            dpi: Resolution for rendering
            
        Returns:
            PIL Image object or None
        """
        if not PDF2IMAGE_AVAILABLE:
            return None
        
        try:
            # pdf2image uses 1-indexed pages
            images = convert_from_path(
                pdf_path,
                dpi=dpi,
                first_page=page_number + 1,
                last_page=page_number + 1
            )
            
            if images:
                return images[0]
            return None
        except Exception as e:
            logger.error(f"pdf2image preview generation failed: {e}")
            return None
    
    def clear_cache(self) -> None:
        """Clear the preview cache."""
        self.cache.clear()
    
    def get_first_page_thumbnail(
        self,
        pdf_path: str,
        max_size: Tuple[int, int] = (200, 200)
    ) -> Optional[Image.Image]:
        """
        Convenience method to get first page thumbnail.
        
        Args:
            pdf_path: Path to the PDF file
            max_size: Maximum thumbnail dimensions
            
        Returns:
            PIL Image object or None
        """
        return self.generate_thumbnail(pdf_path, 0, max_size)


def create_blank_thumbnail(
    size: Tuple[int, int] = (200, 200),
    text: str = "No Preview"
) -> Image.Image:
    """
    Create a blank thumbnail with text.
    
    Args:
        size: Thumbnail dimensions
        text: Text to display
        
    Returns:
        PIL Image object
    """
    from PIL import ImageDraw, ImageFont
    
    # Create blank image
    image = Image.new('RGB', size, color='lightgray')
    draw = ImageDraw.Draw(image)
    
    # Try to use a nice font, fallback to default
    # Check common font paths across different platforms
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
        "/System/Library/Fonts/Helvetica.ttc",  # macOS
        "C:\\Windows\\Fonts\\arial.ttf",  # Windows
    ]
    
    font = None
    for font_path in font_paths:
        try:
            font = ImageFont.truetype(font_path, 16)
            break
        except:
            continue
    
    # Fallback to default font if none found
    if font is None:
        font = ImageFont.load_default()
    
    # Calculate text position (centered)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
    
    # Draw text
    draw.text(position, text, fill='black', font=font)
    
    return image
