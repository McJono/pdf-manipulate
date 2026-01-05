#!/usr/bin/env python3
"""
Verification script for PDF Manipulate installation
Run this to verify the core functionality works
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))


def test_imports():
    """Test that all core modules can be imported"""
    print("Testing imports...")
    try:
        from src.config.manager import config
        from src.utils.logger import setup_logger
        from src.utils.validators import sanitize_filename
        from src.naming.parser import TemplateParser
        print("  ✓ All core modules import successfully")
        return True
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        return False


def test_naming_system():
    """Test the naming template system"""
    print("\nTesting naming system...")
    try:
        from src.naming.parser import parse_template
        from datetime import datetime

        # Test basic template
        result = parse_template("{date}_{name}.pdf", name="test")
        expected_date = datetime.now().strftime("%Y-%m-%d")
        assert result == f"{expected_date}_test.pdf"

        # Test date offset
        result = parse_template("{date+7}_{name}.pdf", name="invoice")
        assert "_invoice.pdf" in result

        print("  ✓ Naming system works correctly")
        return True
    except Exception as e:
        print(f"  ✗ Naming test failed: {e}")
        return False


def test_validators():
    """Test validation utilities"""
    print("\nTesting validators...")
    try:
        from src.utils.validators import sanitize_filename

        tests = [
            ("document.pdf", "document.pdf"),
            ("test/file.pdf", "testfile.pdf"),
            ("  document.pdf  ", "document.pdf"),
        ]

        for input_val, expected in tests:
            result = sanitize_filename(input_val)
            assert result == expected, f"Expected {expected}, got {result}"

        print("  ✓ Validators work correctly")
        return True
    except Exception as e:
        print(f"  ✗ Validator test failed: {e}")
        return False


def test_config():
    """Test configuration system"""
    print("\nTesting configuration...")
    try:
        from src.config.manager import config

        # Check default config loaded
        assert config.get("naming.date_format") == "YYYY-MM-DD"
        assert len(config.get("naming.templates")) >= 3

        print("  ✓ Configuration system works correctly")
        return True
    except Exception as e:
        print(f"  ✗ Config test failed: {e}")
        return False


def check_optional_dependencies():
    """Check if optional dependencies are installed"""
    print("\nChecking optional dependencies...")
    optional = {
        "PyPDF2": "PDF manipulation",
        "PyMuPDF": "Advanced PDF operations",
        "PIL": "Image processing",
        "pytesseract": "OCR functionality",
    }

    missing = []
    for module, description in optional.items():
        try:
            if module == "PIL":
                import PIL
            else:
                __import__(module)
            print(f"  ✓ {module:15} - {description}")
        except ImportError:
            print(f"  ✗ {module:15} - {description} (not installed)")
            missing.append(module)

    if missing:
        print(f"\nTo install missing dependencies, run:")
        print(f"  pip install -r requirements.txt")

    return len(missing) == 0


def main():
    """Run all verification tests"""
    print("=" * 60)
    print("PDF Manipulate - Installation Verification")
    print("=" * 60)

    results = []
    results.append(test_imports())
    results.append(test_naming_system())
    results.append(test_validators())
    results.append(test_config())

    print("\n" + "=" * 60)
    if all(results):
        print("✅ All core functionality tests PASSED!")
        print("=" * 60)

        # Check optional dependencies
        deps_ok = check_optional_dependencies()

        if deps_ok:
            print("\n✅ All dependencies installed!")
            print("\nYou can now run the application with:")
            print("  python3 main.py")
        else:
            print("\n⚠️  Some dependencies are missing.")
            print("Install them to use all features.")

        return 0
    else:
        print("❌ Some tests FAILED!")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
