# Troubleshooting Guide

This guide helps you diagnose and fix common issues with PDF Manipulate.

---

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Dependency Problems](#dependency-problems)
3. [Application Startup Issues](#application-startup-issues)
4. [Auto-Rotation Problems](#auto-rotation-problems)
5. [Preview & Display Issues](#preview--display-issues)
6. [Merge Operation Failures](#merge-operation-failures)
7. [File Access & Permission Errors](#file-access--permission-errors)
8. [Performance Issues](#performance-issues)
9. [Configuration Problems](#configuration-problems)
10. [Platform-Specific Issues](#platform-specific-issues)

---

## Installation Issues

### Problem: `pip install` fails

**Symptoms:**
- Error messages during `pip install -r requirements.txt`
- Packages fail to download
- Permission errors

**Solutions:**

1. **Update pip:**
   ```bash
   python3 -m pip install --upgrade pip
   ```

2. **Use user installation (if permission denied):**
   ```bash
   pip install --user -r requirements.txt
   ```

3. **Use virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Check Python version:**
   ```bash
   python3 --version  # Must be 3.8+
   ```

### Problem: Installation succeeds but imports fail

**Symptoms:**
- `ModuleNotFoundError: No module named 'PyPDF2'`
- Packages appear installed but can't be imported

**Solutions:**

1. **Check you're using the right Python:**
   ```bash
   which python3  # Linux/macOS
   where python   # Windows
   ```

2. **Verify installation:**
   ```bash
   pip list | grep PyPDF2
   pip list | grep Pillow
   ```

3. **Try reinstalling:**
   ```bash
   pip uninstall PyPDF2 Pillow
   pip install PyPDF2 Pillow
   ```

---

## Dependency Problems

### Problem: Tesseract OCR not found

**Symptoms:**
- Auto-rotation feature shows "Tesseract not found" error
- OCR operations fail

**Solutions:**

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
1. Download installer from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
2. Install to default location (usually `C:\Program Files\Tesseract-OCR`)
3. Add to PATH:
   - Open "Environment Variables"
   - Add `C:\Program Files\Tesseract-OCR` to PATH
   - Restart command prompt

**Verify installation:**
```bash
tesseract --version
```

### Problem: PyMuPDF installation fails

**Symptoms:**
- `ERROR: Failed building wheel for PyMuPDF`
- Compilation errors during installation

**Solutions:**

1. **Install pre-built binary:**
   ```bash
   pip install --upgrade pip
   pip install PyMuPDF --no-cache-dir
   ```

2. **On Linux, install development libraries:**
   ```bash
   sudo apt-get install python3-dev
   sudo apt-get install libmupdf-dev
   ```

3. **If still failing, skip PyMuPDF:**
   - Edit `requirements.txt` and comment out or remove PyMuPDF
   - The program will use pdf2image as fallback

### Problem: pdf2image requires poppler

**Symptoms:**
- `PDFInfoNotInstalledError: Unable to get page count`
- Preview generation fails

**Solutions:**

**Ubuntu/Debian:**
```bash
sudo apt-get install poppler-utils
```

**macOS:**
```bash
brew install poppler
```

**Windows:**
1. Download poppler from [here](http://blog.alivate.com.au/poppler-windows/)
2. Extract to `C:\Program Files\poppler`
3. Add `C:\Program Files\poppler\bin` to PATH

---

## Application Startup Issues

### Problem: Application window doesn't appear

**Symptoms:**
- `python3 main.py` runs but no window appears
- Process runs but nothing visible

**Solutions:**

1. **Check for errors:**
   ```bash
   python3 main.py 2>&1 | tee output.log
   ```

2. **Verify tkinter is available:**
   ```python
   python3 -c "import tkinter; print('tkinter OK')"
   ```

3. **On Linux, install tkinter:**
   ```bash
   sudo apt-get install python3-tk
   ```

4. **Try running with display:**
   ```bash
   export DISPLAY=:0  # Linux
   python3 main.py
   ```

### Problem: Application crashes immediately

**Symptoms:**
- Window appears briefly then closes
- Segmentation fault
- ImportError on startup

**Solutions:**

1. **Run verification script:**
   ```bash
   python3 verify_installation.py
   ```

2. **Check logs:**
   ```bash
   tail -f pdf_manipulate.log
   ```

3. **Test with minimal imports:**
   ```python
   python3 -c "from src.ui.main_window import MainWindow; print('OK')"
   ```

4. **Update all dependencies:**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

---

## Auto-Rotation Problems

### Problem: Orientation detection fails

**Symptoms:**
- All pages detected as same orientation
- Confidence scores are very low (< 0.3)
- OCR returns no results

**Solutions:**

1. **Verify Tesseract works:**
   ```bash
   tesseract --version
   tesseract test_image.png output
   ```

2. **Check document language:**
   - Edit `config.json`:
     ```json
     {
       "auto_rotation": {
         "ocr_language": "eng"
       }
     }
     ```
   - Available languages: `tesseract --list-langs`

3. **Install language packs (if needed):**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr-fra  # French
   sudo apt-get install tesseract-ocr-deu  # German
   ```

4. **Check PDF quality:**
   - Low-quality scans may not detect well
   - Image-only PDFs need high DPI
   - Try with a different test PDF

### Problem: Auto-rotation is very slow

**Symptoms:**
- Processing takes minutes per page
- High CPU usage
- Progress bar barely moves

**Solutions:**

1. **Reduce confidence threshold:**
   ```json
   {
     "auto_rotation": {
       "confidence_threshold": 0.6
     }
   }
   ```

2. **Process fewer pages at once:**
   - Split large PDFs
   - Process in smaller batches

3. **Check system resources:**
   ```bash
   top  # Linux/macOS
   # Look for high CPU/memory usage
   ```

4. **Close other applications:**
   - Free up RAM
   - Reduce CPU load

---

## Preview & Display Issues

### Problem: Preview images are blank or corrupted

**Symptoms:**
- White/black squares instead of preview
- Distorted or pixelated previews
- "Failed to generate preview" errors

**Solutions:**

1. **Check dependencies:**
   ```bash
   pip install --upgrade Pillow pdf2image PyMuPDF
   ```

2. **Test preview generation:**
   ```python
   from src.pdf_operations.preview import PDFPreviewGenerator
   preview = PDFPreviewGenerator()
   img = preview.generate_thumbnail("test.pdf", 0)
   ```

3. **Check file is valid PDF:**
   - Open in another PDF viewer (Adobe, Firefox, etc.)
   - Try with a different PDF

4. **Reduce preview quality:**
   ```json
   {
     "ui": {
       "preview_quality": "low"
     }
   }
   ```

### Problem: Zoom doesn't work

**Symptoms:**
- Zoom buttons don't change image size
- Error when clicking zoom controls
- Image disappears after zoom

**Solutions:**

1. **Restart the application**

2. **Clear preview cache:**
   - Delete cache directory if it exists
   - Reopen the preview dialog

3. **Check available memory:**
   - High zoom levels need more RAM
   - Close other applications

4. **Update to latest version:**
   ```bash
   git pull origin main
   pip install --upgrade -r requirements.requirements.txt
   ```

---

## Merge Operation Failures

### Problem: Merge fails with "Cannot write to file"

**Symptoms:**
- Merge operation starts but fails at the end
- "Permission denied" or "File in use" errors
- Output file not created

**Solutions:**

1. **Check output directory permissions:**
   ```bash
   ls -la /path/to/output/directory  # Linux/macOS
   ```

2. **Close output file in other programs:**
   - Check if PDF is open in viewer
   - Close all PDF readers

3. **Choose different output location:**
   - Try saving to Documents or Desktop
   - Avoid system directories

4. **Check disk space:**
   ```bash
   df -h  # Linux/macOS
   # Ensure enough free space
   ```

### Problem: Merged PDF is corrupted

**Symptoms:**
- Output PDF won't open
- "File is damaged" error in viewers
- Incomplete merge

**Solutions:**

1. **Verify source PDFs:**
   - Open each source PDF individually
   - Ensure all are valid

2. **Check for file corruption:**
   ```python
   from src.pdf_operations.loader import PDFLoader
   loader = PDFLoader()
   for pdf in ["file1.pdf", "file2.pdf"]:
       metadata = loader.load(pdf)
       print(f"{pdf}: {metadata}")
   ```

3. **Try merging in smaller batches:**
   - Merge 2-3 files at a time
   - Identify problematic file

4. **Check logs:**
   ```bash
   tail -f pdf_manipulate.log
   ```

### Problem: Bookmarks are lost after merge

**Symptoms:**
- Merged PDF has no table of contents
- Bookmarks from source files missing

**Solutions:**

1. **Enable bookmark preservation:**
   ```json
   {
     "merge": {
       "preserve_bookmarks": true
     }
   }
   ```

2. **Check source PDFs have bookmarks:**
   - Open in PDF viewer
   - Look for TOC/bookmarks panel

3. **Update PyPDF2:**
   ```bash
   pip install --upgrade PyPDF2
   ```

---

## File Access & Permission Errors

### Problem: "Permission denied" when opening PDF

**Symptoms:**
- Cannot open PDF for reading
- Access denied errors
- File locked messages

**Solutions:**

1. **Check file permissions:**
   ```bash
   ls -l file.pdf  # Linux/macOS
   ```

2. **On Windows, check if file is read-only:**
   - Right-click → Properties
   - Uncheck "Read-only"

3. **Close file in other programs:**
   - Close PDF viewers
   - Close browser tabs with PDF

4. **Copy file to different location:**
   ```bash
   cp locked_file.pdf ~/Documents/copy.pdf
   ```

### Problem: Cannot save output file

**Symptoms:**
- "Access denied" when saving
- File saves but is 0 bytes
- Output directory not writable

**Solutions:**

1. **Use different output directory:**
   - Save to user home directory
   - Avoid Program Files or system directories

2. **Run with appropriate permissions:**
   ```bash
   # Don't use sudo unless necessary
   python3 main.py
   ```

3. **Check parent directory exists:**
   - Create output directory first
   - Use absolute paths

---

## Performance Issues

### Problem: Application is slow/unresponsive

**Symptoms:**
- UI freezes during operations
- Long delays when clicking buttons
- "Not responding" messages

**Solutions:**

1. **Close other applications:**
   - Free up RAM and CPU
   - Check task manager

2. **Process smaller batches:**
   - Don't merge 50+ files at once
   - Split into smaller operations

3. **Reduce preview quality:**
   ```json
   {
     "ui": {
       "preview_quality": "low"
     }
   }
   ```

4. **Clear cache/temp files:**
   - Delete temporary preview files
   - Clear system temp directory

5. **Check system requirements:**
   - Minimum: 4GB RAM, dual-core CPU
   - Recommended: 8GB RAM, quad-core CPU

### Problem: High memory usage

**Symptoms:**
- Memory usage grows during operation
- System becomes slow
- Out of memory errors

**Solutions:**

1. **Process files individually:**
   - Don't load too many previews
   - Process one at a time

2. **Restart application between batches:**
   - Clear memory
   - Start fresh

3. **Monitor memory usage:**
   ```bash
   top  # Linux/macOS
   # Watch python3 process
   ```

4. **Reduce page count:**
   - Split large PDFs before processing
   - Merge in stages

---

## Configuration Problems

### Problem: Configuration changes don't apply

**Symptoms:**
- Edited config.json but no effect
- Settings revert to defaults
- Application ignores configuration

**Solutions:**

1. **Verify JSON syntax:**
   ```bash
   python3 -m json.tool config.json
   ```

2. **Check file location:**
   - Must be in project root directory
   - Named exactly `config.json`

3. **Restart application:**
   - Close completely
   - Reopen to load new config

4. **Check for syntax errors:**
   - Missing commas
   - Unmatched brackets
   - Invalid values

### Problem: Lost configuration after update

**Symptoms:**
- Custom settings disappeared
- Back to default configuration
- config.json deleted or overwritten

**Solutions:**

1. **Backup config before updates:**
   ```bash
   cp config.json config.backup.json
   ```

2. **Restore from backup:**
   ```bash
   cp config.backup.json config.json
   ```

3. **Check git status:**
   ```bash
   git status  # See if config.json changed
   git diff config.json
   ```

---

## Platform-Specific Issues

### Linux Issues

**Problem: Tkinter not available**
```bash
sudo apt-get install python3-tk
```

**Problem: Permission errors with temp directories**
```bash
chmod 755 /tmp
export TMPDIR=~/tmp
mkdir -p ~/tmp
```

**Problem: Display issues**
```bash
export DISPLAY=:0
xhost +local:
```

### macOS Issues

**Problem: "Python not installed" despite having Python**
```bash
# Use python3 explicitly
python3 main.py

# Or create alias
alias python=python3
```

**Problem: Gatekeeper blocks application**
- System Preferences → Security & Privacy
- Allow applications from identified developers

**Problem: Command not found for brew packages**
```bash
# Add Homebrew to PATH
export PATH="/usr/local/bin:$PATH"
```

### Windows Issues

**Problem: "Python is not recognized"**
- Add Python to PATH:
  - System Properties → Environment Variables
  - Add Python installation directory to PATH

**Problem: Script hangs on Windows**
- Use `python` instead of `python3`
- Check antivirus isn't blocking

**Problem: Poppler/Tesseract not found**
- Verify PATH includes installation directories
- Use full paths in config if needed

---

## Getting Additional Help

### Collect Diagnostic Information

Before reporting an issue, gather this information:

1. **Python version:**
   ```bash
   python3 --version
   ```

2. **Operating system:**
   ```bash
   uname -a  # Linux/macOS
   # On Windows: winver
   ```

3. **Installed packages:**
   ```bash
   pip list > packages.txt
   ```

4. **Error logs:**
   ```bash
   tail -50 pdf_manipulate.log > error_log.txt
   ```

5. **Configuration:**
   ```bash
   cat config.json > current_config.txt
   ```

### Report an Issue

Open an issue on GitHub with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Diagnostic information from above
- Screenshots if relevant

### Additional Resources

- **FAQ:** [FAQ.md](FAQ.md)
- **Installation Guide:** [../INSTALL.md](../INSTALL.md)
- **Getting Started:** [GETTING_STARTED.md](GETTING_STARTED.md)
- **GitHub Issues:** https://github.com/McJono/pdf-manipulate/issues

---

## Still Having Issues?

If your problem isn't solved here:

1. Search [existing issues](https://github.com/McJono/pdf-manipulate/issues)
2. Check the [FAQ](FAQ.md)
3. Open a new issue with detailed information
4. Include diagnostic information and logs

We're here to help you get PDF Manipulate working!
