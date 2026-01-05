#!/usr/bin/env python3
"""
Demo script for testing orientation detection.

Creates a sample PDF and tests orientation detection on it.
"""

from pathlib import Path
import sys

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

try:
    import PyPDF2
    from src.pdf_operations.orientation_detector import OrientationDetector
    from src.pdf_operations.rotation import RotationManager
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"Error: {e}")
    DEPENDENCIES_AVAILABLE = False
    sys.exit(1)


def create_sample_pdf(output_path: Path):
    """Create a simple PDF with text for testing"""
    if not REPORTLAB_AVAILABLE:
        print("reportlab not installed. Install with: pip install reportlab")
        return False
    
    c = canvas.Canvas(str(output_path), pagesize=letter)
    width, height = letter
    
    # Page 1: Normal orientation
    c.setFont("Helvetica", 24)
    c.drawString(100, height - 100, "Page 1: Normal Orientation")
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 150, "This text should be readable without rotation.")
    c.drawString(100, height - 180, "Lorem ipsum dolor sit amet, consectetur adipiscing elit.")
    c.showPage()
    
    # Page 2: Some more text
    c.setFont("Helvetica", 24)
    c.drawString(100, height - 100, "Page 2: Also Normal")
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 150, "More readable text on the second page.")
    c.drawString(100, height - 180, "Sed do eiusmod tempor incididunt ut labore.")
    c.showPage()
    
    c.save()
    print(f"✓ Created sample PDF: {output_path}")
    return True


def create_rotated_pdf(input_path: Path, output_path: Path):
    """Create a version of the PDF with rotated pages"""
    reader = PyPDF2.PdfReader(str(input_path))
    writer = PyPDF2.PdfWriter()
    
    # Rotate first page 90 degrees
    page1 = reader.pages[0]
    page1.rotate(90)
    writer.add_page(page1)
    
    # Rotate second page 180 degrees
    if len(reader.pages) > 1:
        page2 = reader.pages[1]
        page2.rotate(180)
        writer.add_page(page2)
    
    with open(output_path, 'wb') as f:
        writer.write(f)
    
    print(f"✓ Created rotated PDF: {output_path}")


def test_orientation_detection(pdf_path: Path):
    """Test orientation detection on a PDF"""
    print(f"\n{'='*60}")
    print(f"Testing Orientation Detection: {pdf_path.name}")
    print(f"{'='*60}\n")
    
    detector = OrientationDetector(confidence_threshold=0.75)
    results = detector.detect_pdf_orientation(pdf_path)
    
    print(f"Analyzed {len(results)} pages:\n")
    
    for i, result in enumerate(results):
        print(f"Page {i + 1}:")
        print(f"  Suggested rotation: {result['angle']}°")
        print(f"  Confidence: {result['confidence']:.2%}")
        print(f"  Method: {result['method']}")
        
        if 'script' in result:
            print(f"  Script: {result['script']} ({result['script_confidence']:.2%})")
        
        if 'error' in result:
            print(f"  Error: {result['error']}")
        
        should_rotate = detector.should_auto_rotate(result)
        print(f"  Auto-rotate: {'✓ YES' if should_rotate else '✗ NO'}")
        print()
    
    # Print summary
    summary = detector.get_rotation_summary(results)
    print(f"Summary:")
    print(f"  Total pages: {summary['total_pages']}")
    print(f"  Need rotation: {summary['needs_rotation']}")
    print(f"  High confidence: {summary['high_confidence']}")
    print(f"  Low confidence: {summary['low_confidence']}")
    print(f"  Pages to auto-rotate: {[p+1 for p in summary['pages_to_rotate']]}")


def main():
    """Main demo function"""
    print("PDF Orientation Detection Demo")
    print("=" * 60)
    
    # Create test directory
    test_dir = Path("/tmp/pdf_orientation_test")
    test_dir.mkdir(exist_ok=True)
    
    normal_pdf = test_dir / "sample_normal.pdf"
    rotated_pdf = test_dir / "sample_rotated.pdf"
    
    # Create sample PDFs
    if not normal_pdf.exists():
        if not create_sample_pdf(normal_pdf):
            print("\nSkipping PDF creation (reportlab not available)")
            print("You can manually place a PDF in /tmp/pdf_orientation_test/test.pdf")
            return
    
    if not rotated_pdf.exists():
        create_rotated_pdf(normal_pdf, rotated_pdf)
    
    # Test normal PDF
    test_orientation_detection(normal_pdf)
    
    # Test rotated PDF
    test_orientation_detection(rotated_pdf)
    
    print(f"\n{'='*60}")
    print("Demo complete!")
    print(f"Test files are in: {test_dir}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
