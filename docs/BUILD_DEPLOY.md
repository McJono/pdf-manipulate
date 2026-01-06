# Build and Deployment Guide

This document describes how to build, test, and deploy the PDF Manipulate application.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Development Setup](#development-setup)
- [Building](#building)
- [Testing](#testing)
- [Code Quality](#code-quality)
- [Deployment](#deployment)
- [Platform-Specific Instructions](#platform-specific-instructions)

---

## Prerequisites

### Required Software

- **Python 3.8 or higher**
- **pip** (Python package installer)
- **git** (for version control)

### System Dependencies

#### Linux (Ubuntu/Debian)
```bash
# Required for pdf2image
sudo apt-get update
sudo apt-get install -y poppler-utils

# Required for OCR (tesseract)
sudo apt-get install -y tesseract-ocr
sudo apt-get install -y tesseract-ocr-eng  # English language pack
```

#### macOS
```bash
# Using Homebrew
brew install poppler tesseract
```

#### Windows
- Download and install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
- Download poppler from: https://github.com/oschwartz10612/poppler-windows/releases/
- Add both to your system PATH

---

## Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/McJono/pdf-manipulate.git
cd pdf-manipulate
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install all dependencies
pip install -r requirements.txt

# Verify installation
python3 verify_installation.py
```

---

## Building

### Running from Source

The application can be run directly from source:

```bash
python3 main.py
```

### Creating Standalone Executable

To create a standalone executable, use PyInstaller:

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --name="PDFManipulate" \
    --windowed \
    --onefile \
    --icon=assets/icon.ico \
    --add-data "config.example.json:." \
    main.py

# Output will be in dist/ folder
```

#### macOS .app Bundle

```bash
pyinstaller --name="PDF Manipulate" \
    --windowed \
    --onefile \
    --icon=assets/icon.icns \
    --add-data "config.example.json:." \
    main.py
```

#### Windows .exe

```bash
pyinstaller --name="PDFManipulate" ^
    --windowed ^
    --onefile ^
    --icon=assets/icon.ico ^
    --add-data "config.example.json;." ^
    main.py
```

---

## Testing

### Run All Tests

```bash
# Run all tests with pytest
python3 -m pytest

# Run with coverage report
python3 -m pytest --cov=src --cov-report=html

# Run specific test file
python3 -m pytest tests/test_naming.py

# Run with verbose output
python3 -m pytest -v
```

### Test Coverage

View coverage report:
```bash
# Generate HTML report
python3 -m pytest --cov=src --cov-report=html

# Open in browser (Linux/macOS)
open htmlcov/index.html

# Open in browser (Windows)
start htmlcov/index.html
```

### Demo Scripts

Test specific features with demo scripts:

```bash
# Test orientation detection
python3 demos/demo_orientation.py

# Test batch rotation
python3 demos/demo_batch_rotation.py

# Test merge screen
python3 demos/demo_merge_screen.py

# Test naming dialog
python3 demos/demo_naming_dialog.py

# Test UI auto-rotation
python3 demos/demo_ui_autorotation.py
```

---

## Code Quality

### Linting

Run all code quality checks:

```bash
# Run linter (black, pylint, mypy, flake8)
python3 lint.py

# Run individual tools
black --check src/ tests/
pylint src/
mypy src/
flake8 src/
```

### Code Formatting

Format code with Black:

```bash
# Format all code
python3 format.py

# Or use black directly
black src/ tests/
```

### Type Checking

```bash
# Run mypy type checker
mypy src/
```

---

## Deployment

### Creating Distribution Package

#### Source Distribution

```bash
# Create source distribution
python3 setup.py sdist

# Output: dist/pdf-manipulate-x.x.x.tar.gz
```

#### Wheel Distribution

```bash
# Install wheel if needed
pip install wheel

# Create wheel
python3 setup.py bdist_wheel

# Output: dist/pdf_manipulate-x.x.x-py3-none-any.whl
```

### Installation from Package

```bash
# Install from wheel
pip install dist/pdf_manipulate-x.x.x-py3-none-any.whl

# Install from source
pip install dist/pdf-manipulate-x.x.x.tar.gz
```

---

## Platform-Specific Instructions

### Linux

#### Create AppImage

1. Install required tools:
   ```bash
   sudo apt-get install fuse libfuse2
   ```

2. Use PyInstaller to create binary
3. Package with AppImageTool:
   ```bash
   # Download AppImageTool
   wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
   chmod +x appimagetool-x86_64.AppImage
   
   # Create AppDir structure
   mkdir -p PDFManipulate.AppDir/usr/bin
   cp dist/PDFManipulate PDFManipulate.AppDir/usr/bin/
   
   # Create AppImage
   ./appimagetool-x86_64.AppImage PDFManipulate.AppDir
   ```

#### Create .deb Package

```bash
# Install required tools
sudo apt-get install dpkg-dev

# Create package structure
mkdir -p pdf-manipulate_1.0.0/DEBIAN
mkdir -p pdf-manipulate_1.0.0/usr/local/bin
mkdir -p pdf-manipulate_1.0.0/usr/share/applications

# Copy files
cp dist/PDFManipulate pdf-manipulate_1.0.0/usr/local/bin/

# Create control file
cat > pdf-manipulate_1.0.0/DEBIAN/control << EOF
Package: pdf-manipulate
Version: 1.0.0
Architecture: amd64
Maintainer: Your Name <email@example.com>
Description: PDF manipulation tool
EOF

# Build package
dpkg-deb --build pdf-manipulate_1.0.0
```

### macOS

#### Create DMG Installer

1. Build .app bundle with PyInstaller
2. Use `create-dmg` tool:
   ```bash
   # Install create-dmg
   brew install create-dmg
   
   # Create DMG
   create-dmg \
     --volname "PDF Manipulate" \
     --window-pos 200 120 \
     --window-size 800 400 \
     --icon-size 100 \
     --app-drop-link 600 185 \
     "PDF-Manipulate-1.0.0.dmg" \
     "dist/PDF Manipulate.app"
   ```

### Windows

#### Create Installer with Inno Setup

1. Download and install Inno Setup
2. Create installer script (`installer.iss`):
   ```ini
   [Setup]
   AppName=PDF Manipulate
   AppVersion=1.0.0
   DefaultDirName={pf}\PDFManipulate
   DefaultGroupName=PDF Manipulate
   OutputBaseFilename=PDFManipulate-Setup
   
   [Files]
   Source: "dist\PDFManipulate.exe"; DestDir: "{app}"
   Source: "config.example.json"; DestDir: "{app}"
   
   [Icons]
   Name: "{group}\PDF Manipulate"; Filename: "{app}\PDFManipulate.exe"
   ```

3. Compile installer:
   ```bash
   iscc installer.iss
   ```

---

## CI/CD Pipeline

### GitHub Actions (Example)

Create `.github/workflows/build.yml`:

```yaml
name: Build and Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: |
          sudo apt-get install -y tesseract-ocr poppler-utils
          pip install -r requirements.txt
      - name: Run tests
        run: python3 -m pytest
      - name: Run linter
        run: python3 lint.py
```

---

## Release Checklist

Before creating a release:

- [ ] Update version number in `setup.py`
- [ ] Update CHANGELOG.md
- [ ] Run all tests: `pytest`
- [ ] Run linter: `python3 lint.py`
- [ ] Build executable for all platforms
- [ ] Test executable on each platform
- [ ] Update documentation
- [ ] Create git tag: `git tag -a v1.0.0 -m "Release 1.0.0"`
- [ ] Push tag: `git push origin v1.0.0`
- [ ] Create GitHub release with binaries
- [ ] Update README.md with download links

---

## Troubleshooting Build Issues

### Missing Dependencies

If you get import errors, ensure all dependencies are installed:
```bash
pip install -r requirements.txt --force-reinstall
```

### PyInstaller Issues

- **Hidden imports**: Add to spec file:
  ```python
  hiddenimports=['PIL', 'pdf2image', 'pytesseract']
  ```

- **Binary dependencies**: Use `--add-binary`:
  ```bash
  pyinstaller --add-binary "/usr/bin/tesseract:bin" main.py
  ```

### Platform-Specific Errors

- **Linux**: Ensure system packages installed (tesseract, poppler)
- **macOS**: Install via Homebrew, not pip (for binary tools)
- **Windows**: Check PATH includes tesseract and poppler

---

## Performance Optimization

### Reduce Executable Size

```bash
# Use UPX to compress executable
pyinstaller --onefile --upx-dir=/path/to/upx main.py
```

### Optimize Python Code

- Remove debug logging in production
- Use `python -O` for optimized bytecode
- Minimize dependencies in requirements.txt

---

## Support

For build/deployment issues:
- Check [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- Review [FAQ.md](docs/FAQ.md)
- Open an issue on GitHub

---

## License

See LICENSE file for distribution terms.
