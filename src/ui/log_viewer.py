"""
Log viewer dialog for viewing application logs.

Allows users to view, search, and manage application logs
directly from the UI.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
from typing import Optional
import os
from ..utils.logger import logger


class LogViewerDialog(tk.Toplevel):
    """
    Dialog for viewing application logs.
    
    Features:
    - View log contents
    - Search logs
    - Clear logs
    - Export logs
    - Auto-refresh
    """
    
    def __init__(self, parent, log_file: Optional[Path] = None):
        """
        Initialize log viewer.
        
        Args:
            parent: Parent window
            log_file: Path to log file. If None, tries to detect from logger
        """
        super().__init__(parent)
        
        self.title("Application Logs")
        self.geometry("800x600")
        self.transient(parent)
        
        self.log_file = log_file
        self.auto_refresh_id = None
        self.auto_refresh_enabled = False
        
        # Try to detect log file from logger if not provided
        if self.log_file is None:
            self.log_file = self._detect_log_file()
        
        self._create_widgets()
        self._layout_widgets()
        self._load_log()
    
    def _detect_log_file(self) -> Optional[Path]:
        """
        Try to detect the log file from the logger.
        
        Returns:
            Path to log file, or None if not found
        """
        # Check if logger has file handlers
        for handler in logger.handlers:
            if hasattr(handler, 'baseFilename'):
                return Path(handler.baseFilename)
        
        # Default location
        return Path.home() / "pdf_manipulate.log"
    
    def _create_widgets(self):
        """Create UI widgets"""
        # Toolbar
        self.toolbar = ttk.Frame(self)
        
        # Refresh button
        self.btn_refresh = ttk.Button(
            self.toolbar,
            text="🔄 Refresh",
            command=self._load_log
        )
        
        # Auto-refresh checkbox
        self.auto_refresh_var = tk.BooleanVar(value=False)
        self.check_auto_refresh = ttk.Checkbutton(
            self.toolbar,
            text="Auto-refresh (5s)",
            variable=self.auto_refresh_var,
            command=self._toggle_auto_refresh
        )
        
        # Search frame
        self.search_frame = ttk.Frame(self.toolbar)
        ttk.Label(self.search_frame, text="Search:").pack(side=tk.LEFT, padx=(10, 5))
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=2)
        self.search_entry.bind('<Return>', lambda e: self._search())
        
        self.btn_search = ttk.Button(
            self.search_frame,
            text="Find",
            command=self._search,
            width=8
        )
        self.btn_search.pack(side=tk.LEFT, padx=2)
        
        # Separator
        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=5)
        
        # Clear button
        self.btn_clear = ttk.Button(
            self.toolbar,
            text="🗑️ Clear Logs",
            command=self._clear_logs
        )
        
        # Export button
        self.btn_export = ttk.Button(
            self.toolbar,
            text="💾 Export",
            command=self._export_logs
        )
        
        # Log text area
        self.text_frame = ttk.Frame(self)
        
        self.log_text = tk.Text(
            self.text_frame,
            wrap=tk.WORD,
            font=("Courier", 9),
            bg="#f5f5f5"
        )
        
        self.scrollbar = ttk.Scrollbar(
            self.text_frame,
            command=self.log_text.yview
        )
        self.log_text.config(yscrollcommand=self.scrollbar.set)
        
        # Configure tags for syntax highlighting
        self.log_text.tag_config("ERROR", foreground="red")
        self.log_text.tag_config("WARNING", foreground="orange")
        self.log_text.tag_config("INFO", foreground="blue")
        self.log_text.tag_config("DEBUG", foreground="gray")
        self.log_text.tag_config("highlight", background="yellow")
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(
            self,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        
        # Bottom buttons
        self.button_frame = ttk.Frame(self)
        
        self.btn_close = ttk.Button(
            self.button_frame,
            text="Close",
            command=self.destroy,
            width=15
        )
    
    def _layout_widgets(self):
        """Layout widgets"""
        # Toolbar
        self.toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.btn_refresh.pack(side=tk.LEFT, padx=2)
        self.check_auto_refresh.pack(side=tk.LEFT, padx=5)
        self.search_frame.pack(side=tk.LEFT, padx=10)
        self.btn_clear.pack(side=tk.RIGHT, padx=2)
        self.btn_export.pack(side=tk.RIGHT, padx=2)
        
        # Text area
        self.text_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status bar
        self.status_label.pack(side=tk.TOP, fill=tk.X, padx=5, pady=(0, 5))
        
        # Bottom buttons
        self.button_frame.pack(side=tk.BOTTOM, pady=5)
        self.btn_close.pack()
    
    def _load_log(self):
        """Load and display log file contents"""
        if not self.log_file or not self.log_file.exists():
            self.log_text.delete("1.0", tk.END)
            self.log_text.insert("1.0", "Log file not found")
            self.status_var.set("Log file not found")
            return
        
        try:
            # Read log file
            with open(self.log_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Clear text area
            self.log_text.delete("1.0", tk.END)
            
            # Insert content with syntax highlighting
            lines = content.split('\n')
            for line in lines:
                # Determine line type and apply tag
                tag = None
                if 'ERROR' in line:
                    tag = "ERROR"
                elif 'WARNING' in line:
                    tag = "WARNING"
                elif 'INFO' in line:
                    tag = "INFO"
                elif 'DEBUG' in line:
                    tag = "DEBUG"
                
                if tag:
                    self.log_text.insert(tk.END, line + '\n', tag)
                else:
                    self.log_text.insert(tk.END, line + '\n')
            
            # Scroll to bottom
            self.log_text.see(tk.END)
            
            # Update status
            file_size = os.path.getsize(self.log_file)
            line_count = len(lines)
            self.status_var.set(
                f"Loaded: {self.log_file.name} ({file_size:,} bytes, {line_count:,} lines)"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load log file:\n{e}")
            self.status_var.set(f"Error: {e}")
    
    def _search(self):
        """Search for text in logs"""
        search_term = self.search_var.get()
        if not search_term:
            return
        
        # Remove previous highlights
        self.log_text.tag_remove("highlight", "1.0", tk.END)
        
        # Search and highlight
        start_pos = "1.0"
        count = 0
        
        while True:
            pos = self.log_text.search(search_term, start_pos, tk.END, nocase=True)
            if not pos:
                break
            
            end_pos = f"{pos}+{len(search_term)}c"
            self.log_text.tag_add("highlight", pos, end_pos)
            start_pos = end_pos
            count += 1
        
        if count > 0:
            # Scroll to first match
            first_pos = self.log_text.search(search_term, "1.0", tk.END, nocase=True)
            self.log_text.see(first_pos)
            self.status_var.set(f"Found {count} occurrence(s)")
        else:
            self.status_var.set("No matches found")
    
    def _clear_logs(self):
        """Clear log file contents"""
        if not messagebox.askyesno(
            "Clear Logs",
            "Are you sure you want to clear all log contents?\n"
            "This action cannot be undone."
        ):
            return
        
        try:
            if self.log_file and self.log_file.exists():
                # Clear file
                with open(self.log_file, 'w', encoding='utf-8') as f:
                    f.write("")
                
                # Reload
                self._load_log()
                self.status_var.set("Logs cleared")
                logger.info("Logs cleared by user")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear logs:\n{e}")
    
    def _export_logs(self):
        """Export logs to a file"""
        filename = filedialog.asksaveasfilename(
            title="Export Logs",
            defaultextension=".log",
            filetypes=[("Log files", "*.log"), ("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"pdf_manipulate_export.log"
        )
        
        if not filename:
            return
        
        try:
            # Copy log file
            if self.log_file and self.log_file.exists():
                with open(self.log_file, 'r', encoding='utf-8') as src:
                    content = src.read()
                
                with open(filename, 'w', encoding='utf-8') as dst:
                    dst.write(content)
                
                self.status_var.set(f"Exported to: {filename}")
                messagebox.showinfo("Export Complete", f"Logs exported to:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export logs:\n{e}")
    
    def _toggle_auto_refresh(self):
        """Toggle auto-refresh"""
        self.auto_refresh_enabled = self.auto_refresh_var.get()
        
        if self.auto_refresh_enabled:
            self._schedule_auto_refresh()
        else:
            if self.auto_refresh_id:
                self.after_cancel(self.auto_refresh_id)
                self.auto_refresh_id = None
    
    def _schedule_auto_refresh(self):
        """Schedule next auto-refresh"""
        if self.auto_refresh_enabled:
            self._load_log()
            self.auto_refresh_id = self.after(5000, self._schedule_auto_refresh)
    
    def destroy(self):
        """Clean up before closing"""
        # Cancel auto-refresh
        if self.auto_refresh_id:
            self.after_cancel(self.auto_refresh_id)
        
        super().destroy()


def show_log_viewer(parent=None, log_file: Optional[Path] = None):
    """
    Show the log viewer dialog.
    
    Args:
        parent: Parent window
        log_file: Path to log file. If None, auto-detects
    
    Returns:
        LogViewerDialog instance
    """
    dialog = LogViewerDialog(parent, log_file)
    return dialog
