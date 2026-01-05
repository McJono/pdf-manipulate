# PDF Manipulate - Development Setup

## Quick Start

### 1. Install Dependencies

```bash
# Create and activate virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python3 main.py
```

## Project Structure

```
pdf-manipulate/
├── README.md                 # Project overview
├── TODO.md                   # Development roadmap
├── main.py                   # Application entry point
├── requirements.txt          # Python dependencies
├── setup.py                  # Package configuration
├── pytest.ini               # Test configuration
│
├── docs/                    # Documentation
│   ├── DELIVERABLES.md
│   ├── GETTING_STARTED.md
│   ├── NAMING_TEMPLATES.md
│   ├── ROADMAP.md
│   └── USER_STORIES.md
│
├── src/                     # Source code
│   ├── config/              # Configuration management
│   │   └── manager.py
│   ├── naming/              # Naming template system
│   │   ├── parser.py
│   │   └── variables.py
│   ├── pdf_operations/      # PDF manipulation
│   │   ├── loader.py
│   │   ├── merger.py
│   │   └── rotation.py
│   ├── ui/                  # User interface
│   │   └── main_window.py
│   └── utils/               # Utilities
│       ├── logger.py
│       └── validators.py
│
└── tests/                   # Test suite
    ├── test_naming.py
    └── test_validators.py
```

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_naming.py

# Run with coverage
pytest --cov=src --cov-report=html
```

## Features Implemented

### ✅ Core Infrastructure
- Project structure with proper Python package organization
- Configuration management system (JSON-based)
- Logging utility
- Input validation and sanitization

### ✅ PDF Operations
- PDF loader with metadata extraction
- Rotation functionality (90°, 180°, 270°)
- PDF merging with metadata preservation
- Page-level operations

### ✅ Naming Template System
- Template parser with variable substitution
- Date arithmetic support (`{date+7}`, `{date-30}`)
- Counter with padding (`{counter:3}`)
- Filename sanitization
- Supported variables:
  - `{date}` - Current date
  - `{date+N}` - Date offset
  - `{timestamp}` - Full timestamp
  - `{name}` - User input
  - `{filename}` - Original filename
  - `{counter}` - Sequential number

### ✅ User Interface
- Tkinter-based GUI
- Main window with menu system
- File selection dialogs
- Placeholder screens for features

## Configuration

The application uses `config.json` for settings. If not present, it uses defaults from `config.example.json`.

Example configuration:
```json
{
  "naming": {
    "templates": [
      "{date+7}_{name}",
      "{name}_{date}",
      "Invoice_{date}_{name}"
    ],
    "date_format": "YYYY-MM-DD"
  }
}
```

## Development Status

✅ **Phase 1 Complete**: Foundation
- Project setup ✅
- Core PDF operations ✅
- Configuration system ✅
- Naming template engine ✅
- Basic UI framework ✅

🚧 **Next Steps** (See TODO.md):
- OCR integration for auto-rotation
- Preview system implementation
- Complete merge UI with drag-and-drop
- Batch processing
- Testing and polish

## Dependencies

Core libraries:
- PyPDF2 - PDF manipulation
- PyMuPDF - Advanced PDF operations
- Pillow - Image processing
- pdf2image - PDF to image conversion
- pytesseract - OCR (planned for auto-rotation)

Development tools:
- pytest - Testing framework
- black - Code formatter
- pylint - Linter

## Contributing

1. Review the [TODO.md](TODO.md) for available tasks
2. Check [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md) for detailed setup
3. Follow the coding standards in the documentation
4. Write tests for new features
5. Submit pull requests with clear descriptions

## License

TBD

## Support

For questions or issues, please open an issue on GitHub.
