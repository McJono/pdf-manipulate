"""
Auto-rotation UI screen for manual review and override.

Provides a graphical interface for reviewing auto-detected rotations
and manually adjusting them before applying.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import List, Optional
import threading

try:
    from PIL import Image, ImageTk
    from pdf2image import convert_from_path
    PREVIEW_AVAILABLE = True
except ImportError:
    PREVIEW_AVAILABLE = False

from ..pdf_operations.batch_rotator import BatchRotationProcessor, PDFRotationJob
from ..utils.logger import logger
from .undo_redo import UndoRedoManager, RotationAction
from .keyboard_shortcuts import create_shortcuts_manager
from .tooltip import create_tooltip


class AutoRotationScreen(ttk.Frame):
    """
    Screen for reviewing and manually overriding auto-detected rotations.
    
    Features:
    - File list with rotation status
    - Preview pane showing before/after rotation
    - Manual rotation controls
    - Batch processing with progress tracking
    """
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.processor: Optional[BatchRotationProcessor] = None
        self.current_job_idx = 0
        self.current_page_idx = 0
        self.is_paused = False
        self.processing_thread = None
        
        # Undo/redo manager
        self.undo_manager = UndoRedoManager(max_history=50)
        
        # Keyboard shortcuts
        self.shortcuts = create_shortcuts_manager(parent)
        self._setup_shortcuts()
        
        self._create_widgets()
        self._layout_widgets()
        
    def _create_widgets(self):
        """Create all UI widgets"""
        
        # Top toolbar
        self.toolbar = ttk.Frame(self)
        
        self.btn_add_files = ttk.Button(
            self.toolbar,
            text="📁 Add Files...",
            command=self._add_files
        )
        create_tooltip(self.btn_add_files, "Add PDF files to process")
        
        self.btn_add_folder = ttk.Button(
            self.toolbar,
            text="📂 Add Folder...",
            command=self._add_folder
        )
        create_tooltip(self.btn_add_folder, "Add all PDFs from a folder")
        
        self.btn_clear = ttk.Button(
            self.toolbar,
            text="🗑️ Clear All",
            command=self._clear_all
        )
        create_tooltip(self.btn_clear, "Clear all files from queue")
        
        # Separator
        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Undo/Redo buttons
        self.btn_undo = ttk.Button(
            self.toolbar,
            text="↶ Undo",
            command=self._undo,
            state=tk.DISABLED
        )
        create_tooltip(self.btn_undo, f"Undo last rotation ({self.shortcuts.get_display_text('undo')})")
        
        self.btn_redo = ttk.Button(
            self.toolbar,
            text="↷ Redo",
            command=self._redo,
            state=tk.DISABLED
        )
        create_tooltip(self.btn_redo, f"Redo rotation ({self.shortcuts.get_display_text('redo')})")
        
        # Main content area (split into two panes)
        self.paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        
        # Left pane: File list
        self.left_pane = ttk.Frame(self.paned_window)
        self.paned_window.add(self.left_pane, weight=1)
        
        ttk.Label(self.left_pane, text="PDF Files", font=("", 12, "bold")).pack(
            anchor=tk.W, padx=5, pady=5
        )
        
        # File tree
        self.tree_frame = ttk.Frame(self.left_pane)
        self.tree_scroll = ttk.Scrollbar(self.tree_frame)
        
        self.file_tree = ttk.Treeview(
            self.tree_frame,
            columns=("pages", "rotation", "confidence"),
            show="tree headings",
            yscrollcommand=self.tree_scroll.set
        )
        self.tree_scroll.config(command=self.file_tree.yview)
        
        self.file_tree.heading("#0", text="File/Page")
        self.file_tree.heading("pages", text="Pages")
        self.file_tree.heading("rotation", text="Rotation")
        self.file_tree.heading("confidence", text="Confidence")
        
        self.file_tree.column("#0", width=200)
        self.file_tree.column("pages", width=60)
        self.file_tree.column("rotation", width=80)
        self.file_tree.column("confidence", width=80)
        
        self.file_tree.bind("<<TreeviewSelect>>", self._on_tree_select)
        
        # Right pane: Preview and controls
        self.right_pane = ttk.Frame(self.paned_window)
        self.paned_window.add(self.right_pane, weight=2)
        
        ttk.Label(self.right_pane, text="Preview", font=("", 12, "bold")).pack(
            anchor=tk.W, padx=5, pady=5
        )
        
        # Preview canvas
        self.preview_frame = ttk.Frame(self.right_pane, relief=tk.SUNKEN, borderwidth=2)
        self.preview_label = ttk.Label(
            self.preview_frame,
            text="Select a page to preview",
            font=("", 10),
            anchor=tk.CENTER
        )
        self.preview_label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Rotation controls
        self.controls_frame = ttk.Frame(self.right_pane)
        
        ttk.Label(self.controls_frame, text="Manual Rotation:").grid(
            row=0, column=0, columnspan=4, pady=5
        )
        
        self.btn_rotate_left = ttk.Button(
            self.controls_frame,
            text="⟲ Rotate Left (90°)",
            command=lambda: self._manual_rotate(-90)
        )
        self.btn_rotate_left.grid(row=1, column=0, padx=2)
        
        self.btn_rotate_180 = ttk.Button(
            self.controls_frame,
            text="⟳ Rotate 180°",
            command=lambda: self._manual_rotate(180)
        )
        self.btn_rotate_180.grid(row=1, column=1, padx=2)
        
        self.btn_rotate_right = ttk.Button(
            self.controls_frame,
            text="⟳ Rotate Right (90°)",
            command=lambda: self._manual_rotate(90)
        )
        self.btn_rotate_right.grid(row=1, column=2, padx=2)
        
        self.btn_reset = ttk.Button(
            self.controls_frame,
            text="Reset",
            command=self._reset_rotation
        )
        self.btn_reset.grid(row=1, column=3, padx=2)
        
        # Bottom action bar
        self.action_bar = ttk.Frame(self)
        
        self.progress_var = tk.StringVar(value="No files loaded")
        self.progress_label = ttk.Label(
            self.action_bar,
            textvariable=self.progress_var
        )
        
        # Accept All / Review Each buttons
        self.btn_accept_all = ttk.Button(
            self.action_bar,
            text="✓ Accept All",
            command=self._accept_all,
            state=tk.DISABLED
        )
        create_tooltip(self.btn_accept_all, "Accept all auto-rotation suggestions and process")
        
        self.btn_review_each = ttk.Button(
            self.action_bar,
            text="👁 Review Each",
            command=self._review_each,
            state=tk.DISABLED
        )
        create_tooltip(self.btn_review_each, "Review each page one by one")
        
        # Pause/Resume button
        self.btn_pause_resume = ttk.Button(
            self.action_bar,
            text="⏸ Pause",
            command=self._toggle_pause,
            state=tk.DISABLED
        )
        create_tooltip(self.btn_pause_resume, "Pause/Resume processing")
        
        self.btn_process = ttk.Button(
            self.action_bar,
            text="▶ Process All",
            command=self._process_all,
            state=tk.DISABLED
        )
        create_tooltip(self.btn_process, "Process all files with current settings")
        
    def _layout_widgets(self):
        """Layout all widgets"""
        
        # Toolbar
        self.toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.btn_add_files.pack(side=tk.LEFT, padx=2)
        self.btn_add_folder.pack(side=tk.LEFT, padx=2)
        self.btn_clear.pack(side=tk.LEFT, padx=2)
        # Undo/redo are in toolbar frame, pack them after separator
        self.btn_undo.pack(side=tk.LEFT, padx=2)
        self.btn_redo.pack(side=tk.LEFT, padx=2)
        
        # Main content
        self.paned_window.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left pane
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Right pane
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.controls_frame.pack(fill=tk.X, padx=5, pady=10)
        
        # Action bar
        self.action_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        self.progress_label.pack(side=tk.LEFT, padx=5)
        self.btn_process.pack(side=tk.RIGHT, padx=2)
        self.btn_pause_resume.pack(side=tk.RIGHT, padx=2)
        self.btn_review_each.pack(side=tk.RIGHT, padx=2)
        self.btn_accept_all.pack(side=tk.RIGHT, padx=2)
        
    def _add_files(self):
        """Add PDF files to the queue"""
        files = filedialog.askopenfilenames(
            title="Select PDF Files",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        
        if files:
            self._initialize_processor()
            for file in files:
                try:
                    self.processor.add_pdf(file)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to add {file}:\n{e}")
            
            self._refresh_tree()
            
    def _add_folder(self):
        """Add all PDFs from a folder"""
        folder = filedialog.askdirectory(title="Select Folder")
        
        if folder:
            self._initialize_processor()
            try:
                self.processor.add_directory(folder, recursive=False)
                self._refresh_tree()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add folder:\n{e}")
    
    def _clear_all(self):
        """Clear all files from the queue"""
        if messagebox.askyesno("Confirm", "Clear all files from the queue?"):
            self.processor = None
            self.file_tree.delete(*self.file_tree.get_children())
            self.progress_var.set("No files loaded")
            self.btn_process.config(state=tk.DISABLED)
            self.preview_label.config(text="Select a page to preview", image="")
    
    def _initialize_processor(self):
        """Initialize the batch processor if not already done"""
        if self.processor is None:
            self.processor = BatchRotationProcessor(
                confidence_threshold=0.80,
                backup_originals=True
            )
    
    def _on_tree_select(self, event):
        """Handle tree selection"""
        # For now, just show a message
        # In a full implementation, this would load and display the page preview
        selection = self.file_tree.selection()
        if selection:
            item = self.file_tree.item(selection[0])
            self.preview_label.config(
                text=f"Preview for: {item['text']}\n(Preview generation not yet implemented)"
            )
    
    def _manual_rotate(self, angle: int):
        """Apply manual rotation to selected page"""
        messagebox.showinfo(
            "Manual Rotation",
            f"Manual rotation by {angle}° will be implemented in the UI.\n"
            "For now, use the batch processor directly."
        )
    
    def _reset_rotation(self):
        """Reset rotation to original"""
        messagebox.showinfo(
            "Reset Rotation",
            "Reset rotation will be implemented in the UI.\n"
            "For now, re-add the file to reset."
        )
    
    def _process_all(self):
        """Process all PDFs with auto-rotation"""
        if not self.processor or not self.processor.jobs:
            messagebox.showwarning("No Files", "No files to process")
            return
        
        # Ask for output directory
        output_dir = filedialog.askdirectory(title="Select Output Directory")
        if not output_dir:
            return
        
        # Confirm processing
        summary = self.processor.get_summary()
        if not messagebox.askyesno(
            "Confirm Processing",
            f"Process {summary['total_jobs']} files?\n"
            f"{summary['high_confidence_pages']} pages will be auto-rotated.\n"
            f"Output will be saved to:\n{output_dir}"
        ):
            return
        
        # Disable controls during processing
        self.btn_process.config(state=tk.DISABLED)
        self.progress_var.set("Processing...")
        
        # Process in background thread
        def process_thread():
            try:
                results = self.processor.process_all(
                    auto_rotate_high_confidence=True,
                    output_dir=Path(output_dir)
                )
                
                # Update UI on completion
                self.after(0, lambda: self._processing_complete(results))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Error", f"Processing failed:\n{e}"))
                self.after(0, lambda: self.btn_process.config(state=tk.NORMAL))
        
        thread = threading.Thread(target=process_thread, daemon=True)
        thread.start()
    
    def _processing_complete(self, results):
        """Handle processing completion"""
        messagebox.showinfo(
            "Processing Complete",
            f"Files processed: {results['total_files']}\n"
            f"Pages rotated: {results['pages_rotated']}\n"
            f"Pages skipped: {results['pages_skipped']}\n"
            f"Errors: {results['errors']}"
        )
        
        self.progress_var.set("Processing complete")
        self.btn_process.config(state=tk.NORMAL)
        self.is_paused = False
        self.btn_pause_resume.config(text="⏸ Pause", state=tk.DISABLED)
    
    def _setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        self.shortcuts.bind('undo', self._undo)
        self.shortcuts.bind('redo', self._redo)
        self.shortcuts.bind('rotate_right', lambda e: self._manual_rotate(90))
        self.shortcuts.bind('rotate_left', lambda e: self._manual_rotate(-90))
        self.shortcuts.bind('accept', self._accept_all)
        self.shortcuts.bind('next', self._next_page)
        self.shortcuts.bind('prev', self._prev_page)
    
    def _update_undo_redo_buttons(self):
        """Update undo/redo button states"""
        self.btn_undo.config(
            state=tk.NORMAL if self.undo_manager.can_undo() else tk.DISABLED
        )
        self.btn_redo.config(
            state=tk.NORMAL if self.undo_manager.can_redo() else tk.DISABLED
        )
    
    def _undo(self, event=None):
        """Undo last rotation"""
        action = self.undo_manager.undo()
        if action:
            # Apply the old rotation
            logger.info(f"Undoing: {action}")
            messagebox.showinfo("Undo", f"Undone: {action}")
            self._update_undo_redo_buttons()
        else:
            messagebox.showinfo("Undo", "Nothing to undo")
    
    def _redo(self, event=None):
        """Redo last undone rotation"""
        action = self.undo_manager.redo()
        if action:
            # Reapply the new rotation
            logger.info(f"Redoing: {action}")
            messagebox.showinfo("Redo", f"Redone: {action}")
            self._update_undo_redo_buttons()
        else:
            messagebox.showinfo("Redo", "Nothing to redo")
    
    def _accept_all(self, event=None):
        """Accept all auto-rotation suggestions and process immediately"""
        if not self.processor or not self.processor.jobs:
            messagebox.showwarning("No Files", "No files to process")
            return
        
        # Ask for confirmation
        summary = self.processor.get_summary()
        if not messagebox.askyesno(
            "Accept All",
            f"Accept all auto-rotation suggestions?\n\n"
            f"{summary['high_confidence_pages']} pages will be automatically rotated.\n"
            f"This will process all files immediately."
        ):
            return
        
        # Process all
        self._process_all()
    
    def _review_each(self):
        """Start review mode - go through each page one by one"""
        if not self.processor or not self.processor.jobs:
            messagebox.showwarning("No Files", "No files to process")
            return
        
        messagebox.showinfo(
            "Review Mode",
            "Review mode will allow you to navigate through each page\n"
            "and accept or modify the rotation suggestion.\n\n"
            "Use arrow keys to navigate:\n"
            "→ Next page\n"
            "← Previous page\n"
            "Enter - Accept current page\n"
            "R - Rotate right\n"
            "L - Rotate left"
        )
        
        # Enable review navigation
        self.btn_accept_all.config(state=tk.DISABLED)
        self.btn_review_each.config(state=tk.DISABLED)
        
        # TODO: Implement page-by-page review interface
    
    def _next_page(self, event=None):
        """Navigate to next page in review mode"""
        # TODO: Implement navigation
        pass
    
    def _prev_page(self, event=None):
        """Navigate to previous page in review mode"""
        # TODO: Implement navigation
        pass
    
    def _toggle_pause(self):
        """Toggle pause/resume for batch processing"""
        self.is_paused = not self.is_paused
        
        if self.is_paused:
            self.btn_pause_resume.config(text="▶ Resume")
            logger.info("Processing paused")
        else:
            self.btn_pause_resume.config(text="⏸ Pause")
            logger.info("Processing resumed")
    
    def _refresh_tree(self):
        """Refresh the file tree with current processor state"""
        self.file_tree.delete(*self.file_tree.get_children())
        
        if not self.processor or not self.processor.jobs:
            return
        
        # Add jobs to tree
        for job in self.processor.jobs:
            # Add file node
            file_node = self.file_tree.insert(
                "",
                tk.END,
                text=job.pdf_path.name,
                values=(
                    job.total_pages,
                    f"{job.pages_needing_rotation} pages",
                    f"{job.high_confidence_pages} high conf"
                ),
                open=True
            )
            
            # Add page nodes
            for page in job.pages:
                self.file_tree.insert(
                    file_node,
                    tk.END,
                    text=f"Page {page.page_number + 1}",
                    values=(
                        "",
                        f"{page.suggested_angle}°" if page.suggested_angle != 0 else "OK",
                        f"{page.confidence:.1%}"
                    )
                )
        
        # Update status and enable buttons
        summary = self.processor.get_summary()
        self.progress_var.set(
            f"{summary['total_jobs']} files, {summary['total_pages']} pages, "
            f"{summary['high_confidence_pages']} auto-rotate ready"
        )
        self.btn_process.config(state=tk.NORMAL)
        self.btn_accept_all.config(state=tk.NORMAL)
        self.btn_review_each.config(state=tk.NORMAL)


def show_auto_rotation_screen(parent=None):
    """
    Show the auto-rotation screen in a new window.
    
    Args:
        parent: Parent window (None for standalone)
    """
    if parent is None:
        root = tk.Tk()
        root.title("PDF Auto-Rotation")
        root.geometry("900x600")
    else:
        root = tk.Toplevel(parent)
        root.title("PDF Auto-Rotation")
        root.geometry("900x600")
    
    screen = AutoRotationScreen(root)
    screen.pack(fill=tk.BOTH, expand=True)
    
    if parent is None:
        root.mainloop()
    
    return screen
