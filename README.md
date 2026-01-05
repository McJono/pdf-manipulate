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

- [TODO.md](TODO.md) - Complete development roadmap and task breakdown
- User Guide - (Coming soon)
- Developer Documentation - (Coming soon)

## Technology Stack (Planned)

- **Language**: Python 3.8+
- **PDF Processing**: PyPDF2, PyMuPDF (fitz)
- **OCR**: Tesseract, pytesseract
- **GUI**: Tkinter/PyQt6
- **Image Processing**: Pillow, pdf2image

## Development Status

🚧 **In Planning Phase** - See [TODO.md](TODO.md) for detailed implementation plan

## License

TBD

## Contributing

Contributions welcome! See TODO.md for areas where help is needed.

## Support

For questions or issues, please open an issue on GitHub.