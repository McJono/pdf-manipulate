"""
Naming dialog for intelligent file naming with template support
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict, Callable
import os
import logging

from ..naming.parser import TemplateParser
from ..config.manager import config

logger = logging.getLogger(__name__)


class NamingDialog(tk.Toplevel):
    """Dialog for inputting file name using templates"""
    
    def __init__(
        self,
        parent: tk.Widget,
        title: str = "Name File",
        default_filename: Optional[str] = None,
        on_save: Optional[Callable[[str], bool]] = None
    ):
        """
        Initialize naming dialog.
        
        Args:
            parent: Parent widget
            title: Dialog title
            default_filename: Default filename (without extension)
            on_save: Callback function that receives filename and returns success status
        """
        super().__init__(parent)
        self.title(title)
        self.result = None
        self.default_filename = default_filename
        self.on_save = on_save
        
        # Get configuration
        self.templates = config.get("naming.templates", ["{date+7}_{name}"])
        self.date_format = config.get("naming.date_format", "YYYY-MM-DD")
        self.default_template = config.get("naming.default_template", "{date+7}_{name}")
        
        # Initialize parser
        self.parser = TemplateParser(date_format=self.date_format)
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        
        # Create UI
        self._create_widgets()
        
        # Center on parent
        self._center_on_parent(parent)
        
        # Update preview on init
        self._update_preview()
        
    def _center_on_parent(self, parent: tk.Widget) -> None:
        """Center dialog on parent window"""
        self.update_idletasks()
        
        # Get parent position and size
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        # Get dialog size
        dialog_width = self.winfo_width()
        dialog_height = self.winfo_height()
        
        # Calculate position
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        self.geometry(f"+{x}+{y}")
        
    def _create_widgets(self) -> None:
        """Create dialog widgets"""
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Template selection
        template_label = ttk.Label(main_frame, text="Naming Template:")
        template_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.template_var = tk.StringVar(value=self.default_template)
        self.template_combo = ttk.Combobox(
            main_frame,
            textvariable=self.template_var,
            values=self.templates,
            width=40,
            state="readonly"
        )
        self.template_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        self.template_combo.bind("<<ComboboxSelected>>", lambda e: self._update_preview())
        
        # Template info label
        info_text = (
            "Available variables: {date}, {date+N}, {date-N}, {name}, "
            "{filename}, {timestamp}, {counter}"
        )
        info_label = ttk.Label(
            main_frame,
            text=info_text,
            font=('TkDefaultFont', 8),
            foreground='gray'
        )
        info_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Name input (for {name} variable)
        name_label = ttk.Label(main_frame, text="Name:")
        name_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        self.name_var = tk.StringVar()
        if self.default_filename:
            # Extract name from default filename (remove extension)
            base_name = os.path.splitext(self.default_filename)[0]
            self.name_var.set(base_name)
        
        name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=42)
        name_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        name_entry.bind('<KeyRelease>', lambda e: self._update_preview())
        name_entry.focus()
        
        # Preview section
        preview_label = ttk.Label(main_frame, text="Preview:")
        preview_label.grid(row=3, column=0, sticky=tk.W, pady=(10, 5))
        
        preview_frame = ttk.Frame(main_frame, relief=tk.SUNKEN, borderwidth=1)
        preview_frame.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=(10, 5))
        
        self.preview_var = tk.StringVar(value="")
        preview_display = ttk.Label(
            preview_frame,
            textvariable=self.preview_var,
            font=('TkDefaultFont', 10, 'bold'),
            foreground='blue',
            padding=5
        )
        preview_display.pack(fill=tk.BOTH, expand=True)
        
        # Validation message
        self.validation_var = tk.StringVar(value="")
        validation_label = ttk.Label(
            main_frame,
            textvariable=self.validation_var,
            foreground='red',
            font=('TkDefaultFont', 8)
        )
        validation_label.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        
        save_button = ttk.Button(
            button_frame,
            text="Save",
            command=self._on_save_clicked,
            width=10
        )
        save_button.pack(side=tk.LEFT, padx=(0, 5))
        
        cancel_button = ttk.Button(
            button_frame,
            text="Cancel",
            command=self._on_cancel_clicked,
            width=10
        )
        cancel_button.pack(side=tk.LEFT)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        
        # Bind Enter and Escape keys
        self.bind('<Return>', lambda e: self._on_save_clicked())
        self.bind('<Escape>', lambda e: self._on_cancel_clicked())
        
    def _update_preview(self) -> None:
        """Update the filename preview"""
        template = self.template_var.get()
        name = self.name_var.get()
        
        try:
            # Validate template
            if not self.parser.validate_template(template):
                self.validation_var.set("Invalid template format")
                self.preview_var.set("(invalid)")
                return
            
            # Parse template
            user_vars = {}
            if name:
                user_vars["name"] = name
            
            filename = self.default_filename or "file"
            preview = self.parser.parse(
                template,
                user_variables=user_vars,
                filename=filename
            )
            
            # Add .pdf extension if not present
            if not preview.lower().endswith('.pdf'):
                preview += '.pdf'
            
            self.preview_var.set(preview)
            self.validation_var.set("")
            
        except Exception as e:
            logger.error(f"Error generating preview: {e}")
            self.preview_var.set("(error)")
            self.validation_var.set(f"Error: {str(e)}")
    
    def _on_save_clicked(self) -> None:
        """Handle save button click"""
        preview = self.preview_var.get()
        
        # Validate
        if not preview or preview in ["(invalid)", "(error)"]:
            messagebox.showerror(
                "Invalid Filename",
                "Please correct the template or inputs before saving."
            )
            return
        
        # Check if name is required but empty
        template = self.template_var.get()
        if "{name}" in template and not self.name_var.get():
            messagebox.showerror(
                "Name Required",
                "The selected template requires a name to be entered."
            )
            return
        
        # Call save callback if provided
        if self.on_save:
            success = self.on_save(preview)
            if not success:
                return  # Don't close dialog on failure
        
        self.result = preview
        self.destroy()
    
    def _on_cancel_clicked(self) -> None:
        """Handle cancel button click"""
        self.result = None
        self.destroy()
    
    def get_result(self) -> Optional[str]:
        """
        Get the dialog result.
        
        Returns:
            Filename if saved, None if cancelled
        """
        return self.result


def show_naming_dialog(
    parent: tk.Widget,
    title: str = "Name File",
    default_filename: Optional[str] = None,
    on_save: Optional[Callable[[str], bool]] = None
) -> Optional[str]:
    """
    Show naming dialog and return result.
    
    Args:
        parent: Parent widget
        title: Dialog title
        default_filename: Default filename
        on_save: Callback for save operation
        
    Returns:
        Filename if saved, None if cancelled
    """
    dialog = NamingDialog(parent, title, default_filename, on_save)
    parent.wait_window(dialog)
    return dialog.get_result()
