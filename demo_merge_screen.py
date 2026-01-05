#!/usr/bin/env python3
"""
Demo script for PDF Merge Screen

This script demonstrates the file selection, preview, and merge functionality.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.ui.merge_screen import show_merge_screen


def main():
    """Run the merge screen demo."""
    print("=" * 60)
    print("PDF Merge Screen Demo")
    print("=" * 60)
    print()
    print("This demo shows the merge interface with:")
    print("  - File browser for selecting PDFs")
    print("  - Thumbnail previews")
    print("  - Merge queue with drag-and-drop ordering")
    print("  - Full-page preview dialog")
    print("  - Merge execution")
    print()
    print("Instructions:")
    print("  1. Click 'Open Folder' to select a folder with PDFs")
    print("  2. Or click 'Add Files' to select individual PDFs")
    print("  3. Double-click files to add them to the merge queue")
    print("  4. Use arrow buttons to reorder files in the queue")
    print("  5. Click 'Merge PDFs' to merge (need 2+ files)")
    print()
    print("Starting GUI...")
    print()
    
    # Check dependencies
    try:
        from src.pdf_operations.preview import PDFPreviewGenerator
        from src.pdf_operations.merger import PDFMerger
        print("✓ All dependencies available")
    except ImportError as e:
        print("✗ Missing dependencies:")
        print(f"  {e}")
        print()
        print("Install with: pip install -r requirements.txt")
        return 1
    
    print()
    
    # Show the merge screen
    try:
        show_merge_screen()
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
        return 0
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
