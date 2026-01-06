# PDF Manipulate

An intelligent PDF manipulation program that automates document processing with features for auto-rotation, merging, and smart file naming.

## Overview

This application streamlines PDF workflow management by providing:

1. **Auto-Rotation**: Automatically detect and rotate pages that are facing down, with manual override capabilities
2. **Interactive Merging**: Select and merge PDFs with live previews and flexible ordering
3. **Smart Naming**: Configure file naming templates with date arithmetic and custom variables

## Features

### 🔄 Auto-Rotation
- Automatically detects page orientation using OCR and text analysis
- Provides confidence scores for rotation suggestions
- Manual review interface for corrections
- Batch processing support for multiple files

### 🔗 Merge with Preview
- Visual file selection with thumbnail previews
- Double-click to preview full pages
- Click-to-merge with order tracking
- Configurable selection modes (click order or manual reorder)
- Drag-and-drop support

### 📝 Intelligent Naming
- Template-based file naming system
- Date arithmetic support (e.g., `{date+7}` for 7 days from now)
- Variables: `{date}`, `{name}`, `{filename}`, `{timestamp}`, `{counter}`
- Custom naming prompts with labels
- Configuration file for reusable templates

## Quick Start

For installation and setup instructions, see [INSTALL.md](INSTALL.md).

Basic usage:
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python3 main.py
```

See [TODO.md](TODO.md) for the comprehensive development roadmap and implementation plan.

## Configuration Example

```json
{
  "naming": {
    "templates": [
      "{date+7}_{name}",
      "{name}_{date}",
      "Invoice_{date}_{name}"
    ],
    "date_format": "YYYY-MM-DD"
  },
  "merge": {
    "selection_mode": "click_order"
  }
}
```

## Workflow

1. **Load PDFs** → Application scans and loads PDF files
2. **Auto-Rotate** → Automatically detects and rotates incorrectly oriented pages
3. **Manual Review** → Review and adjust rotation as needed
4. **Select & Preview** → Choose files to merge with thumbnail previews
5. **Merge** → Combine selected PDFs in chosen order
6. **Name & Save** → Apply naming template and save output

## Documentation

### Quick Reference
- [INSTALL.md](INSTALL.md) - Installation and setup guide
- [TODO.md](TODO.md) - Complete development roadmap and task breakdown

### Detailed Documentation
- [PROJECT_STATUS.md](docs/PROJECT_STATUS.md) - Current project status and completed features
- [ROADMAP.md](docs/ROADMAP.md) - Development timeline and milestones
- [USER_STORIES.md](docs/USER_STORIES.md) - User personas and feature requirements
- [NAMING_TEMPLATES.md](docs/NAMING_TEMPLATES.md) - Naming template system reference
- [GETTING_STARTED.md](docs/GETTING_STARTED.md) - Developer onboarding guide
- [CONTRIBUTING.md](docs/CONTRIBUTING.md) - Contribution guidelines
- [FAQ.md](docs/FAQ.md) - Frequently asked questions
- [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - Common issues and solutions

### Demo Scripts
Demo scripts are available in the `demos/` folder:
- `demos/demo_orientation.py` - Test orientation detection
- `demos/demo_batch_rotation.py` - Batch rotation processing
- `demos/demo_merge_screen.py` - File merging with preview
- `demos/demo_naming_dialog.py` - Template-based naming
- `demos/demo_ui_autorotation.py` - Auto-rotation UI
- `demos/demo_tooltips.py` - Tooltip functionality

## Technology Stack

- **Language**: Python 3.8+
- **PDF Processing**: PyPDF2, PyMuPDF (fitz)
- **OCR**: Tesseract, pytesseract
- **GUI**: Tkinter
- **Image Processing**: Pillow, pdf2image

## Development Status

✅ **Core Features Complete** - The application is functional with all major features implemented:
- ✅ Auto-rotation with OCR detection
- ✅ PDF merging with preview
- ✅ Template-based naming system
- ✅ Batch processing
- ✅ Comprehensive UI

See [docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md) for detailed progress and [TODO.md](TODO.md) for remaining tasks.

## License

TBD

## Contributing

Contributions welcome! See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for contribution guidelines and [TODO.md](TODO.md) for areas where help is needed.

## Support

For questions or issues, please open an issue on GitHub.