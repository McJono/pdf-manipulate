"""
Main window for PDF Manipulate application
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import List, Optional
from ..config.manager import config
from ..config.preferences import preferences
from ..utils.logger import logger
from .keyboard_shortcuts import create_shortcuts_manager
from .tooltip import create_tooltip


class MainWindow:
    """Main application window"""

    def __init__(self):
        """Initialize main window"""
        self.root = tk.Tk()
        self.root.title("PDF Manipulate")

        # Load window geometry from preferences
        geom = preferences.get_window_geometry()
        width, height = geom['width'], geom['height']
        x, y = geom['x'], geom['y']
        
        if x is not None and y is not None:
            self.root.geometry(f"{width}x{height}+{x}+{y}")
        else:
            self.root.geometry(f"{width}x{height}")

        # Selected files
        self.selected_files: List[Path] = []

        # Setup keyboard shortcuts
        self.shortcuts = create_shortcuts_manager(self.root)
        self._setup_shortcuts()

        # Setup UI
        self._create_menu()
        self._create_toolbar()
        self._create_widgets()
        
        # Save window geometry on close
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

        logger.info("Main window initialized")

    def _create_menu(self) -> None:
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Add keyboard shortcut hints to menu items
        open_shortcut = self.shortcuts.get_display_text('open_file')
        quit_shortcut = self.shortcuts.get_display_text('quit')
        
        file_menu.add_command(
            label=f"Open PDF{'...':<15}{open_shortcut:>10}",
            command=self._open_file
        )
        file_menu.add_command(label="Open Folder...", command=self._open_folder)
        
        # Recent files submenu
        self.recent_files_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Recent Files", menu=self.recent_files_menu)
        self._update_recent_files_menu()
        
        file_menu.add_separator()
        file_menu.add_command(
            label=f"Exit{'':< 15}{quit_shortcut:>10}",
            command=self._on_closing
        )

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        
        settings_shortcut = self.shortcuts.get_display_text('settings')
        edit_menu.add_command(
            label=f"Settings...{'':< 15}{settings_shortcut:>10}",
            command=self._show_settings
        )

        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        
        auto_rotate_shortcut = self.shortcuts.get_display_text('auto_rotate')
        merge_shortcut = self.shortcuts.get_display_text('merge')
        
        tools_menu.add_command(
            label=f"Auto-Rotate{'':< 15}{auto_rotate_shortcut:>10}",
            command=self._show_auto_rotate
        )
        tools_menu.add_command(
            label=f"Merge PDFs{'':< 15}{merge_shortcut:>10}",
            command=self._show_merge
        )
        tools_menu.add_command(label="Batch Process", command=self._show_batch_process)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        help_shortcut = self.shortcuts.get_display_text('help')
        help_menu.add_command(
            label=f"Help{'':< 15}{help_shortcut:>10}",
            command=self._show_help
        )
        help_menu.add_command(label="About", command=self._show_about)
    
    def _create_toolbar(self) -> None:
        """Create toolbar with quick access buttons"""
        toolbar = ttk.Frame(self.root, relief=tk.RAISED, borderwidth=1)
        toolbar.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=2, pady=2)
        
        # Open file button
        btn_open = ttk.Button(toolbar, text="📁 Open", command=self._open_file, width=12)
        btn_open.pack(side=tk.LEFT, padx=2, pady=2)
        create_tooltip(btn_open, f"Open PDF files ({self.shortcuts.get_display_text('open_file')})")
        
        # Separator
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=2)
        
        # Auto-rotate button
        btn_rotate = ttk.Button(toolbar, text="🔄 Auto-Rotate", command=self._show_auto_rotate, width=14)
        btn_rotate.pack(side=tk.LEFT, padx=2, pady=2)
        create_tooltip(btn_rotate, f"Auto-rotate PDFs ({self.shortcuts.get_display_text('auto_rotate')})")
        
        # Merge button
        btn_merge = ttk.Button(toolbar, text="🔗 Merge", command=self._show_merge, width=12)
        btn_merge.pack(side=tk.LEFT, padx=2, pady=2)
        create_tooltip(btn_merge, f"Merge PDFs ({self.shortcuts.get_display_text('merge')})")
        
        # Separator
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=2)
        
        # Settings button
        btn_settings = ttk.Button(toolbar, text="⚙️ Settings", command=self._show_settings, width=12)
        btn_settings.pack(side=tk.LEFT, padx=2, pady=2)
        create_tooltip(btn_settings, f"Settings ({self.shortcuts.get_display_text('settings')})")
        
        # Help button (on the right)
        btn_help = ttk.Button(toolbar, text="❓ Help", command=self._show_help, width=10)
        btn_help.pack(side=tk.RIGHT, padx=2, pady=2)
        create_tooltip(btn_help, f"Help ({self.shortcuts.get_display_text('help')})")
    
    def _setup_shortcuts(self) -> None:
        """Setup keyboard shortcuts"""
        self.shortcuts.bind('open_file', self._open_file)
        self.shortcuts.bind('quit', self._on_closing)
        self.shortcuts.bind('settings', self._show_settings)
        self.shortcuts.bind('auto_rotate', self._show_auto_rotate)
        self.shortcuts.bind('merge', self._show_merge)
        self.shortcuts.bind('help', self._show_help)
    
    def _update_recent_files_menu(self) -> None:
        """Update the recent files menu"""
        # Clear existing items
        self.recent_files_menu.delete(0, tk.END)
        
        recent_files = preferences.get_recent_files()
        
        if not recent_files:
            self.recent_files_menu.add_command(label="(No recent files)", state=tk.DISABLED)
        else:
            for filepath in recent_files[:10]:  # Show max 10
                path = Path(filepath)
                self.recent_files_menu.add_command(
                    label=path.name,
                    command=lambda p=path: self._open_recent_file(p)
                )
            
            # Add clear recent files option
            self.recent_files_menu.add_separator()
            self.recent_files_menu.add_command(
                label="Clear Recent Files",
                command=self._clear_recent_files
            )
    
    def _open_recent_file(self, filepath: Path) -> None:
        """Open a recent file"""
        if filepath.exists():
            self.selected_files = [filepath]
            self.status_var.set(f"Opened: {filepath.name}")
            logger.info(f"Opened recent file: {filepath}")
        else:
            messagebox.showerror("File Not Found", f"File not found:\n{filepath}")
            # Remove from recent files
            recent = preferences.get("recent_files", [])
            if str(filepath) in recent:
                recent.remove(str(filepath))
                preferences.set("recent_files", recent)
                preferences.save()
                self._update_recent_files_menu()
    
    def _clear_recent_files(self) -> None:
        """Clear recent files list"""
        if messagebox.askyesno("Clear Recent Files", "Clear all recent files from the list?"):
            preferences.set("recent_files", [])
            preferences.save()
            self._update_recent_files_menu()
    
    def _on_closing(self, event=None) -> None:
        """Handle window closing - save preferences"""
        # Save window geometry
        geom = self.root.geometry()
        # Parse geometry string: WIDTHxHEIGHT+X+Y
        parts = geom.replace('x', '+').split('+')
        if len(parts) >= 4:
            width, height, x, y = int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])
            preferences.set_window_geometry(width, height, x, y)
        
        # Save preferences
        preferences.save()
        logger.info("Saved preferences")
        
        # Close application
        self.root.quit()

    def _create_widgets(self) -> None:
        """Create main window widgets"""
        # Main frame (now at row 1 because toolbar is at row 0)
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)  # Main frame expands
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="PDF Manipulate",
            font=("Arial", 24, "bold")
        )
        title_label.grid(row=0, column=0, pady=20)

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, pady=20)

        # Buttons
        ttk.Button(
            button_frame,
            text="Open PDF Files",
            command=self._open_file,
            width=20
        ).grid(row=0, column=0, padx=5, pady=5)

        ttk.Button(
            button_frame,
            text="Auto-Rotate PDFs",
            command=self._show_auto_rotate,
            width=20
        ).grid(row=1, column=0, padx=5, pady=5)

        ttk.Button(
            button_frame,
            text="Merge PDFs",
            command=self._show_merge,
            width=20
        ).grid(row=2, column=0, padx=5, pady=5)

        # Status bar (now at row 2)
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.grid(row=2, column=0, sticky=(tk.W, tk.E))

    def _open_file(self, event=None) -> None:
        """Open file dialog to select PDF files"""
        # Get initial directory from preferences
        initial_dir = preferences.get("last_output_directory", str(Path.home()))
        
        files = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialdir=initial_dir
        )

        if files:
            self.selected_files = [Path(f) for f in files]
            self.status_var.set(f"Selected {len(self.selected_files)} file(s)")
            logger.info(f"Selected {len(self.selected_files)} files")
            
            # Add to recent files
            for file in self.selected_files:
                preferences.add_recent_file(file)
            
            # Save directory
            if self.selected_files:
                preferences.set("last_output_directory", str(self.selected_files[0].parent))
                preferences.save()
                self._update_recent_files_menu()

    def _open_folder(self) -> None:
        """Open folder dialog"""
        # Get initial directory from preferences
        initial_dir = preferences.get("last_output_directory", str(Path.home()))
        
        folder = filedialog.askdirectory(title="Select folder", initialdir=initial_dir)
        if folder:
            folder_path = Path(folder)
            self.selected_files = list(folder_path.glob("*.pdf"))
            self.status_var.set(f"Found {len(self.selected_files)} PDF(s) in folder")
            logger.info(f"Found {len(self.selected_files)} PDFs in {folder}")
            
            # Add to recent directories
            preferences.add_recent_directory(folder_path)
            preferences.set("last_output_directory", str(folder_path))
            preferences.save()

    def _show_auto_rotate(self) -> None:
        """Show auto-rotation interface (placeholder)"""
        messagebox.showinfo(
            "Auto-Rotate",
            "Auto-rotation feature coming soon!\n\n"
            "This will automatically detect and rotate incorrectly oriented pages."
        )

    def _show_merge(self) -> None:
        """Show merge interface"""
        try:
            from .merge_screen import show_merge_screen
            
            # Create new window for merge screen
            merge_window = tk.Toplevel(self.root)
            merge_window.title("PDF Merge")
            merge_window.geometry("1200x700")
            
            # Show merge screen
            show_merge_screen(merge_window)
            
        except ImportError as e:
            messagebox.showerror(
                "Missing Dependencies",
                f"Merge functionality requires additional dependencies:\n\n{e}\n\n"
                "Install with: pip install -r requirements.txt"
            )
        except Exception as e:
            logger.error(f"Error showing merge screen: {e}")
            messagebox.showerror("Error", f"Failed to open merge screen:\n{str(e)}")

    def _show_batch_process(self) -> None:
        """Show batch processing interface (placeholder)"""
        messagebox.showinfo(
            "Batch Process",
            "Batch processing feature coming soon!"
        )
    
    def _show_settings(self) -> None:
        """Show settings/preferences dialog"""
        try:
            from .settings_dialog import show_settings_dialog
            show_settings_dialog(self.root)
        except Exception as e:
            logger.error(f"Error showing settings dialog: {e}")
            messagebox.showerror("Error", f"Failed to open settings dialog:\n{str(e)}")
    
    def _show_help(self, event=None) -> None:
        """Show help dialog"""
        help_window = tk.Toplevel(self.root)
        help_window.title("PDF Manipulate - Help")
        help_window.geometry("600x500")
        help_window.transient(self.root)
        
        # Main frame
        main_frame = ttk.Frame(help_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(
            main_frame,
            text="PDF Manipulate - Quick Help",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=(0, 15))
        
        # Help text
        help_text = tk.Text(
            main_frame,
            wrap=tk.WORD,
            font=("Arial", 10)
        )
        help_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        help_content = """KEYBOARD SHORTCUTS:

File Operations:
  {open}  - Open PDF files
  {quit}  - Exit application

Tools:
  {auto_rotate}  - Auto-rotate PDFs
  {merge}  - Merge PDFs

Settings & Help:
  {settings}  - Open settings
  {help}  - Show this help

Navigation (in dialogs):
  Arrow Keys - Navigate items
  Enter - Accept/Select
  Escape - Cancel/Close

FEATURES:

Auto-Rotation:
  Automatically detect and rotate incorrectly oriented pages using OCR.
  Review and manually adjust rotations before applying.

PDF Merging:
  Select multiple PDFs and merge them in any order.
  Preview pages before merging.
  Use smart naming templates for output files.

Smart Naming:
  Use templates like {{date}}_{{name}}.pdf
  Date arithmetic: {{date+7}} for 7 days from now
  Variables: {{date}}, {{name}}, {{filename}}, {{timestamp}}, {{counter}}

For more information, see the documentation or visit:
https://github.com/McJono/pdf-manipulate
""".format(
            open=self.shortcuts.get_display_text('open_file'),
            quit=self.shortcuts.get_display_text('quit'),
            auto_rotate=self.shortcuts.get_display_text('auto_rotate'),
            merge=self.shortcuts.get_display_text('merge'),
            settings=self.shortcuts.get_display_text('settings'),
            help=self.shortcuts.get_display_text('help')
        )
        
        help_text.insert("1.0", help_content)
        help_text.config(state=tk.DISABLED)
        
        # Close button
        ttk.Button(
            main_frame,
            text="Close",
            command=help_window.destroy,
            width=15
        ).pack()

    def _show_about(self) -> None:
        """Show about dialog"""
        about_window = tk.Toplevel(self.root)
        about_window.title("About PDF Manipulate")
        about_window.geometry("450x400")
        about_window.resizable(False, False)
        
        # Center the window
        about_window.transient(self.root)
        about_window.grab_set()
        
        # Main frame
        main_frame = ttk.Frame(about_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(
            main_frame,
            text="PDF Manipulate",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=(0, 5))
        
        # Version
        version = ttk.Label(
            main_frame,
            text="Version 1.0.0",
            font=("Arial", 10)
        )
        version.pack(pady=(0, 20))
        
        # Description
        description = tk.Text(
            main_frame,
            height=8,
            width=50,
            wrap=tk.WORD,
            relief=tk.FLAT,
            background=about_window.cget('bg')
        )
        description.pack(pady=(0, 20))
        
        description_text = """An intelligent PDF manipulation program that automates document processing with features for auto-rotation, merging, and smart file naming.

Features:
• Auto-Rotation - Detect and rotate incorrectly oriented pages
• Interactive Merging - Select and merge PDFs with live previews
• Smart Naming - Template-based file naming with date arithmetic
• Cross-Platform - Works on Windows, macOS, and Linux"""
        
        description.insert("1.0", description_text)
        description.config(state=tk.DISABLED)
        
        # Copyright
        copyright_label = ttk.Label(
            main_frame,
            text="© 2024-2026 McJono",
            font=("Arial", 9)
        )
        copyright_label.pack(pady=(0, 10))
        
        # GitHub link
        github_frame = ttk.Frame(main_frame)
        github_frame.pack(pady=(0, 20))
        
        ttk.Label(
            github_frame,
            text="GitHub:",
            font=("Arial", 9)
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        github_label = ttk.Label(
            github_frame,
            text="github.com/McJono/pdf-manipulate",
            font=("Arial", 9),
            foreground="blue",
            cursor="hand2"
        )
        github_label.pack(side=tk.LEFT)
        
        # Make GitHub link clickable (visual only)
        def on_github_click(event):
            messagebox.showinfo(
                "GitHub",
                "Visit: https://github.com/McJono/pdf-manipulate"
            )
        github_label.bind("<Button-1>", on_github_click)
        
        # Close button
        ttk.Button(
            main_frame,
            text="Close",
            command=about_window.destroy,
            width=15
        ).pack()

    def run(self) -> None:
        """Start the application main loop"""
        logger.info("Starting application")
        self.root.mainloop()


def create_main_window() -> MainWindow:
    """
    Create and return main window instance.

    Returns:
        MainWindow instance
    """
    return MainWindow()
