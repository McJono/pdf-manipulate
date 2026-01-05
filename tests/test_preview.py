"""
Unit tests for PDF Preview module
"""

import pytest
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from PIL import Image

from src.pdf_operations.preview import (
    PreviewCache,
    PDFPreviewGenerator,
    create_blank_thumbnail
)


class TestPreviewCache:
    """Tests for PreviewCache class."""
    
    def test_cache_initialization(self):
        """Test cache is initialized correctly."""
        cache = PreviewCache(max_size=10)
        assert cache.max_size == 10
        assert len(cache.cache) == 0
        assert len(cache.access_order) == 0
    
    def test_put_and_get(self):
        """Test putting and getting items from cache."""
        cache = PreviewCache(max_size=5)
        
        # Create a test image
        image = Image.new('RGB', (100, 100), color='red')
        
        # Put in cache
        cache.put("test_key", image)
        
        # Get from cache
        retrieved = cache.get("test_key")
        assert retrieved is not None
        assert retrieved == image
    
    def test_get_nonexistent(self):
        """Test getting non-existent key returns None."""
        cache = PreviewCache()
        result = cache.get("nonexistent")
        assert result is None
    
    def test_lru_eviction(self):
        """Test least recently used item is evicted when cache is full."""
        cache = PreviewCache(max_size=3)
        
        img1 = Image.new('RGB', (10, 10), color='red')
        img2 = Image.new('RGB', (10, 10), color='green')
        img3 = Image.new('RGB', (10, 10), color='blue')
        img4 = Image.new('RGB', (10, 10), color='yellow')
        
        # Fill cache
        cache.put("key1", img1)
        cache.put("key2", img2)
        cache.put("key3", img3)
        
        # Access key1 to make it recently used
        cache.get("key1")
        
        # Add new item - key2 should be evicted (least recently used)
        cache.put("key4", img4)
        
        # Check
        assert cache.get("key1") is not None  # Still in cache
        assert cache.get("key2") is None       # Evicted
        assert cache.get("key3") is not None  # Still in cache
        assert cache.get("key4") is not None  # Newly added
    
    def test_update_existing_key(self):
        """Test updating an existing key."""
        cache = PreviewCache(max_size=3)
        
        img1 = Image.new('RGB', (10, 10), color='red')
        img2 = Image.new('RGB', (10, 10), color='green')
        
        cache.put("key1", img1)
        cache.put("key1", img2)  # Update
        
        # Should have only one entry
        assert len(cache.cache) == 1
        assert cache.get("key1") == img2
    
    def test_clear(self):
        """Test clearing the cache."""
        cache = PreviewCache()
        
        img = Image.new('RGB', (10, 10))
        cache.put("key1", img)
        cache.put("key2", img)
        
        cache.clear()
        
        assert len(cache.cache) == 0
        assert len(cache.access_order) == 0


class TestPDFPreviewGenerator:
    """Tests for PDFPreviewGenerator class."""
    
    @patch('src.pdf_operations.preview.PYMUPDF_AVAILABLE', False)
    @patch('src.pdf_operations.preview.PDF2IMAGE_AVAILABLE', False)
    def test_initialization_without_dependencies(self):
        """Test initialization fails without dependencies."""
        with pytest.raises(ImportError):
            PDFPreviewGenerator()
    
    @patch('src.pdf_operations.preview.PYMUPDF_AVAILABLE', True)
    def test_initialization_with_pymupdf(self):
        """Test initialization succeeds with PyMuPDF."""
        generator = PDFPreviewGenerator(cache_size=20)
        assert generator.cache.max_size == 20
        assert generator.prefer_pymupdf is True
    
    @patch('src.pdf_operations.preview.PYMUPDF_AVAILABLE', False)
    @patch('src.pdf_operations.preview.PDF2IMAGE_AVAILABLE', True)
    def test_initialization_with_pdf2image(self):
        """Test initialization succeeds with pdf2image."""
        generator = PDFPreviewGenerator()
        assert generator.prefer_pymupdf is False
    
    @patch('src.pdf_operations.preview.PYMUPDF_AVAILABLE', True)
    def test_cache_usage(self):
        """Test that cache is used for thumbnails."""
        generator = PDFPreviewGenerator()
        
        # Mock the _generate_with_pymupdf method
        mock_image = Image.new('RGB', (100, 100), color='blue')
        generator._generate_with_pymupdf = Mock(return_value=mock_image)
        
        # First call - should generate
        result1 = generator.generate_thumbnail("test.pdf", 0, use_cache=True)
        assert generator._generate_with_pymupdf.call_count == 1
        
        # Second call with same params - should use cache
        result2 = generator.generate_thumbnail("test.pdf", 0, use_cache=True)
        assert generator._generate_with_pymupdf.call_count == 1  # Not called again
        
        # Results should be the same (or at least similar)
        assert result1 is not None
        assert result2 is not None
    
    @patch('src.pdf_operations.preview.PYMUPDF_AVAILABLE', True)
    def test_cache_disabled(self):
        """Test generation without cache."""
        generator = PDFPreviewGenerator()
        
        mock_image = Image.new('RGB', (100, 100), color='blue')
        generator._generate_with_pymupdf = Mock(return_value=mock_image)
        
        # First call
        result1 = generator.generate_thumbnail("test.pdf", 0, use_cache=False)
        assert generator._generate_with_pymupdf.call_count == 1
        
        # Second call - should generate again (no cache)
        result2 = generator.generate_thumbnail("test.pdf", 0, use_cache=False)
        assert generator._generate_with_pymupdf.call_count == 2
    
    @patch('src.pdf_operations.preview.PYMUPDF_AVAILABLE', True)
    def test_thumbnail_resize(self):
        """Test that thumbnails are resized correctly."""
        generator = PDFPreviewGenerator()
        
        # Create a large mock image
        large_image = Image.new('RGB', (1000, 1000), color='red')
        generator._generate_with_pymupdf = Mock(return_value=large_image)
        
        # Generate thumbnail with max size
        result = generator.generate_thumbnail(
            "test.pdf", 0,
            max_size=(200, 200),
            use_cache=False
        )
        
        assert result is not None
        # Image should be resized to fit within max_size
        assert result.width <= 200
        assert result.height <= 200
    
    @patch('src.pdf_operations.preview.PYMUPDF_AVAILABLE', True)
    def test_clear_cache(self):
        """Test clearing the cache."""
        generator = PDFPreviewGenerator()
        
        mock_image = Image.new('RGB', (100, 100))
        generator._generate_with_pymupdf = Mock(return_value=mock_image)
        
        # Generate and cache
        generator.generate_thumbnail("test.pdf", 0, use_cache=True)
        assert len(generator.cache.cache) > 0
        
        # Clear
        generator.clear_cache()
        assert len(generator.cache.cache) == 0
    
    @patch('src.pdf_operations.preview.PYMUPDF_AVAILABLE', True)
    def test_get_first_page_thumbnail(self):
        """Test convenience method for first page."""
        generator = PDFPreviewGenerator()
        
        mock_image = Image.new('RGB', (100, 100))
        generator.generate_thumbnail = Mock(return_value=mock_image)
        
        result = generator.get_first_page_thumbnail("test.pdf")
        
        # Should call generate_thumbnail with page 0
        generator.generate_thumbnail.assert_called_once()
        args = generator.generate_thumbnail.call_args
        assert args[0][1] == 0  # page_number should be 0


class TestCreateBlankThumbnail:
    """Tests for create_blank_thumbnail function."""
    
    def test_creates_image(self):
        """Test that a blank thumbnail is created."""
        image = create_blank_thumbnail()
        assert image is not None
        assert isinstance(image, Image.Image)
    
    def test_correct_size(self):
        """Test that thumbnail has correct size."""
        size = (300, 400)
        image = create_blank_thumbnail(size=size)
        assert image.size == size
    
    def test_with_custom_text(self):
        """Test creating thumbnail with custom text."""
        image = create_blank_thumbnail(text="Test Text")
        assert image is not None
        # Can't easily test if text is rendered, but at least it doesn't crash
    
    def test_default_size(self):
        """Test default size is used when not specified."""
        image = create_blank_thumbnail()
        assert image.size == (200, 200)
