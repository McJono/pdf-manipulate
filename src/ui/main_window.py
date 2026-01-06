"""
Main window for PDF Manipulate application
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import List, Optional
from ..config.manager import config
from ..utils.logger import logger


class MainWindow:
    """Main application window"""

    def __init__(self):
        """Initialize main window"""
        self.root = tk.Tk()
        self.root.title("PDF Manipulate")

        # Get window size from config
        window_size = config.get("ui.window_size", {"width": 1200, "height": 800})
        self.root.geometry(f"{window_size['width']}x{window_size['height']}")

        # Selected files
        self.selected_files: List[Path] = []

        # Setup UI
        self._create_menu()
        self._create_widgets()

        logger.info("Main window initialized")

    def _create_menu(self) -> None:
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open PDF", command=self._open_file)
        file_menu.add_command(label="Open Folder", command=self._open_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Settings...", command=self._show_settings)

        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Auto-Rotate", command=self._show_auto_rotate)
        tools_menu.add_command(label="Merge PDFs", command=self._show_merge)
        tools_menu.add_command(label="Batch Process", command=self._show_batch_process)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)

    def _create_widgets(self) -> None:
        """Create main window widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
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

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))

    def _open_file(self) -> None:
        """Open file dialog to select PDF files"""
        files = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )

        if files:
            self.selected_files = [Path(f) for f in files]
            self.status_var.set(f"Selected {len(self.selected_files)} file(s)")
            logger.info(f"Selected {len(self.selected_files)} files")

    def _open_folder(self) -> None:
        """Open folder dialog"""
        folder = filedialog.askdirectory(title="Select folder")
        if folder:
            folder_path = Path(folder)
            self.selected_files = list(folder_path.glob("*.pdf"))
            self.status_var.set(f"Found {len(self.selected_files)} PDF(s) in folder")
            logger.info(f"Found {len(self.selected_files)} PDFs in {folder}")

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
