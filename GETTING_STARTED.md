# Getting Started Guide - PDF Manipulate

## Quick Start for Developers

This guide helps you get started with developing the PDF Manipulate application.

---

## Project Documentation

The project has comprehensive planning documentation:

1. **[README.md](README.md)** - Project overview and features
2. **[TODO.md](TODO.md)** - Detailed task breakdown and implementation checklist
3. **[ROADMAP.md](ROADMAP.md)** - Development timeline and milestones
4. **[USER_STORIES.md](USER_STORIES.md)** - User personas and feature requirements
5. **[NAMING_TEMPLATES.md](NAMING_TEMPLATES.md)** - Naming template system reference
6. **[config.example.json](config.example.json)** - Example configuration file

---

## Recommended Reading Order

### For New Contributors
1. Start with **README.md** - understand what we're building
2. Read **USER_STORIES.md** - understand why we're building it
3. Review **ROADMAP.md** - see the development plan
4. Dive into **TODO.md** - find tasks to work on

### For Project Managers
1. **README.md** - project overview
2. **ROADMAP.md** - timeline and milestones
3. **USER_STORIES.md** - requirements and priorities
4. **TODO.md** - detailed work breakdown

### For End Users (Future)
1. **README.md** - what the application does
2. **NAMING_TEMPLATES.md** - how to use naming templates

---

## Development Setup (When Implementation Starts)

### Prerequisites
```bash
# Install Python 3.8 or higher
python --version

# Install pip
pip --version
```

### Initial Setup
```bash
# Clone repository
git clone https://github.com/McJono/pdf-manipulate.git
cd pdf-manipulate

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies (when requirements.txt exists)
pip install -r requirements.txt
```

### Configuration
```bash
# Copy example config
cp config.example.json config.json

# Edit config.json with your preferences
```

---

## Project Structure (Planned)

```
pdf-manipulate/
├── README.md                 # Project overview
├── TODO.md                   # Development tasks
├── ROADMAP.md               # Timeline and milestones
├── USER_STORIES.md          # Requirements and personas
├── NAMING_TEMPLATES.md      # Template system reference
├── config.example.json      # Example configuration
├── requirements.txt         # Python dependencies (to be created)
├── setup.py                 # Package setup (to be created)
├── .gitignore              # Git ignore rules (to be created)
│
├── src/                     # Source code (to be created)
│   ├── __init__.py
│   ├── main.py             # Application entry point
│   ├── pdf_operations/     # PDF manipulation module
│   │   ├── __init__.py
│   │   ├── loader.py       # PDF loading
│   │   ├── rotation.py     # Rotation detection and operations
│   │   └── merger.py       # PDF merging
│   ├── ui/                 # User interface
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── rotation_ui.py
│   │   ├── merge_ui.py
│   │   └── naming_ui.py
│   ├── naming/             # Naming template system
│   │   ├── __init__.py
│   │   ├── parser.py       # Template parser
│   │   └── variables.py    # Variable handlers
│   ├── config/             # Configuration management
│   │   ├── __init__.py
│   │   └── manager.py
│   └── utils/              # Utilities
│       ├── __init__.py
│       ├── logger.py       # Logging setup
│       └── validators.py   # Input validation
│
├── tests/                   # Test suite (to be created)
│   ├── __init__.py
│   ├── test_rotation.py
│   ├── test_merger.py
│   ├── test_naming.py
│   └── fixtures/           # Test PDF files
│
├── docs/                    # Additional documentation (to be created)
│   ├── installation.md
│   ├── user_guide.md
│   └── api_reference.md
│
└── assets/                  # Resources (to be created)
    ├── icons/
    └── examples/
```

---

## Key Technologies (Recommended)

### Core Libraries
- **PyPDF2** or **PyMuPDF (fitz)** - PDF manipulation
- **pdf2image** - PDF to image conversion for previews
- **pytesseract** - OCR for orientation detection
- **Pillow (PIL)** - Image processing

### GUI Framework Options
- **Tkinter** - Built-in, simple, cross-platform
- **PyQt6** - More features, professional look
- **Kivy** - Modern, touch-friendly

### Development Tools
- **pytest** - Testing framework
- **black** - Code formatter
- **pylint** - Code linter
- **mypy** - Type checking

---

## Development Workflow

### 1. Choose a Task
Browse **TODO.md** and pick a task:
- Start with Phase 1 (Foundation) tasks if new to project
- Look for tasks marked with your skill level
- Check if task has dependencies

### 2. Create Feature Branch
```bash
git checkout -b feature/task-name
```

### 3. Implement Feature
- Follow the task checklist in TODO.md
- Write tests for new functionality
- Keep commits small and focused

### 4. Test Your Changes
```bash
# Run tests
pytest

# Run linter
pylint src/

# Format code
black src/
```

### 5. Submit Pull Request
- Reference the TODO.md task
- Include before/after screenshots for UI changes
- Update documentation if needed

---

## Coding Standards

### Python Style
- Follow PEP 8
- Use type hints
- Write docstrings for all functions/classes
- Maximum line length: 100 characters

### Example
```python
from typing import List, Optional
from pathlib import Path

def rotate_pdf(
    pdf_path: Path,
    rotation_angle: int,
    pages: Optional[List[int]] = None
) -> bool:
    """
    Rotate specified pages in a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        rotation_angle: Angle to rotate (90, 180, or 270)
        pages: List of page numbers to rotate (None for all pages)
        
    Returns:
        True if successful, False otherwise
        
    Raises:
        ValueError: If rotation_angle is not 90, 180, or 270
        FileNotFoundError: If pdf_path does not exist
    """
    # Implementation here
    pass
```

### Naming Conventions
- Classes: `PascalCase` (e.g., `PDFRotator`)
- Functions/Methods: `snake_case` (e.g., `rotate_page`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_FILE_SIZE`)
- Private: prefix with `_` (e.g., `_internal_method`)

---

## Testing Guidelines

### Test Structure
```python
import pytest
from src.pdf_operations.rotation import detect_orientation

def test_detect_orientation_normal():
    """Test orientation detection on normally oriented page."""
    result = detect_orientation("tests/fixtures/normal.pdf", page=0)
    assert result.angle == 0
    assert result.confidence > 0.8

def test_detect_orientation_upside_down():
    """Test orientation detection on upside-down page."""
    result = detect_orientation("tests/fixtures/upside_down.pdf", page=0)
    assert result.angle == 180
    assert result.confidence > 0.8
```

### Coverage Goal
- Aim for 80%+ code coverage
- Focus on critical paths first
- Test edge cases and error conditions

---

## Debugging Tips

### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Common Issues
1. **PDF won't load**: Check file permissions and PDF version
2. **OCR not working**: Verify Tesseract installation
3. **Preview slow**: Reduce preview quality in config
4. **Memory issues**: Process PDFs in chunks

---

## Performance Considerations

### Optimization Priorities
1. **Preview generation** - Most frequent operation
2. **Batch processing** - Can process many files
3. **Merge operation** - Should be fast for user experience

### Best Practices
- Use lazy loading for large PDFs
- Cache thumbnails aggressively
- Process operations in background threads
- Show progress indicators for long operations

---

## Contributing

### First-Time Contributors
1. Read all documentation
2. Set up development environment
3. Start with "good first issue" tasks
4. Ask questions in issues/discussions

### Regular Contributors
1. Pick tasks from TODO.md
2. Update task status as you work
3. Write comprehensive tests
4. Keep documentation in sync with code

---

## Getting Help

### Resources
- **TODO.md** - Task details and acceptance criteria
- **USER_STORIES.md** - Feature requirements and use cases
- **NAMING_TEMPLATES.md** - Template system specification

### Community
- Open an issue for bugs
- Start a discussion for questions
- Submit PRs for improvements

---

## Next Steps

1. ✅ Review all documentation
2. ⏳ Wait for Phase 1 implementation to begin
3. ⏳ Set up development environment (when Phase 1 starts)
4. ⏳ Choose first task from TODO.md
5. ⏳ Start coding!

---

## FAQ

### Q: Can I use JavaScript instead of Python?
A: While Python is recommended for its excellent PDF libraries, Node.js with pdf-lib is also viable. Discuss in an issue first.

### Q: What's the minimum Python version?
A: Python 3.8+ is recommended for type hints and modern features.

### Q: Do I need to implement everything in TODO.md?
A: No! Pick tasks that interest you. The TODO is a complete roadmap, but contributions of any size are welcome.

### Q: How do I test without real PDF files?
A: We'll create test fixtures. You can also generate simple PDFs using PyPDF2 or reportlab.

### Q: What if I want to add a feature not in the plan?
A: Great! Open an issue to discuss it first. We want to keep scope manageable for v1.0, but good ideas are always welcome.

### Q: Is there a chat/discussion board?
A: Use GitHub Discussions for general questions and GitHub Issues for specific bugs/features.

---

## License

TBD - Check LICENSE file when available.

---

**Ready to contribute?** Start with [TODO.md](TODO.md) and pick your first task!
