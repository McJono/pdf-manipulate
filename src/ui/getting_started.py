"""
Getting Started wizard for new users.

Provides a step-by-step introduction to the application features
and helps users get started quickly.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ..config.preferences import preferences
from ..utils.logger import logger


class GettingStartedWizard(tk.Toplevel):
    """
    Multi-step wizard to introduce new users to the application.
    
    Shows key features and basic workflow.
    """
    
    def __init__(self, parent):
        """
        Initialize getting started wizard.
        
        Args:
            parent: Parent window
        """
        super().__init__(parent)
        
        self.title("Getting Started - PDF Manipulate")
        self.geometry("700x500")
        self.transient(parent)
        self.resizable(False, False)
        
        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.winfo_screenheight() // 2) - (500 // 2)
        self.geometry(f"700x500+{x}+{y}")
        
        self.current_page = 0
        self.pages = [
            self._create_welcome_page,
            self._create_features_page,
            self._create_auto_rotation_page,
            self._create_merge_page,
            self._create_naming_page,
            self._create_complete_page,
        ]
        
        self._create_widgets()
        self._show_page(0)
    
    def _create_widgets(self):
        """Create wizard widgets"""
        # Content frame
        self.content_frame = ttk.Frame(self, padding=30)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Navigation frame
        self.nav_frame = ttk.Frame(self, padding=10)
        self.nav_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Page indicator
        self.page_indicator = ttk.Label(self.nav_frame, text="")
        self.page_indicator.pack(side=tk.LEFT, padx=10)
        
        # Buttons
        self.btn_prev = ttk.Button(
            self.nav_frame,
            text="← Previous",
            command=self._prev_page,
            state=tk.DISABLED,
            width=12
        )
        self.btn_prev.pack(side=tk.RIGHT, padx=5)
        
        self.btn_next = ttk.Button(
            self.nav_frame,
            text="Next →",
            command=self._next_page,
            width=12
        )
        self.btn_next.pack(side=tk.RIGHT, padx=5)
        
        # Don't show again checkbox
        self.dont_show_var = tk.BooleanVar(value=False)
        self.dont_show_check = ttk.Checkbutton(
            self.nav_frame,
            text="Don't show this again",
            variable=self.dont_show_var
        )
        self.dont_show_check.pack(side=tk.LEFT, padx=20)
    
    def _show_page(self, page_num):
        """Show specific page"""
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create new page
        self.current_page = page_num
        self.pages[page_num]()
        
        # Update navigation
        self._update_navigation()
    
    def _update_navigation(self):
        """Update navigation buttons and page indicator"""
        # Update page indicator
        self.page_indicator.config(
            text=f"Step {self.current_page + 1} of {len(self.pages)}"
        )
        
        # Update previous button
        if self.current_page == 0:
            self.btn_prev.config(state=tk.DISABLED)
        else:
            self.btn_prev.config(state=tk.NORMAL)
        
        # Update next button
        if self.current_page == len(self.pages) - 1:
            self.btn_next.config(text="Finish", command=self._finish)
        else:
            self.btn_next.config(text="Next →", command=self._next_page)
    
    def _next_page(self):
        """Go to next page"""
        if self.current_page < len(self.pages) - 1:
            self._show_page(self.current_page + 1)
    
    def _prev_page(self):
        """Go to previous page"""
        if self.current_page > 0:
            self._show_page(self.current_page - 1)
    
    def _finish(self):
        """Finish wizard"""
        # Save preference if user checked "don't show again"
        if self.dont_show_var.get():
            preferences.set("ui_state.show_getting_started", False)
            preferences.save()
            logger.info("User disabled getting started wizard")
        
        self.destroy()
    
    def _create_welcome_page(self):
        """Create welcome page"""
        # Title
        title = ttk.Label(
            self.content_frame,
            text="Welcome to PDF Manipulate!",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=(20, 10))
        
        # Subtitle
        subtitle = ttk.Label(
            self.content_frame,
            text="Your intelligent PDF manipulation assistant",
            font=("Arial", 12)
        )
        subtitle.pack(pady=(0, 30))
        
        # Welcome text
        welcome_text = tk.Text(
            self.content_frame,
            wrap=tk.WORD,
            height=12,
            font=("Arial", 10),
            relief=tk.FLAT,
            bg=self.cget('bg')
        )
        welcome_text.pack(fill=tk.BOTH, expand=True, pady=20)
        
        content = """This wizard will guide you through the main features of PDF Manipulate.

PDF Manipulate helps you:

• Automatically detect and rotate incorrectly oriented pages
• Merge multiple PDF files with live previews
• Use smart naming templates with date arithmetic
• Manage your PDF workflow efficiently

The application is designed to save you time and make PDF manipulation tasks easy and intuitive.

Click "Next" to learn about the key features."""
        
        welcome_text.insert("1.0", content)
        welcome_text.config(state=tk.DISABLED)
    
    def _create_features_page(self):
        """Create features overview page"""
        title = ttk.Label(
            self.content_frame,
            text="Key Features",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=(10, 20))
        
        # Feature list
        features_frame = ttk.Frame(self.content_frame)
        features_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        features = [
            ("🔄 Auto-Rotation", 
             "Detect and rotate pages using OCR technology.\n"
             "Review suggestions before applying."),
            
            ("🔗 PDF Merging", 
             "Select and merge PDFs in any order.\n"
             "Preview pages before merging."),
            
            ("📝 Smart Naming", 
             "Use templates with date arithmetic.\n"
             "Example: {date+7}_{name}.pdf"),
            
            ("⚙️ Preferences", 
             "Customize settings to your workflow.\n"
             "Save window positions and recent files."),
        ]
        
        for i, (title_text, desc) in enumerate(features):
            # Feature frame
            feature_frame = ttk.LabelFrame(
                features_frame,
                text=title_text,
                padding=10
            )
            feature_frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(
                feature_frame,
                text=desc,
                justify=tk.LEFT
            ).pack(anchor=tk.W)
    
    def _create_auto_rotation_page(self):
        """Create auto-rotation feature page"""
        title = ttk.Label(
            self.content_frame,
            text="Auto-Rotation Feature",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=(10, 20))
        
        text = tk.Text(
            self.content_frame,
            wrap=tk.WORD,
            height=15,
            font=("Arial", 10),
            relief=tk.FLAT,
            bg=self.cget('bg')
        )
        text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        content = """HOW AUTO-ROTATION WORKS:

1. Add Files
   Click "Add Files" or "Add Folder" to select PDFs

2. Automatic Detection
   The application scans each page using OCR to detect orientation
   Confidence scores show how certain the detection is

3. Review Options
   • Accept All - Process all files with suggested rotations
   • Review Each - Go through pages one by one
   • Manual Override - Rotate specific pages manually

4. Process
   Apply rotations and save to output directory

KEYBOARD SHORTCUTS:
   Ctrl+R - Rotate right
   Ctrl+Shift+R - Rotate left
   Ctrl+Z - Undo
   Ctrl+Y - Redo

Access: Tools → Auto-Rotate (Ctrl+Alt+R)"""
        
        text.insert("1.0", content)
        text.config(state=tk.DISABLED)
    
    def _create_merge_page(self):
        """Create merge feature page"""
        title = ttk.Label(
            self.content_frame,
            text="PDF Merging Feature",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=(10, 20))
        
        text = tk.Text(
            self.content_frame,
            wrap=tk.WORD,
            height=15,
            font=("Arial", 10),
            relief=tk.FLAT,
            bg=self.cget('bg')
        )
        text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        content = """HOW TO MERGE PDFs:

1. Open Merge Screen
   Tools → Merge PDFs (Ctrl+M)

2. Select Files
   • Click "Open Folder" to browse PDFs
   • Double-click files to add to merge queue

3. Preview Pages
   • Click a file to see thumbnail
   • Double-click for full-page preview

4. Arrange Order
   • Use "Move Up/Down" buttons to reorder
   • Or drag files in the queue

5. Merge & Name
   • Click "Merge Selected"
   • Choose output directory
   • Use naming templates for smart file names

FEATURES:
   ✓ Preserves bookmarks and metadata
   ✓ Handles different page sizes
   ✓ Live preview before merging"""
        
        text.insert("1.0", content)
        text.config(state=tk.DISABLED)
    
    def _create_naming_page(self):
        """Create naming templates page"""
        title = ttk.Label(
            self.content_frame,
            text="Smart Naming Templates",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=(10, 20))
        
        text = tk.Text(
            self.content_frame,
            wrap=tk.WORD,
            height=15,
            font=("Arial", 10),
            relief=tk.FLAT,
            bg=self.cget('bg')
        )
        text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        content = """NAMING TEMPLATE SYNTAX:

Available Variables:
   {date}       - Current date (2026-01-06)
   {date+N}     - Date plus N days ({date+7} = 2026-01-13)
   {date-N}     - Date minus N days ({date-30} = 2025-12-07)
   {name}       - User-provided name
   {filename}   - Original filename
   {timestamp}  - Full timestamp
   {counter}    - Sequential counter (001, 002, ...)

Template Examples:

Invoice_{date+7}_{name}.pdf
   → Invoice_2026-01-13_ClientA.pdf

{date}_Report_{counter}.pdf
   → 2026-01-06_Report_001.pdf

Contract_{name}_{date}.pdf
   → Contract_NewClient_2026-01-06.pdf

Configure Templates:
   Edit → Settings → Naming tab
   Add custom templates for quick access"""
        
        text.insert("1.0", content)
        text.config(state=tk.DISABLED)
    
    def _create_complete_page(self):
        """Create completion page"""
        title = ttk.Label(
            self.content_frame,
            text="You're All Set!",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=(30, 20))
        
        text = tk.Text(
            self.content_frame,
            wrap=tk.WORD,
            height=12,
            font=("Arial", 10),
            relief=tk.FLAT,
            bg=self.cget('bg')
        )
        text.pack(fill=tk.BOTH, expand=True, pady=20)
        
        content = """Quick Start Tips:

1. Press F1 anytime for help
2. Use Ctrl+O to quickly open files
3. View logs: Help → View Logs
4. Customize settings: Edit → Settings
5. Check keyboard shortcuts in Help

Need More Help?
• Visit: https://github.com/McJono/pdf-manipulate
• Check the docs/ folder for detailed guides
• View FAQ.md for common questions

Thank you for using PDF Manipulate!

Click "Finish" to start working with your PDFs."""
        
        text.insert("1.0", content)
        text.config(state=tk.DISABLED)


def show_getting_started(parent=None):
    """
    Show the getting started wizard.
    
    Args:
        parent: Parent window
    
    Returns:
        GettingStartedWizard instance
    """
    # Check if user has disabled it
    if not preferences.get("ui_state.show_getting_started", True):
        return None
    
    wizard = GettingStartedWizard(parent)
    return wizard
