# Contributing to PDF Manipulate

Thank you for your interest in contributing to PDF Manipulate! This document provides guidelines and instructions for contributing to the project.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [How to Contribute](#how-to-contribute)
5. [Code Guidelines](#code-guidelines)
6. [Testing](#testing)
7. [Pull Request Process](#pull-request-process)
8. [Issue Reporting](#issue-reporting)
9. [Development Workflow](#development-workflow)

---

## Code of Conduct

### Our Standards

We are committed to providing a welcoming and inspiring community for all. Examples of behavior that contributes to creating a positive environment include:

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

Examples of unacceptable behavior include:

- The use of sexualized language or imagery
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by opening an issue or contacting the project maintainers. All complaints will be reviewed and investigated.

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic knowledge of Python and PDF manipulation
- Familiarity with GitHub workflow

### First-Time Contributors

If you're new to open source contribution:

1. Read the [README.md](README.md) to understand the project
2. Check out [GETTING_STARTED.md](docs/GETTING_STARTED.md) for usage
3. Browse [existing issues](https://github.com/McJono/pdf-manipulate/issues)
4. Look for issues labeled `good first issue` or `help wanted`

---

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/pdf-manipulate.git
cd pdf-manipulate

# Add upstream remote
git remote add upstream https://github.com/McJono/pdf-manipulate.git
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Verify activation
which python  # Should point to venv/bin/python
```

### 3. Install Dependencies

```bash
# Install all dependencies including development tools
pip install -r requirements.txt

# Verify installation
python3 verify_installation.py
```

### 4. Install Development Tools

```bash
# Linters and formatters
pip install black pylint mypy flake8

# Testing tools
pip install pytest pytest-cov

# Pre-commit hooks (optional but recommended)
pip install pre-commit
pre-commit install
```

### 5. Verify Setup

```bash
# Run tests
pytest tests/

# Check code style
black --check src/ tests/

# Run linter
pylint src/

# Type checking
mypy src/
```

---

## How to Contribute

### Types of Contributions

We welcome various types of contributions:

1. **Bug Fixes** - Fix issues and improve stability
2. **New Features** - Implement new functionality
3. **Documentation** - Improve or add documentation
4. **Tests** - Add or improve test coverage
5. **Performance** - Optimize code performance
6. **UI/UX** - Improve user interface and experience

### Finding Work

1. **Browse Issues:** Check [GitHub Issues](https://github.com/McJono/pdf-manipulate/issues)
2. **Check TODO.md:** Review [TODO.md](TODO.md) for planned features
3. **Ask First:** For major changes, open an issue first to discuss

### Good First Issues

Look for issues labeled:
- `good first issue` - Suitable for newcomers
- `help wanted` - We need community help
- `documentation` - Documentation improvements
- `bug` - Bug fixes needed

---

## Code Guidelines

### Python Style

We follow PEP 8 with some modifications:

```python
# Use 4 spaces for indentation
# Maximum line length: 100 characters (not 80)
# Use double quotes for strings (unless single quotes avoid escaping)

# Good
def process_pdf(file_path: str, output_dir: str) -> bool:
    """
    Process a PDF file and save to output directory.
    
    Args:
        file_path: Path to input PDF file
        output_dir: Directory for output file
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Implementation here
        return True
    except Exception as e:
        logger.error(f"Failed to process PDF: {e}")
        return False
```

### Code Formatting

Use **Black** for automatic formatting:

```bash
# Format entire codebase
black src/ tests/

# Check without modifying
black --check src/ tests/

# Format specific file
black src/utils/validators.py
```

### Type Hints

Use type hints for all function signatures:

```python
from typing import List, Dict, Optional, Tuple

def merge_pdfs(
    file_paths: List[str],
    output_path: str,
    preserve_bookmarks: bool = True
) -> bool:
    """Merge multiple PDF files."""
    pass

def load_config(path: Optional[str] = None) -> Dict[str, any]:
    """Load configuration from file."""
    pass
```

### Documentation

#### Docstrings

Use Google-style docstrings:

```python
def rotate_page(pdf_path: str, page_num: int, angle: int) -> bool:
    """
    Rotate a specific page in a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        page_num: Page number (0-indexed)
        angle: Rotation angle (0, 90, 180, 270)
    
    Returns:
        True if rotation successful, False otherwise
    
    Raises:
        ValueError: If angle is not a multiple of 90
        FileNotFoundError: If PDF file doesn't exist
    
    Example:
        >>> rotate_page("document.pdf", 0, 90)
        True
    """
    pass
```

#### Comments

- Use comments sparingly - code should be self-documenting
- Explain **why**, not **what**
- Keep comments up to date with code

```python
# Good - explains why
# Use OCR with higher threshold for scanned documents
confidence_threshold = 0.9 if is_scanned else 0.7

# Bad - explains what (obvious from code)
# Set x to 5
x = 5
```

### Error Handling

```python
from src.utils.logger import logger

def process_file(file_path: str) -> bool:
    """Process a PDF file with proper error handling."""
    try:
        # Validate input
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return False
        
        # Process file
        result = do_processing(file_path)
        logger.info(f"Successfully processed: {file_path}")
        return result
        
    except ValueError as e:
        logger.error(f"Invalid value: {e}")
        return False
    except Exception as e:
        logger.exception(f"Unexpected error processing {file_path}: {e}")
        return False
```

### Logging

Use the centralized logging system:

```python
from src.utils.logger import logger

# Different log levels
logger.debug("Detailed debugging information")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error message")
logger.exception("Exception with traceback")  # Use in except blocks
```

---

## Testing

### Writing Tests

All new features must include tests:

```python
# tests/test_new_feature.py
import pytest
from src.module.feature import new_function

class TestNewFeature:
    """Tests for new feature."""
    
    def test_basic_functionality(self):
        """Test basic use case."""
        result = new_function("input")
        assert result == "expected_output"
    
    def test_edge_cases(self):
        """Test edge cases."""
        assert new_function("") == ""
        assert new_function(None) is None
    
    def test_error_handling(self):
        """Test error conditions."""
        with pytest.raises(ValueError):
            new_function("invalid_input")
```

### Test Categories

Use pytest markers:

```python
@pytest.mark.unit
def test_parser():
    """Unit test for parser."""
    pass

@pytest.mark.integration
def test_complete_workflow():
    """Integration test for complete workflow."""
    pass

@pytest.mark.slow
def test_large_file_processing():
    """Slow test with large files."""
    pass
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_naming.py

# Run specific test
pytest tests/test_naming.py::TestTemplateParser::test_date_variable

# Run with coverage
pytest --cov=src tests/

# Skip slow tests
pytest -m "not slow"

# Run only integration tests
pytest -m integration
```

### Test Coverage

Aim for:
- 80%+ overall coverage
- 90%+ for critical modules (PDF operations, naming)
- 100% for utility functions

Check coverage:

```bash
pytest --cov=src --cov-report=html tests/
# Open htmlcov/index.html in browser
```

---

## Pull Request Process

### Before Submitting

1. **Create a branch:**
   ```bash
   git checkout -b feature/my-new-feature
   # or
   git checkout -b fix/issue-123
   ```

2. **Make your changes:**
   - Write clean, documented code
   - Follow style guidelines
   - Add tests

3. **Run quality checks:**
   ```bash
   # Format code
   black src/ tests/
   
   # Run linter
   pylint src/ tests/
   
   # Type check
   mypy src/
   
   # Run tests
   pytest tests/
   ```

4. **Update documentation:**
   - Update docstrings
   - Update README.md if needed
   - Update relevant .md files in docs/
   - Update TODO.md if completing items

5. **Commit changes:**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   # or
   git commit -m "fix: resolve issue #123"
   ```

### Commit Message Format

Use conventional commits:

```
<type>: <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `style`: Code style changes (formatting, etc.)
- `perf`: Performance improvements
- `chore`: Maintenance tasks

**Examples:**
```
feat: add zoom controls to preview dialog

fix: resolve merge failure with corrupted PDFs (#123)

docs: update troubleshooting guide with Linux issues

test: add integration tests for auto-rotation workflow
```

### Submitting Pull Request

1. **Push to your fork:**
   ```bash
   git push origin feature/my-new-feature
   ```

2. **Open Pull Request on GitHub:**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill in PR template

3. **PR Description should include:**
   - Clear description of changes
   - Related issue numbers (e.g., "Fixes #123")
   - Testing performed
   - Screenshots (for UI changes)
   - Breaking changes (if any)

4. **Wait for review:**
   - Respond to feedback
   - Make requested changes
   - Push updates to same branch

### PR Checklist

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No breaking changes (or documented if necessary)
- [ ] Commits are clean and descriptive
- [ ] PR description is clear and complete

---

## Issue Reporting

### Before Opening an Issue

1. **Search existing issues** - Someone may have reported it already
2. **Check FAQ and troubleshooting** - Solution might be documented
3. **Verify with latest version** - Update and test again

### Bug Reports

Include:

```markdown
**Description:**
Clear description of the bug

**Steps to Reproduce:**
1. Step one
2. Step two
3. Step three

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Environment:**
- OS: Ubuntu 22.04
- Python: 3.10.5
- PDF Manipulate: v1.0.0

**Logs:**
```
Paste relevant logs here
```

**Screenshots:**
[If applicable]
```

### Feature Requests

Include:

```markdown
**Feature Description:**
Clear description of proposed feature

**Use Case:**
Why is this feature needed?

**Proposed Solution:**
How should it work?

**Alternatives Considered:**
Other approaches you've thought about

**Additional Context:**
Any other relevant information
```

---

## Development Workflow

### Branching Strategy

- `main` - Stable, production-ready code
- `develop` - Integration branch for features
- `feature/*` - New features
- `fix/*` - Bug fixes
- `docs/*` - Documentation updates

### Development Cycle

1. **Sync with upstream:**
   ```bash
   git checkout main
   git fetch upstream
   git merge upstream/main
   git push origin main
   ```

2. **Create feature branch:**
   ```bash
   git checkout -b feature/my-feature
   ```

3. **Develop and test:**
   - Write code
   - Write tests
   - Run quality checks

4. **Keep branch updated:**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

5. **Submit PR:**
   - Push to your fork
   - Open pull request
   - Respond to reviews

### Code Review

When reviewing PRs:

- Be constructive and respectful
- Focus on code quality, not personal preferences
- Suggest improvements with examples
- Approve when satisfied with changes

When receiving reviews:

- Don't take feedback personally
- Ask questions if unclear
- Make requested changes promptly
- Thank reviewers for their time

---

## Release Process

(For maintainers)

1. Update version in `setup.py`
2. Update `CHANGELOG.md`
3. Create release branch
4. Tag release: `git tag -a v1.0.0 -m "Release v1.0.0"`
5. Push tag: `git push origin v1.0.0`
6. Create GitHub release
7. Update documentation

---

## Getting Help

### For Development Questions:

1. Check [documentation](docs/)
2. Search [existing issues](https://github.com/McJono/pdf-manipulate/issues)
3. Open a discussion or issue
4. Ask in pull request comments

### Resources:

- **README:** [README.md](README.md)
- **Getting Started:** [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)
- **FAQ:** [docs/FAQ.md](docs/FAQ.md)
- **Troubleshooting:** [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- **TODO List:** [TODO.md](TODO.md)

---

## Recognition

Contributors are recognized in:
- GitHub contributors page
- Release notes
- CONTRIBUTORS.md file (coming soon)

Significant contributions may be highlighted in release announcements.

---

## Questions?

If you have questions about contributing:

1. Read through this guide
2. Check existing documentation
3. Open an issue with the `question` label
4. We're here to help!

Thank you for contributing to PDF Manipulate! 🎉
