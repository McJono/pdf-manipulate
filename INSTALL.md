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
├── INSTALL.md                # Installation and setup guide
├── TODO.md                   # Development roadmap
├── main.py                   # Application entry point
├── requirements.txt          # Python dependencies
├── setup.py                  # Package configuration
├── pytest.ini               # Test configuration
├── config.example.json      # Example configuration
│
├── docs/                    # Documentation
│   ├── BUILD_DEPLOY.md
│   ├── CONTRIBUTING.md
│   ├── DELIVERABLES.md
│   ├── FAQ.md
│   ├── GETTING_STARTED.md
│   ├── IMPLEMENTATION_SUMMARY.md
│   ├── NAMING_TEMPLATES.md
│   ├── PHASE2_SUMMARY.md
│   ├── PHASE3_SUMMARY.md
│   ├── PHASE4_SUMMARY.md
│   ├── PHASE5_ENHANCEMENTS.md
│   ├── PHASE6_SUMMARY.md
│   ├── PROJECT_STATUS.md
│   ├── ROADMAP.md
│   ├── TROUBLESHOOTING.md
│   └── USER_STORIES.md
│
├── demos/                   # Demo scripts
│   ├── demo_batch_rotation.py
│   ├── demo_merge_screen.py
│   ├── demo_naming_dialog.py
│   ├── demo_orientation.py
│   ├── demo_tooltips.py
│   └── demo_ui_autorotation.py
│
├── src/                     # Source code
│   ├── config/              # Configuration management
│   │   └── manager.py
│   ├── naming/              # Naming template system
│   │   ├── parser.py
│   │   └── variables.py
│   ├── pdf_operations/      # PDF manipulation
│   │   ├── batch_rotator.py
│   │   ├── loader.py
│   │   ├── merger.py
│   │   ├── orientation_detector.py
│   │   ├── preview.py
│   │   └── rotation.py
│   ├── ui/                  # User interface
│   │   ├── auto_rotation_screen.py
│   │   ├── main_window.py
│   │   ├── merge_screen.py
│   │   ├── naming_dialog.py
│   │   └── tooltip.py
│   └── utils/               # Utilities
│       ├── logger.py
│       └── validators.py
│
└── tests/                   # Test suite
    ├── test_integration.py
    ├── test_naming.py
    ├── test_orientation_detector.py
    ├── test_preferences.py
    ├── test_preview.py
    ├── test_undo_redo.py
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
- Comprehensive test suite (56 tests)

### ✅ PDF Operations
- PDF loader with metadata extraction
- Rotation functionality (90°, 180°, 270°)
- PDF merging with metadata preservation
- Page-level operations
- OCR-based auto-rotation with confidence scoring
- Batch rotation processing
- Preview generation with caching

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
- Auto-rotation screen with manual override
- Merge screen with preview functionality
- Naming dialog with template selection
- Tooltips throughout the interface
- File selection and preview dialogs
- Zoom controls for previews
- Drag-free reordering controls

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

✅ **Completed Phases**:
- Phase 1: Foundation ✅
  - Project setup and structure
  - Core PDF operations
  - Configuration system
  - Naming template engine
  - Basic UI framework
- Phase 2: Auto-Rotation ✅
  - OCR integration with Tesseract
  - Orientation detection engine
  - Batch processing system
  - Auto-rotation UI with manual override
- Phase 3: Merge with Preview ✅
  - Preview generation system
  - File browser with metadata
  - Merge queue with ordering controls
  - Full-page preview dialogs
- Phase 4: Naming Integration ✅
  - Naming dialog component
  - Template selection UI
  - Merge workflow integration
  - Merge history logging
- Phase 5: UI Enhancements ✅
  - Tooltip system
  - Zoom controls
  - Preferences system
  - Undo/redo framework

🚧 **Next Steps** (See [TODO.md](TODO.md) and [docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md)):
- Additional testing and polish
- Performance optimizations
- Deployment preparation
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
