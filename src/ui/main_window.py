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
        """Show merge interface (placeholder)"""
        if not self.selected_files:
            messagebox.showwarning(
                "No Files",
                "Please select PDF files first using 'Open PDF Files'"
            )
            return

        messagebox.showinfo(
            "Merge PDFs",
            f"Merge feature coming soon!\n\n"
            f"Selected {len(self.selected_files)} file(s) to merge."
        )

    def _show_batch_process(self) -> None:
        """Show batch processing interface (placeholder)"""
        messagebox.showinfo(
            "Batch Process",
            "Batch processing feature coming soon!"
        )

    def _show_about(self) -> None:
        """Show about dialog"""
        messagebox.showinfo(
            "About PDF Manipulate",
            "PDF Manipulate v0.1.0\n\n"
            "An intelligent PDF manipulation program\n"
            "that automates document processing.\n\n"
            "Features:\n"
            "• Auto-Rotation\n"
            "• Interactive Merging\n"
            "• Smart Naming\n\n"
            "© 2024 McJono"
        )

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
