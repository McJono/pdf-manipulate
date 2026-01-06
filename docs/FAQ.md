# Frequently Asked Questions (FAQ)

## General Questions

### What is PDF Manipulate?

PDF Manipulate is a comprehensive PDF manipulation program that automates PDF rotation, provides merging capabilities with preview, and supports intelligent file naming based on configurable templates.

### What can I do with PDF Manipulate?

You can:
- **Auto-rotate PDFs** using OCR-based orientation detection
- **Merge multiple PDFs** with preview and custom ordering
- **Use intelligent naming** with templates supporting date arithmetic
- **Batch process** multiple files efficiently
- **Preview PDFs** before merging with zoom capabilities

### What platforms does it support?

PDF Manipulate is cross-platform and works on:
- Windows 10/11
- macOS (latest versions)
- Linux (Ubuntu, Fedora, and other distributions)

---

## Installation & Setup

### How do I install PDF Manipulate?

1. Clone the repository:
   ```bash
   git clone https://github.com/McJono/pdf-manipulate.git
   cd pdf-manipulate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Verify installation:
   ```bash
   python3 verify_installation.py
   ```

See [INSTALL.md](../INSTALL.md) for detailed instructions.

### What dependencies are required?

**Required:**
- Python 3.8 or higher
- PyPDF2 (PDF operations)
- Pillow (image processing)
- tkinter (usually comes with Python)

**Optional:**
- PyMuPDF (faster preview generation)
- pytesseract & tesseract-ocr (for auto-rotation)
- pdf2image (for preview generation)

### Do I need to install Tesseract separately?

Yes, for the auto-rotation feature. Tesseract OCR must be installed on your system:

- **Ubuntu/Debian:** `sudo apt-get install tesseract-ocr`
- **macOS:** `brew install tesseract`
- **Windows:** Download from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)

### Can I use the program without Tesseract?

Yes! The core features (merging, manual rotation, naming) work without Tesseract. Only the automatic orientation detection requires it.

---

## Using the Program

### How do I start the application?

Run the main program:
```bash
python3 main.py
```

Or on Windows:
```bash
python main.py
```

### How do I merge PDFs?

1. Click **"Tools"** → **"Merge PDFs"** in the menu
2. Click **"Open Folder"** or **"Add Files"** to select PDFs
3. Double-click files to add them to the merge queue
4. Reorder using **"Move Up"** / **"Move Down"** buttons
5. Click **"Merge PDFs"** button
6. Enter a filename using the template system
7. Choose save location

### How do I auto-rotate PDFs?

1. Click **"Tools"** → **"Auto-Rotate"** in the menu
2. Select PDFs to process
3. The program will analyze orientation
4. Review suggestions and make manual adjustments if needed
5. Click to apply rotations
6. Choose output directory

### What are naming templates?

Naming templates let you create filenames with dynamic content:

- `{date}` - Today's date (2026-01-06)
- `{date+7}` - Date 7 days from now
- `{date-30}` - Date 30 days ago
- `{name}` - User-provided name
- `{filename}` - Original filename
- `{counter}` - Sequential number

**Example:** `Invoice_{date+7}_{name}.pdf` → `Invoice_2026-01-13_ClientABC.pdf`

See [NAMING_TEMPLATES.md](NAMING_TEMPLATES.md) for more details.

### How do I configure the program?

Configuration is stored in `config.json`. You can:

1. Edit `config.json` directly
2. Copy `config.example.json` and modify it
3. Use the Settings dialog (Tools → Settings) *[coming soon]*

### Can I change the date format?

Yes! In `config.json`, modify the `naming.date_format` setting:

```json
{
  "naming": {
    "date_format": "DD-MM-YYYY"
  }
}
```

Supported formats: `YYYY-MM-DD`, `DD-MM-YYYY`, `MM-DD-YYYY`, and custom formats.

---

## Features & Capabilities

### Can I preview PDFs before merging?

Yes! Click on any file in the merge screen to see a thumbnail preview. Double-click to open a full-page preview with zoom controls.

### Can I zoom in the preview?

Yes! The full-page preview dialog has:
- **Zoom In** button (increases by 25%)
- **Zoom Out** button (decreases by 25%)
- **Reset** button (returns to 100%)
- Zoom range: 25% to 300%

### How accurate is the auto-rotation?

Auto-rotation uses OCR (Optical Character Recognition) and typically achieves 90%+ accuracy on documents with readable text. Accuracy depends on:
- Text quality and clarity
- Document language (configure in `config.json`)
- Scan quality for scanned documents

### Can I rotate pages manually?

Yes! The auto-rotation screen provides manual rotation controls for each page. You can rotate by 90°, 180°, or 270°.

### Does merging preserve bookmarks?

Yes! By default, PDF Manipulate preserves bookmarks (table of contents) when merging. This can be configured in `config.json`:

```json
{
  "merge": {
    "preserve_bookmarks": true
  }
}
```

### Can I merge PDFs with different page sizes?

Yes! The program handles PDFs with different page sizes gracefully. Each page retains its original dimensions in the merged document.

---

## Troubleshooting

### The program won't start

**Check Python version:**
```bash
python3 --version
```
Must be 3.8 or higher.

**Verify installation:**
```bash
python3 verify_installation.py
```

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.

### Auto-rotation says "Tesseract not found"

Install Tesseract OCR for your platform:

- **Ubuntu/Debian:** `sudo apt-get install tesseract-ocr`
- **macOS:** `brew install tesseract`
- **Windows:** Download installer from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

After installation, restart the application.

### Preview images are not loading

**Check dependencies:**
```bash
pip install Pillow pdf2image PyMuPDF
```

**On Linux, install poppler-utils:**
```bash
sudo apt-get install poppler-utils
```

**On macOS:**
```bash
brew install poppler
```

### I get "Permission denied" errors

**Check file permissions:**
- Ensure you have read access to source PDFs
- Ensure you have write access to output directory
- On Linux/macOS, check with: `ls -la`

**Try running from a different directory:**
```bash
cd ~/Documents
python3 /path/to/pdf-manipulate/main.py
```

### Merge fails with "Cannot open file"

**Possible causes:**
1. File is open in another program (close it)
2. File is corrupted (try opening in a PDF viewer)
3. Insufficient disk space (check available space)
4. File path contains special characters (rename file)

### The program is slow with large PDFs

**Tips for better performance:**

1. **Reduce preview quality** in `config.json`:
   ```json
   {
     "ui": {
       "preview_quality": "low"
     }
   }
   ```

2. **Close other applications** to free memory

3. **Process fewer files at once** in batch operations

4. **Use PyMuPDF** for faster preview generation (install with `pip install PyMuPDF`)

---

## Configuration

### Where is the configuration file?

Configuration is stored in `config.json` in the project root directory. If it doesn't exist, the program uses defaults from `config.example.json`.

### How do I reset to default settings?

Delete or rename `config.json`. The program will use default settings on next run.

To create a fresh config:
```bash
cp config.example.json config.json
```

### What can I configure?

**Auto-rotation:**
- Confidence threshold
- OCR language
- Enabled/disabled

**Merging:**
- Selection mode (click order, manual reorder)
- Preserve bookmarks
- Delete source files after merge

**Naming:**
- Templates
- Date format
- Default template

**UI:**
- Theme (light/dark) *[coming soon]*
- Preview quality

See `config.example.json` for all available options.

---

## Advanced Usage

### Can I use this from the command line?

Currently, PDF Manipulate is primarily a GUI application. Command-line interface is planned for a future release.

### Can I automate batch processing?

Yes! You can:
1. Use the batch auto-rotation feature
2. Process entire folders at once
3. Configure templates for consistent naming

Scheduled/scripted automation via CLI is planned for future releases.

### How do I contribute or report bugs?

- **Report bugs:** Open an issue on [GitHub](https://github.com/McJono/pdf-manipulate/issues)
- **Contribute code:** See [CONTRIBUTING.md](../CONTRIBUTING.md)
- **Suggest features:** Open a feature request on GitHub

### Is there an API for integration?

Currently, the modules can be imported and used programmatically:

```python
from src.pdf_operations.merger import PDFMerger
from src.naming.parser import TemplateParser

# Merge PDFs
merger = PDFMerger()
merger.merge(["file1.pdf", "file2.pdf"], "output.pdf")

# Use naming templates
parser = TemplateParser()
filename = parser.parse("{date}_{name}.pdf", user_variables={"name": "report"})
```

A formal API is planned for future releases.

---

## Performance & Limitations

### What's the maximum PDF size?

There's no hard limit, but performance may degrade with very large files (100+ MB or 500+ pages). For best performance:
- Keep individual PDFs under 50 MB
- Split very large PDFs before processing

### How many files can I merge at once?

Tested with up to 100 files. The practical limit depends on:
- Available RAM
- Individual file sizes
- System performance

### Does it support password-protected PDFs?

Currently, no. Password-protected PDFs must be unlocked before using PDF Manipulate. This feature is planned for a future release.

### Can I edit PDF content?

No, PDF Manipulate focuses on:
- Rotation
- Merging
- Naming

Content editing (text, annotations, etc.) is not currently supported but may be added in future releases.

---

## Getting Help

### Where can I find documentation?

- **Quick Start:** [README.md](../README.md)
- **Installation:** [INSTALL.md](../INSTALL.md)
- **Getting Started:** [GETTING_STARTED.md](GETTING_STARTED.md)
- **Naming Templates:** [NAMING_TEMPLATES.md](NAMING_TEMPLATES.md)
- **Troubleshooting:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **User Stories:** [USER_STORIES.md](USER_STORIES.md)

### How do I get support?

1. Check this FAQ
2. Read the [Troubleshooting Guide](TROUBLESHOOTING.md)
3. Search [existing issues](https://github.com/McJono/pdf-manipulate/issues)
4. Open a new issue with details about your problem

### Can I request features?

Yes! Open a feature request on GitHub with:
- Clear description of the feature
- Use case / why it's needed
- Any relevant examples

---

## About the Project

### Is PDF Manipulate free?

Yes! PDF Manipulate is open source software. See the LICENSE file for details.

### Who maintains this project?

PDF Manipulate is maintained by the open source community. See [CONTRIBUTING.md](../CONTRIBUTING.md) for how to get involved.

### What's the roadmap?

See [ROADMAP.md](ROADMAP.md) for planned features and development phases.

Current priorities:
- Settings/Preferences dialog
- Command-line interface
- Package distribution (standalone executables)
- Additional PDF operations (split, extract, etc.)

---

## Still Have Questions?

If your question isn't answered here:

1. Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Browse the [documentation](.)
3. Search [GitHub issues](https://github.com/McJono/pdf-manipulate/issues)
4. Open a new issue with the `question` label

We're here to help!
