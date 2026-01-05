"""
File Selection and Merge Screen

This module implements the UI for selecting PDF files, previewing them,
arranging merge order, and executing the merge operation.
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import List, Optional, Dict, Tuple
import logging
from datetime import datetime
from PIL import Image, ImageTk

try:
    from ..pdf_operations.preview import PDFPreviewGenerator, create_blank_thumbnail
    from ..pdf_operations.merger import PDFMerger
    from ..pdf_operations.loader import PDFLoader
    from ..naming.parser import TemplateParser
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False

logger = logging.getLogger(__name__)


class PDFFileInfo:
    """Information about a PDF file for the merge interface."""
    
    def __init__(self, file_path: str):
        """
        Initialize file info.
        
        Args:
            file_path: Path to the PDF file
        """
        self.file_path = file_path
        self.filename = os.path.basename(file_path)
        self.file_size = os.path.getsize(file_path)
        self.modified_date = datetime.fromtimestamp(os.path.getmtime(file_path))
        self.page_count = 0
        self.thumbnail: Optional[ImageTk.PhotoImage] = None
        
        # Try to get page count
        try:
            if DEPENDENCIES_AVAILABLE:
                loader = PDFLoader()
                metadata = loader.get_metadata(file_path)
                self.page_count = metadata.get('page_count', 0)
        except Exception as e:
            logger.warning(f"Could not load page count for {file_path}: {e}")
    
    def format_size(self) -> str:
        """Format file size in human-readable form."""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def format_date(self) -> str:
        """Format modification date."""
        return self.modified_date.strftime("%Y-%m-%d %H:%M")


class PreviewDialog(tk.Toplevel):
    """Full-page preview dialog."""
    
    def __init__(self, parent, pdf_path: str, page_number: int = 0):
        """
        Initialize preview dialog.
        
        Args:
            parent: Parent window
            pdf_path: Path to PDF file
            page_number: Initial page to display (0-indexed)
        """
        super().__init__(parent)
        
        self.pdf_path = pdf_path
        self.current_page = page_number
        self.total_pages = 0
        self.preview_generator = PDFPreviewGenerator()
        
        # Get total pages
        try:
            loader = PDFLoader()
            metadata = loader.get_metadata(pdf_path)
            self.total_pages = metadata.get('page_count', 1)
        except Exception as e:
            logger.error(f"Could not load PDF metadata: {e}")
            self.total_pages = 1
        
        self.title(f"Preview: {os.path.basename(pdf_path)}")
        self.geometry("800x900")
        
        self._create_widgets()
        self._load_page()
    
    def _create_widgets(self):
        """Create dialog widgets."""
        # Navigation frame
        nav_frame = ttk.Frame(self)
        nav_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Previous button
        self.prev_button = ttk.Button(
            nav_frame,
            text="◀ Previous",
            command=self._previous_page
        )
        self.prev_button.pack(side=tk.LEFT, padx=2)
        
        # Page info
        self.page_label = ttk.Label(nav_frame, text="")
        self.page_label.pack(side=tk.LEFT, expand=True)
        
        # Next button
        self.next_button = ttk.Button(
            nav_frame,
            text="Next ▶",
            command=self._next_page
        )
        self.next_button.pack(side=tk.RIGHT, padx=2)
        
        # Preview canvas with scrollbar
        canvas_frame = ttk.Frame(self)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(canvas_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas = tk.Canvas(
            canvas_frame,
            yscrollcommand=scrollbar.set,
            bg='gray85'
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.canvas.yview)
        
        # Close button
        close_button = ttk.Button(self, text="Close", command=self.destroy)
        close_button.pack(pady=5)
    
    def _load_page(self):
        """Load and display the current page."""
        # Update page label
        self.page_label.config(
            text=f"Page {self.current_page + 1} of {self.total_pages}"
        )
        
        # Update button states
        self.prev_button.config(state=tk.NORMAL if self.current_page > 0 else tk.DISABLED)
        self.next_button.config(
            state=tk.NORMAL if self.current_page < self.total_pages - 1 else tk.DISABLED
        )
        
        # Load preview image
        try:
            image = self.preview_generator.generate_preview(
                self.pdf_path,
                self.current_page,
                dpi=150
            )
            
            if image:
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(image)
                
                # Clear canvas
                self.canvas.delete("all")
                
                # Center image on canvas
                canvas_width = self.canvas.winfo_width()
                x = max((canvas_width - photo.width()) // 2, 0)
                
                # Add image
                self.canvas.create_image(x, 0, anchor=tk.NW, image=photo)
                self.canvas.image = photo  # Keep reference
                
                # Configure scroll region
                self.canvas.config(scrollregion=(0, 0, photo.width(), photo.height()))
            else:
                self.canvas.delete("all")
                self.canvas.create_text(
                    400, 300,
                    text="Preview not available",
                    font=('Arial', 16)
                )
        except Exception as e:
            logger.error(f"Error loading preview: {e}")
            messagebox.showerror("Error", f"Failed to load preview:\n{str(e)}")
    
    def _previous_page(self):
        """Navigate to previous page."""
        if self.current_page > 0:
            self.current_page -= 1
            self._load_page()
    
    def _next_page(self):
        """Navigate to next page."""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self._load_page()


class MergeScreen(ttk.Frame):
    """Main merge screen with file selection and preview."""
    
    def __init__(self, parent):
        """
        Initialize merge screen.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        
        if not DEPENDENCIES_AVAILABLE:
            self._show_dependency_error()
            return
        
        self.preview_generator = PDFPreviewGenerator(cache_size=100)
        self.files: Dict[str, PDFFileInfo] = {}  # file_path -> info
        self.merge_queue: List[str] = []  # Ordered list of file paths
        
        self._create_widgets()
    
    def _show_dependency_error(self):
        """Show error message for missing dependencies."""
        error_label = ttk.Label(
            self,
            text="Missing dependencies for merge functionality.\n"
                 "Install with: pip install -r requirements.txt",
            font=('Arial', 12),
            foreground='red'
        )
        error_label.pack(expand=True)
    
    def _create_widgets(self):
        """Create screen widgets."""
        # Main container with three columns
        main_pane = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=True)
        
        # Left: File browser
        self.file_browser_frame = self._create_file_browser()
        main_pane.add(self.file_browser_frame, weight=2)
        
        # Middle: Merge queue
        self.merge_queue_frame = self._create_merge_queue()
        main_pane.add(self.merge_queue_frame, weight=1)
        
        # Right: Preview
        self.preview_frame = self._create_preview_panel()
        main_pane.add(self.preview_frame, weight=2)
    
    def _create_file_browser(self) -> ttk.Frame:
        """Create file browser panel."""
        frame = ttk.Frame(self)
        
        # Title
        title = ttk.Label(frame, text="Available PDF Files", font=('Arial', 12, 'bold'))
        title.pack(pady=5)
        
        # Toolbar
        toolbar = ttk.Frame(frame)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(
            toolbar,
            text="Open Folder",
            command=self._open_folder
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            toolbar,
            text="Add Files",
            command=self._add_files
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            toolbar,
            text="Refresh",
            command=self._refresh_file_list
        ).pack(side=tk.LEFT, padx=2)
        
        # File list with thumbnails
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Using Treeview for file list
        self.file_tree = ttk.Treeview(
            list_frame,
            columns=('size', 'pages', 'date'),
            show='tree headings',
            yscrollcommand=scrollbar.set
        )
        self.file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.file_tree.yview)
        
        # Configure columns
        self.file_tree.heading('#0', text='Filename')
        self.file_tree.heading('size', text='Size')
        self.file_tree.heading('pages', text='Pages')
        self.file_tree.heading('date', text='Modified')
        
        self.file_tree.column('#0', width=200)
        self.file_tree.column('size', width=80)
        self.file_tree.column('pages', width=60)
        self.file_tree.column('date', width=120)
        
        # Bind events
        self.file_tree.bind('<Double-Button-1>', self._on_file_double_click)
        self.file_tree.bind('<Button-1>', self._on_file_click)
        
        return frame
    
    def _create_merge_queue(self) -> ttk.Frame:
        """Create merge queue panel."""
        frame = ttk.Frame(self)
        
        # Title
        title = ttk.Label(frame, text="Merge Queue", font=('Arial', 12, 'bold'))
        title.pack(pady=5)
        
        # Queue list
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.queue_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=('Courier', 10)
        )
        self.queue_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.queue_listbox.yview)
        
        self.queue_listbox.bind('<Double-Button-1>', self._on_queue_double_click)
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(
            button_frame,
            text="↑ Move Up",
            command=self._move_up_in_queue
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            button_frame,
            text="↓ Move Down",
            command=self._move_down_in_queue
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            button_frame,
            text="✕ Remove",
            command=self._remove_from_queue
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            button_frame,
            text="Clear All",
            command=self._clear_queue
        ).pack(fill=tk.X, pady=2)
        
        ttk.Separator(button_frame).pack(fill=tk.X, pady=5)
        
        self.merge_button = ttk.Button(
            button_frame,
            text="Merge PDFs",
            command=self._execute_merge,
            state=tk.DISABLED
        )
        self.merge_button.pack(fill=tk.X, pady=2)
        
        return frame
    
    def _create_preview_panel(self) -> ttk.Frame:
        """Create preview panel."""
        frame = ttk.Frame(self)
        
        # Title
        title = ttk.Label(frame, text="Preview", font=('Arial', 12, 'bold'))
        title.pack(pady=5)
        
        # Preview canvas
        self.preview_canvas = tk.Canvas(
            frame,
            width=400,
            height=500,
            bg='gray85'
        )
        self.preview_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Info label
        self.preview_info_label = ttk.Label(
            frame,
            text="Click a file to preview",
            font=('Arial', 10)
        )
        self.preview_info_label.pack(pady=5)
        
        # Button to open full preview
        self.full_preview_button = ttk.Button(
            frame,
            text="Open Full Preview",
            command=self._open_full_preview,
            state=tk.DISABLED
        )
        self.full_preview_button.pack(pady=5)
        
        self.current_preview_file = None
        
        return frame
    
    def _open_folder(self):
        """Open a folder and load all PDFs."""
        folder = filedialog.askdirectory(title="Select Folder Containing PDFs")
        if folder:
            self._load_folder(folder)
    
    def _add_files(self):
        """Add individual PDF files."""
        files = filedialog.askopenfilenames(
            title="Select PDF Files",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        for file in files:
            self._add_file(file)
        self._refresh_file_list()
    
    def _load_folder(self, folder_path: str):
        """
        Load all PDFs from a folder.
        
        Args:
            folder_path: Path to folder
        """
        self.files.clear()
        
        try:
            for filename in os.listdir(folder_path):
                if filename.lower().endswith('.pdf'):
                    filepath = os.path.join(folder_path, filename)
                    self._add_file(filepath)
            
            self._refresh_file_list()
        except Exception as e:
            logger.error(f"Error loading folder: {e}")
            messagebox.showerror("Error", f"Failed to load folder:\n{str(e)}")
    
    def _add_file(self, file_path: str):
        """
        Add a file to the available files.
        
        Args:
            file_path: Path to PDF file
        """
        if file_path not in self.files:
            self.files[file_path] = PDFFileInfo(file_path)
    
    def _refresh_file_list(self):
        """Refresh the file list display."""
        # Clear current list
        self.file_tree.delete(*self.file_tree.get_children())
        
        # Add files
        for file_path, info in sorted(self.files.items(), key=lambda x: x[1].filename):
            self.file_tree.insert(
                '',
                tk.END,
                iid=file_path,
                text=info.filename,
                values=(info.format_size(), info.page_count, info.format_date())
            )
    
    def _on_file_click(self, event):
        """Handle file click."""
        # Get selected item
        item = self.file_tree.identify('item', event.x, event.y)
        if item:
            self._show_preview(item)
    
    def _on_file_double_click(self, event):
        """Handle file double-click - add to merge queue."""
        item = self.file_tree.identify('item', event.x, event.y)
        if item and item in self.files:
            self._add_to_queue(item)
    
    def _on_queue_double_click(self, event):
        """Handle queue double-click - show preview."""
        selection = self.queue_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.merge_queue):
                file_path = self.merge_queue[index]
                self._show_preview(file_path)
    
    def _show_preview(self, file_path: str):
        """
        Show preview of a file.
        
        Args:
            file_path: Path to PDF file
        """
        if file_path not in self.files:
            return
        
        self.current_preview_file = file_path
        info = self.files[file_path]
        
        # Update info label
        self.preview_info_label.config(
            text=f"{info.filename}\n{info.format_size()}, {info.page_count} pages"
        )
        
        # Enable full preview button
        self.full_preview_button.config(state=tk.NORMAL)
        
        # Load thumbnail
        try:
            image = self.preview_generator.get_first_page_thumbnail(
                file_path,
                max_size=(350, 450)
            )
            
            if image:
                photo = ImageTk.PhotoImage(image)
                
                # Clear canvas
                self.preview_canvas.delete("all")
                
                # Center image
                canvas_width = self.preview_canvas.winfo_width()
                canvas_height = self.preview_canvas.winfo_height()
                x = max((canvas_width - photo.width()) // 2, 10)
                y = max((canvas_height - photo.height()) // 2, 10)
                
                self.preview_canvas.create_image(x, y, anchor=tk.NW, image=photo)
                self.preview_canvas.image = photo  # Keep reference
            else:
                # Show placeholder
                self._show_placeholder_preview()
        except Exception as e:
            logger.error(f"Error showing preview: {e}")
            self._show_placeholder_preview()
    
    def _show_placeholder_preview(self):
        """Show placeholder when preview cannot be generated."""
        self.preview_canvas.delete("all")
        self.preview_canvas.create_text(
            200, 250,
            text="Preview not available",
            font=('Arial', 14)
        )
    
    def _open_full_preview(self):
        """Open full preview dialog."""
        if self.current_preview_file:
            PreviewDialog(self, self.current_preview_file)
    
    def _add_to_queue(self, file_path: str):
        """
        Add file to merge queue.
        
        Args:
            file_path: Path to PDF file
        """
        if file_path not in self.merge_queue:
            self.merge_queue.append(file_path)
            self._update_queue_display()
    
    def _remove_from_queue(self):
        """Remove selected file from queue."""
        selection = self.queue_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.merge_queue):
                self.merge_queue.pop(index)
                self._update_queue_display()
    
    def _move_up_in_queue(self):
        """Move selected file up in queue."""
        selection = self.queue_listbox.curselection()
        if selection and selection[0] > 0:
            index = selection[0]
            self.merge_queue[index], self.merge_queue[index - 1] = \
                self.merge_queue[index - 1], self.merge_queue[index]
            self._update_queue_display()
            self.queue_listbox.selection_set(index - 1)
    
    def _move_down_in_queue(self):
        """Move selected file down in queue."""
        selection = self.queue_listbox.curselection()
        if selection and selection[0] < len(self.merge_queue) - 1:
            index = selection[0]
            self.merge_queue[index], self.merge_queue[index + 1] = \
                self.merge_queue[index + 1], self.merge_queue[index]
            self._update_queue_display()
            self.queue_listbox.selection_set(index + 1)
    
    def _clear_queue(self):
        """Clear the merge queue."""
        if self.merge_queue and messagebox.askyesno(
            "Clear Queue",
            "Are you sure you want to clear the merge queue?"
        ):
            self.merge_queue.clear()
            self._update_queue_display()
    
    def _update_queue_display(self):
        """Update the queue listbox display."""
        self.queue_listbox.delete(0, tk.END)
        
        for i, file_path in enumerate(self.merge_queue, 1):
            filename = os.path.basename(file_path)
            self.queue_listbox.insert(tk.END, f"{i}. {filename}")
        
        # Enable/disable merge button
        self.merge_button.config(
            state=tk.NORMAL if len(self.merge_queue) >= 2 else tk.DISABLED
        )
    
    def _execute_merge(self):
        """Execute the merge operation."""
        if len(self.merge_queue) < 2:
            messagebox.showwarning("Warning", "Select at least 2 files to merge")
            return
        
        # Ask for output filename
        output_file = filedialog.asksaveasfilename(
            title="Save Merged PDF As",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if not output_file:
            return
        
        # Perform merge
        try:
            merger = PDFMerger()
            
            # Add files in queue order
            for file_path in self.merge_queue:
                merger.add_pdf(file_path)
            
            # Merge
            result = merger.merge(output_file)
            
            if result:
                messagebox.showinfo(
                    "Success",
                    f"Successfully merged {len(self.merge_queue)} PDFs!\n\n"
                    f"Output: {output_file}"
                )
                
                # Ask if user wants to clear queue
                if messagebox.askyesno("Clear Queue", "Clear the merge queue?"):
                    self.merge_queue.clear()
                    self._update_queue_display()
            else:
                messagebox.showerror("Error", "Merge operation failed")
        except Exception as e:
            logger.error(f"Merge failed: {e}")
            messagebox.showerror("Error", f"Failed to merge PDFs:\n{str(e)}")


def show_merge_screen(parent=None):
    """
    Show the merge screen.
    
    Args:
        parent: Parent widget (creates new window if None)
    """
    if parent is None:
        root = tk.Tk()
        root.title("PDF Merge")
        root.geometry("1200x700")
        screen = MergeScreen(root)
        screen.pack(fill=tk.BOTH, expand=True)
        root.mainloop()
    else:
        screen = MergeScreen(parent)
        screen.pack(fill=tk.BOTH, expand=True)
        return screen
