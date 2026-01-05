#!/usr/bin/env python3
"""
Demo script for batch PDF auto-rotation.

Creates sample PDFs and demonstrates the batch rotation processor.
"""

from pathlib import Path
import sys

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("Warning: reportlab not installed, will skip PDF generation")

try:
    import PyPDF2
    from src.pdf_operations.batch_rotator import BatchRotationProcessor
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"Error: {e}")
    DEPENDENCIES_AVAILABLE = False
    sys.exit(1)


def create_text_pdf(output_path: Path, page_texts: list):
    """Create a PDF with multiple pages of text"""
    if not REPORTLAB_AVAILABLE:
        return False
    
    c = canvas.Canvas(str(output_path), pagesize=letter)
    width, height = letter
    
    for page_num, text_lines in enumerate(page_texts):
        c.setFont("Helvetica", 16)
        c.drawString(100, height - 100, f"Page {page_num + 1}")
        
        c.setFont("Helvetica", 12)
        y = height - 150
        for line in text_lines:
            c.drawString(100, y, line)
            y -= 20
        
        c.showPage()
    
    c.save()
    print(f"✓ Created: {output_path.name}")
    return True


def create_sample_pdfs(test_dir: Path):
    """Create sample PDFs for testing"""
    test_dir.mkdir(exist_ok=True)
    
    # Create Document 1: Invoice (all pages correct orientation)
    invoice_pages = [
        [
            "INVOICE #12345",
            "Date: January 5, 2026",
            "Customer: John Doe",
            "Amount: $1,000.00"
        ],
        [
            "INVOICE DETAILS",
            "Item 1: Widget A - $500.00",
            "Item 2: Widget B - $500.00",
            "Total: $1,000.00"
        ]
    ]
    invoice_path = test_dir / "invoice_001.pdf"
    create_text_pdf(invoice_path, invoice_pages)
    
    # Create Document 2: Report (will be rotated)
    report_pages = [
        [
            "QUARTERLY REPORT",
            "Q4 2025",
            "Revenue: $50,000",
            "Expenses: $30,000",
            "Profit: $20,000"
        ],
        [
            "PERFORMANCE METRICS",
            "Customer Satisfaction: 95%",
            "On-time Delivery: 98%",
            "Quality Score: 4.8/5.0"
        ],
        [
            "FUTURE OUTLOOK",
            "Expected growth: 15%",
            "New markets: 3",
            "Product launches: 2"
        ]
    ]
    report_path_normal = test_dir / "report_normal.pdf"
    create_text_pdf(report_path_normal, report_pages)
    
    # Create rotated version
    report_path_rotated = test_dir / "report_rotated.pdf"
    reader = PyPDF2.PdfReader(str(report_path_normal))
    writer = PyPDF2.PdfWriter()
    
    # Rotate pages differently
    page1 = reader.pages[0]
    page1.rotate(90)
    writer.add_page(page1)
    
    page2 = reader.pages[1]
    page2.rotate(270)
    writer.add_page(page2)
    
    if len(reader.pages) > 2:
        page3 = reader.pages[2]
        page3.rotate(180)
        writer.add_page(page3)
    
    with open(report_path_rotated, 'wb') as f:
        writer.write(f)
    print(f"✓ Created: {report_path_rotated.name} (rotated)")
    
    # Create Document 3: Contract
    contract_pages = [
        [
            "EMPLOYMENT CONTRACT",
            "This agreement is made between:",
            "Employer: ABC Corporation",
            "Employee: Jane Smith",
            "Effective Date: January 1, 2026"
        ]
    ]
    contract_path = test_dir / "contract_002.pdf"
    create_text_pdf(contract_path, contract_pages)
    
    return [invoice_path, report_path_rotated, contract_path]


def main():
    """Main demo function"""
    print("\n" + "="*60)
    print("Batch PDF Auto-Rotation Demo")
    print("="*60 + "\n")
    
    # Create test directory
    test_dir = Path("/tmp/batch_rotation_test")
    test_dir.mkdir(exist_ok=True)
    
    # Create sample PDFs
    print("Creating sample PDFs...")
    if REPORTLAB_AVAILABLE:
        pdf_files = create_sample_pdfs(test_dir)
    else:
        print("Skipping PDF creation (reportlab not available)")
        return
    
    print()
    
    # Initialize batch processor
    print("Initializing batch processor...")
    processor = BatchRotationProcessor(
        confidence_threshold=0.01,  # Very low threshold for demo (synthetic PDFs have little text)
        backup_originals=True,
        output_suffix="_auto_rotated"
    )
    print(f"  Confidence threshold: 1% (low for demo purposes)")
    print(f"  Note: Real scanned documents typically have 80-95% confidence")
    
    # Add PDFs to queue
    print("\nAdding PDFs to processing queue...")
    for pdf_file in pdf_files:
        processor.add_pdf(pdf_file)
    
    # Print summary before processing
    print()
    processor.print_summary()
    
    # Process all PDFs
    print("Processing PDFs...")
    output_dir = test_dir / "output"
    results = processor.process_all(
        auto_rotate_high_confidence=True,
        output_dir=output_dir
    )
    
    # Print final results
    print("\n" + "="*60)
    print("Processing Complete!")
    print("="*60)
    print(f"Files processed: {results['total_files']}")
    print(f"Total pages: {results['total_pages']}")
    print(f"Pages rotated: {results['pages_rotated']}")
    print(f"Pages skipped: {results['pages_skipped']}")
    print(f"Errors: {results['errors']}")
    print()
    print(f"Output directory: {output_dir}")
    print(f"Original backups saved with .pdf.bak extension")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
