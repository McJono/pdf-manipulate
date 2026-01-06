# PDF Manipulate - Development TODO List

## Project Overview
Build a comprehensive PDF manipulation program that automates PDF rotation, provides merging capabilities with preview, and supports intelligent file naming based on configurable templates.

---

## 1. Project Setup & Infrastructure

### 1.1 Technology Stack Selection
- [ ] Choose primary programming language (Python recommended for PDF manipulation)
  - Python: PyPDF2, pdf2image, PyMuPDF (fitz), reportlab
  - Alternative: Node.js with pdf-lib, pdf-poppler
- [ ] Select GUI framework
  - Python: Tkinter (built-in), PyQt5/PyQt6, or Kivy
  - Electron for cross-platform web-based UI
- [ ] Set up dependency management (requirements.txt, package.json, etc.)
- [ ] Initialize version control and .gitignore

### 1.2 Project Structure
- [ ] Create main project directories:
  - `/src` - Source code
  - `/tests` - Unit and integration tests
  - `/config` - Configuration files
  - `/docs` - Documentation
  - `/assets` - Icons, images, resources
- [ ] Set up configuration management system
- [ ] Create logging infrastructure
- [ ] Set up error handling framework

### 1.3 Development Environment
- [ ] Set up virtual environment
- [ ] Install PDF manipulation libraries
- [ ] Install image processing libraries (for previews)
- [ ] Install GUI framework
- [ ] Set up linting/formatting tools (pylint, black, flake8, etc.)
- [ ] Configure IDE/editor

---

## 2. Core PDF Operations Module

### 2.1 PDF Loading & Analysis
- [ ] Create PDF file loader function
- [ ] Implement PDF metadata extraction
- [ ] Develop page count detector
- [ ] Build page dimension analyzer
- [ ] Create PDF validation function (check if file is valid/corrupted)

### 2.2 Orientation Detection
- [ ] Research orientation detection algorithms
  - OCR-based detection (tesseract)
  - Text orientation analysis
  - Image-based detection (visual content analysis)
- [ ] Implement automatic orientation detection for each page
- [ ] Create confidence scoring system for rotation suggestions
- [ ] Handle edge cases (blank pages, image-only pages, etc.)

### 2.3 PDF Rotation
- [ ] Implement single page rotation function (90°, 180°, 270°)
- [ ] Create batch rotation for multiple pages
- [ ] Develop auto-rotation based on detection
- [ ] Implement rotation preview generation
- [ ] Add undo/redo functionality for rotations
- [ ] Ensure metadata preservation during rotation

### 2.4 PDF Merging
- [ ] Implement basic PDF merge functionality
- [ ] Preserve bookmarks/TOC when merging
- [ ] Maintain metadata from source files
- [ ] Handle different page sizes during merge
- [ ] Create merge order management system
- [ ] Add validation for merged output

---

## 3. Auto-Rotation Feature

### 3.1 Detection Engine
- [ ] Implement text-based orientation detection
  - Use OCR to detect text orientation
  - Calculate confidence scores
- [ ] Develop image-based detection (optional, for scanned documents)
- [ ] Create batch processing for multiple files
- [ ] Add progress tracking for batch operations

### 3.2 Manual Override Interface
- [ ] Design UI for reviewing auto-rotation suggestions
- [ ] Create page-by-page review interface
- [ ] Add thumbnail previews showing before/after rotation
- [ ] Implement manual rotation controls (rotate left/right buttons)
- [ ] Add "Accept All" / "Review Each" options
- [ ] Create keyboard shortcuts for quick navigation
  - Arrow keys for navigation
  - R/L for rotate right/left
  - Space/Enter for accept
  - Escape for skip

### 3.3 Batch Processing
- [ ] Implement multi-file auto-rotation queue
- [ ] Add file selection dialog (individual or folder)
- [ ] Create progress bar with status updates
- [ ] Implement pause/resume functionality
- [ ] Add error handling and logging for failed rotations
- [ ] Generate summary report after batch processing

---

## 4. File Merging with Preview

### 4.1 File Selection Interface
- [x] Create file browser/selector
- [x] Display all available PDF files in directory
- [ ] Add drag-and-drop support for adding files
- [x] Implement multi-file selection
- [x] Show file metadata (name, size, page count, date)

### 4.2 Preview System
- [x] Generate thumbnail previews for PDF pages
  - First page as default thumbnail
  - Option to show all pages
- [x] Implement double-click to open full preview
- [x] Create full-page preview modal/window
  - Navigation between pages
  - [ ] Zoom in/out controls
  - Page counter
- [x] Add caching for faster preview loading
- [x] Handle large files efficiently (lazy loading)

### 4.3 Merge Selection & Ordering
- [x] Design click-to-select interface
- [x] Implement selection order tracking
  - Visual indicators (numbers, highlights)
  - Order can be modified by user
- [x] Add configuration option for merge mode:
  - "Click order" - merge in order of clicking
  - "Manual reorder" - allow drag-and-drop reordering after selection
- [x] Create visual merge queue/list
- [x] Add "Clear Selection" and "Remove Item" options
- [x] Implement drag-and-drop reordering in merge queue

### 4.4 Merge Execution
- [x] Create "Merge Selected" button
- [ ] Show preview of merge result before final save
- [x] Implement merge operation with progress indicator
- [x] Add option to delete source files after successful merge
- [x] Generate merge log/history

---

## 5. Intelligent Naming System

### 5.1 Configuration System
- [x] Create config file format (JSON, YAML, or INI)
- [x] Define naming template syntax
  - `{date}` - current date
  - `{date+N}` - date plus N days (e.g., `{date+7}`)
  - `{date-N}` - date minus N days
  - `{name}` - user-provided name
  - `{filename}` - original filename
  - `{counter}` - sequential counter
  - `{timestamp}` - full timestamp
- [x] Implement date formatting options
  - YYYY-MM-DD, DD-MM-YYYY, MM-DD-YYYY, etc.
  - Custom formats
- [x] Add config validation

### 5.2 Naming Template Engine
- [x] Create template parser
- [x] Implement variable substitution
- [x] Add date arithmetic functionality (e.g., +7 days)
- [x] Create preview of generated filename
- [x] Handle invalid characters in filenames
- [x] Add filename sanitization

### 5.3 User Prompts & Labels
- [x] Design prompt interface for name input
- [ ] Create batch naming interface for multiple files
- [x] Add name validation (no conflicts, valid characters)
- [x] Implement filename suggestion system
- [ ] Add history/autocomplete for frequently used names
- [x] Create templates library for common naming patterns
  - Invoice: `Invoice_{date}_{name}.pdf`
  - Receipt: `Receipt_{date+7}_{name}.pdf`
  - Contract: `Contract_{name}_{date}.pdf`

### 5.4 File Saving
- [x] Implement save dialog with name preview
- [x] Add overwrite confirmation
- [x] Create "Save As" functionality
- [ ] Implement batch save with naming template
- [x] Add output directory selection
- [x] Generate save report/log

---

## 6. User Interface Design

### 6.1 Main Window
- [ ] Design main application window layout
- [ ] Create menu bar
  - File: Open, Open Folder, Save, Exit
  - Edit: Preferences, Config
  - Tools: Auto-rotate, Merge, Batch Process
  - Help: Documentation, About
- [ ] Add toolbar with quick access buttons
- [ ] Implement status bar for messages/progress

### 6.2 Workflow Screens
- [ ] **Screen 1: Auto-Rotation**
  - File list with rotation status
  - Preview pane (before/after)
  - Manual override controls
  - Progress indicator
- [ ] **Screen 2: File Selection & Preview**
  - Grid/list view of PDF files
  - Thumbnail previews
  - Selection indicators
  - Merge queue panel
- [ ] **Screen 3: Merge Preview**
  - Preview of merge result
  - Page order visualization
  - Edit/reorder options
- [ ] **Screen 4: Naming & Save**
  - Template selector
  - Name preview
  - Input fields for variables
  - Save location selector

### 6.3 Dialogs & Modals
- [ ] File picker dialog
- [ ] Settings/preferences dialog
- [ ] Preview modal for double-click
- [ ] Error/warning dialogs
- [ ] Progress dialog for long operations
- [ ] About/help dialog

### 6.4 User Experience Enhancements
- [ ] Add keyboard shortcuts throughout
- [ ] Implement tooltips for all controls
- [ ] Add context menus (right-click)
- [ ] Create responsive layouts
- [ ] Add dark/light theme support
- [ ] Implement accessibility features

---

## 7. Configuration Management

### 7.1 Config File Structure
- [ ] Create default configuration file
- [ ] Define all configurable settings:
  ```json
  {
    "auto_rotation": {
      "enabled": true,
      "confidence_threshold": 0.8,
      "ocr_language": "eng"
    },
    "merge": {
      "selection_mode": "click_order",
      "preserve_bookmarks": true
    },
    "naming": {
      "templates": [
        "{date+7}_{name}",
        "{name}_{date}",
        "Invoice_{date}_{name}"
      ],
      "date_format": "YYYY-MM-DD",
      "default_template": "{date+7}_{name}"
    },
    "ui": {
      "theme": "light",
      "preview_quality": "medium"
    }
  }
  ```
- [ ] Implement config loader
- [ ] Create config validator
- [ ] Add config editor UI

### 7.2 Settings Persistence
- [ ] Save user preferences
- [ ] Remember window size/position
- [ ] Store recent files/directories
- [ ] Save custom naming templates

---

## 8. Testing Strategy

### 8.1 Unit Tests
- [ ] Test PDF loading functions
- [ ] Test rotation detection accuracy
- [ ] Test rotation operations
- [ ] Test merge functionality
- [ ] Test naming template engine
- [ ] Test config parsing

### 8.2 Integration Tests
- [ ] Test complete auto-rotation workflow
- [ ] Test merge workflow end-to-end
- [ ] Test naming and saving workflow
- [ ] Test error handling scenarios

### 8.3 User Acceptance Testing
- [ ] Create test PDFs with various orientations
- [ ] Test with different PDF versions
- [ ] Test with large files (100+ pages)
- [ ] Test with corrupted/invalid PDFs
- [ ] Test batch processing with many files
- [ ] Verify merge quality and integrity

### 8.4 Performance Testing
- [ ] Benchmark rotation speed
- [ ] Test preview generation performance
- [ ] Measure memory usage with large files
- [ ] Test concurrent operation handling

---

## 9. Error Handling & Logging

### 9.1 Error Handling
- [ ] Implement try-catch for all file operations
- [ ] Create user-friendly error messages
- [ ] Add recovery mechanisms for common errors
- [ ] Implement graceful degradation
- [ ] Create error logging system

### 9.2 Logging
- [ ] Set up logging framework
- [ ] Log all file operations
- [ ] Log errors with stack traces
- [ ] Create rotating log files
- [ ] Add log viewer in application

### 9.3 Validation
- [ ] Validate input files (are they PDFs?)
- [ ] Validate file permissions (read/write access)
- [ ] Validate disk space before saving
- [ ] Validate configuration values
- [ ] Check for duplicate filenames

---

## 10. Documentation

### 10.1 User Documentation
- [ ] Create user manual/guide
- [ ] Write quick start guide
- [ ] Document naming template syntax
- [ ] Create FAQ section
- [ ] Add troubleshooting guide
- [ ] Create video tutorials (optional)

### 10.2 Developer Documentation
- [ ] Document code architecture
- [ ] Create API documentation
- [ ] Write contribution guidelines
- [ ] Document build/deployment process
- [ ] Create development setup guide

### 10.3 In-App Help
- [ ] Add help tooltips
- [ ] Create contextual help system
- [ ] Add "Getting Started" wizard
- [ ] Include example templates

---

## 11. Deployment & Distribution

### 11.1 Packaging
- [ ] Create standalone executable (PyInstaller, py2exe, etc.)
- [ ] Include all dependencies
- [ ] Add application icon
- [ ] Create installer
  - Windows: NSIS, Inno Setup
  - macOS: DMG
  - Linux: AppImage, .deb, .rpm

### 11.2 Platform Support
- [ ] Test on Windows 10/11
- [ ] Test on macOS (latest versions)
- [ ] Test on Linux (Ubuntu, Fedora)
- [ ] Ensure cross-platform compatibility

### 11.3 Distribution
- [ ] Create GitHub releases
- [ ] Write release notes
- [ ] Create download page
- [ ] Set up update mechanism (optional)

---

## 12. Future Enhancements (Post-MVP)

### 12.1 Advanced Features
- [ ] PDF editing (add text, annotations)
- [ ] Page extraction/deletion
- [ ] PDF splitting
- [ ] Watermark addition
- [ ] Password protection/encryption
- [ ] PDF compression
- [ ] OCR for searchable PDFs

### 12.2 Automation
- [ ] Watch folder for automatic processing
- [ ] Scheduled batch processing
- [ ] Command-line interface for scripting
- [ ] API for integration with other tools

### 12.3 Cloud Integration
- [ ] Save to cloud storage (Dropbox, Google Drive, OneDrive)
- [ ] Load from cloud storage
- [ ] Cloud-based preview generation

### 12.4 Collaboration
- [ ] Share naming templates
- [ ] Export/import configurations
- [ ] Multi-user support

---

## Development Phases

### Phase 1: Foundation (Weeks 1-2)
- Project setup
- Core PDF operations
- Basic rotation functionality

### Phase 2: Auto-Rotation (Weeks 3-4)
- Orientation detection
- Auto-rotation with manual override
- Batch processing

### Phase 3: Merge & Preview (Weeks 5-6)
- File selection interface
- Preview system
- Merge functionality

### Phase 4: Naming System (Week 7)
- Template engine
- Config management
- User prompts

### Phase 5: Polish & Testing (Weeks 8-9)
- UI refinement
- Comprehensive testing
- Bug fixes
- Documentation

### Phase 6: Deployment (Week 10)
- Packaging
- Distribution
- Release

---

## Success Criteria

- [ ] Application successfully auto-rotates PDFs with 90%+ accuracy
- [ ] Manual override is intuitive and efficient
- [ ] Merge functionality preserves PDF quality and metadata
- [ ] Preview system loads quickly (< 2 seconds for typical PDFs)
- [ ] Naming templates work correctly with date arithmetic
- [ ] Application is stable and handles errors gracefully
- [ ] User interface is intuitive and requires minimal training
- [ ] Performance is acceptable for files up to 100 pages
- [ ] Cross-platform compatibility is verified

---

## Resources & References

### Libraries & Tools
- **PDF Manipulation**: PyPDF2, PyMuPDF (fitz), pdf2image
- **OCR**: tesseract-ocr, pytesseract
- **GUI**: Tkinter, PyQt6, Electron
- **Image Processing**: Pillow (PIL), OpenCV
- **Configuration**: configparser, PyYAML, python-dotenv

### Documentation Links
- PyPDF2: https://pypdf2.readthedocs.io/
- PyMuPDF: https://pymupdf.readthedocs.io/
- Tesseract: https://github.com/tesseract-ocr/tesseract
- Tkinter: https://docs.python.org/3/library/tkinter.html
- PyQt6: https://www.riverbankcomputing.com/static/Docs/PyQt6/

---

## Notes

- Prioritize user experience and workflow efficiency
- Ensure all file operations are non-destructive (keep originals unless explicitly deleted)
- Implement comprehensive error handling - PDF files can be unpredictable
- Consider performance implications for large files and batch operations
- Make the application accessible to non-technical users
- Keep the codebase maintainable and well-documented
