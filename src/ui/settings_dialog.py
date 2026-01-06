"""
Settings/Preferences dialog for PDF Manipulate
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from pathlib import Path
from typing import Dict, Any, Optional

from ..config.manager import config
from ..utils.logger import logger


class SettingsDialog:
    """Settings and preferences dialog window"""

    def __init__(self, parent: tk.Tk):
        """
        Initialize settings dialog.
        
        Args:
            parent: Parent window
        """
        self.parent = parent
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Settings - PDF Manipulate")
        self.dialog.geometry("700x600")
        self.dialog.resizable(False, False)
        
        # Center the window
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Store settings widgets
        self.widgets: Dict[str, Any] = {}
        
        # Create UI
        self._create_widgets()
        self._load_current_settings()
        
        logger.info("Settings dialog opened")
    
    def _create_widgets(self) -> None:
        """Create settings dialog widgets"""
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create tabs
        self._create_general_tab()
        self._create_autorotation_tab()
        self._create_merge_tab()
        self._create_naming_tab()
        self._create_preview_tab()
        self._create_advanced_tab()
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(
            button_frame,
            text="Save",
            command=self._save_settings,
            width=15
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Cancel",
            command=self.dialog.destroy,
            width=15
        ).pack(side=tk.RIGHT)
        
        ttk.Button(
            button_frame,
            text="Reset to Defaults",
            command=self._reset_to_defaults,
            width=20
        ).pack(side=tk.LEFT)
    
    def _create_general_tab(self) -> None:
        """Create General settings tab"""
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="General")
        
        # UI Theme
        frame = ttk.LabelFrame(tab, text="User Interface", padding=10)
        frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame, text="Theme:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.widgets["ui.theme"] = ttk.Combobox(
            frame,
            values=["light", "dark"],
            state="readonly",
            width=20
        )
        self.widgets["ui.theme"].grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        
        ttk.Label(frame, text="Window Width:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.widgets["ui.window_size.width"] = ttk.Entry(frame, width=23)
        self.widgets["ui.window_size.width"].grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        
        ttk.Label(frame, text="Window Height:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.widgets["ui.window_size.height"] = ttk.Entry(frame, width=23)
        self.widgets["ui.window_size.height"].grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)
        
        self.widgets["ui.show_tooltips"] = tk.BooleanVar()
        ttk.Checkbutton(
            frame,
            text="Show tooltips",
            variable=self.widgets["ui.show_tooltips"]
        ).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        self.widgets["ui.keyboard_shortcuts_enabled"] = tk.BooleanVar()
        ttk.Checkbutton(
            frame,
            text="Enable keyboard shortcuts",
            variable=self.widgets["ui.keyboard_shortcuts_enabled"]
        ).grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Logging
        log_frame = ttk.LabelFrame(tab, text="Logging", padding=10)
        log_frame.pack(fill=tk.X, pady=5)
        
        self.widgets["logging.enabled"] = tk.BooleanVar()
        ttk.Checkbutton(
            log_frame,
            text="Enable logging",
            variable=self.widgets["logging.enabled"]
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        ttk.Label(log_frame, text="Log Level:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.widgets["logging.level"] = ttk.Combobox(
            log_frame,
            values=["DEBUG", "INFO", "WARNING", "ERROR"],
            state="readonly",
            width=20
        )
        self.widgets["logging.level"].grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        
        ttk.Label(log_frame, text="Log File:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.widgets["logging.log_file"] = ttk.Entry(log_frame, width=23)
        self.widgets["logging.log_file"].grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)
    
    def _create_autorotation_tab(self) -> None:
        """Create Auto-Rotation settings tab"""
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="Auto-Rotation")
        
        frame = ttk.LabelFrame(tab, text="Orientation Detection", padding=10)
        frame.pack(fill=tk.X, pady=5)
        
        self.widgets["auto_rotation.enabled"] = tk.BooleanVar()
        ttk.Checkbutton(
            frame,
            text="Enable auto-rotation",
            variable=self.widgets["auto_rotation.enabled"]
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        ttk.Label(frame, text="Confidence Threshold:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.widgets["auto_rotation.confidence_threshold"] = ttk.Entry(frame, width=23)
        self.widgets["auto_rotation.confidence_threshold"].grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        ttk.Label(
            frame,
            text="(0.0 - 1.0, higher = more strict)",
            font=("Arial", 8)
        ).grid(row=2, column=1, sticky=tk.W, padx=10)
        
        ttk.Label(frame, text="OCR Language:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.widgets["auto_rotation.ocr_language"] = ttk.Entry(frame, width=23)
        self.widgets["auto_rotation.ocr_language"].grid(row=3, column=1, sticky=tk.W, padx=10, pady=5)
        ttk.Label(
            frame,
            text="(e.g., 'eng', 'fra', 'deu')",
            font=("Arial", 8)
        ).grid(row=4, column=1, sticky=tk.W, padx=10)
        
        # Batch Processing
        batch_frame = ttk.LabelFrame(tab, text="Batch Processing", padding=10)
        batch_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(batch_frame, text="Max Concurrent Jobs:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.widgets["auto_rotation.batch_processing.max_concurrent"] = ttk.Entry(batch_frame, width=23)
        self.widgets["auto_rotation.batch_processing.max_concurrent"].grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        
        self.widgets["auto_rotation.batch_processing.show_progress"] = tk.BooleanVar()
        ttk.Checkbutton(
            batch_frame,
            text="Show progress during batch processing",
            variable=self.widgets["auto_rotation.batch_processing.show_progress"]
        ).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
    
    def _create_merge_tab(self) -> None:
        """Create Merge settings tab"""
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="Merge")
        
        frame = ttk.LabelFrame(tab, text="Merge Options", padding=10)
        frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame, text="Selection Mode:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.widgets["merge.selection_mode"] = ttk.Combobox(
            frame,
            values=["click_order", "manual_reorder"],
            state="readonly",
            width=20
        )
        self.widgets["merge.selection_mode"].grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        
        self.widgets["merge.preserve_bookmarks"] = tk.BooleanVar()
        ttk.Checkbutton(
            frame,
            text="Preserve bookmarks/TOC when merging",
            variable=self.widgets["merge.preserve_bookmarks"]
        ).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        self.widgets["merge.preserve_metadata"] = tk.BooleanVar()
        ttk.Checkbutton(
            frame,
            text="Preserve metadata from source files",
            variable=self.widgets["merge.preserve_metadata"]
        ).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        self.widgets["merge.delete_source_after_merge"] = tk.BooleanVar()
        ttk.Checkbutton(
            frame,
            text="Delete source files after successful merge",
            variable=self.widgets["merge.delete_source_after_merge"]
        ).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
    
    def _create_naming_tab(self) -> None:
        """Create Naming settings tab"""
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="Naming")
        
        frame = ttk.LabelFrame(tab, text="Naming Templates", padding=10)
        frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame, text="Date Format:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.widgets["naming.date_format"] = ttk.Combobox(
            frame,
            values=["YYYY-MM-DD", "DD-MM-YYYY", "MM-DD-YYYY", "YYYY/MM/DD"],
            width=20
        )
        self.widgets["naming.date_format"].grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        
        ttk.Label(frame, text="Default Template:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.widgets["naming.default_template"] = ttk.Entry(frame, width=23)
        self.widgets["naming.default_template"].grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        
        self.widgets["naming.prompt_for_name"] = tk.BooleanVar()
        ttk.Checkbutton(
            frame,
            text="Always prompt for name variable",
            variable=self.widgets["naming.prompt_for_name"]
        ).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        self.widgets["naming.sanitize_filenames"] = tk.BooleanVar()
        ttk.Checkbutton(
            frame,
            text="Sanitize filenames (remove invalid characters)",
            variable=self.widgets["naming.sanitize_filenames"]
        ).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        ttk.Label(frame, text="Max Filename Length:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.widgets["naming.max_filename_length"] = ttk.Entry(frame, width=23)
        self.widgets["naming.max_filename_length"].grid(row=4, column=1, sticky=tk.W, padx=10, pady=5)
    
    def _create_preview_tab(self) -> None:
        """Create Preview settings tab"""
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="Preview")
        
        frame = ttk.LabelFrame(tab, text="Preview Options", padding=10)
        frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame, text="Thumbnail Size (px):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.widgets["preview.thumbnail_size"] = ttk.Entry(frame, width=23)
        self.widgets["preview.thumbnail_size"].grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        
        ttk.Label(frame, text="Quality:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.widgets["preview.quality"] = ttk.Combobox(
            frame,
            values=["low", "medium", "high"],
            state="readonly",
            width=20
        )
        self.widgets["preview.quality"].grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        
        self.widgets["preview.cache_enabled"] = tk.BooleanVar()
        ttk.Checkbutton(
            frame,
            text="Enable preview caching (improves performance)",
            variable=self.widgets["preview.cache_enabled"]
        ).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        ttk.Label(frame, text="Cache Size (MB):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.widgets["preview.cache_size_mb"] = ttk.Entry(frame, width=23)
        self.widgets["preview.cache_size_mb"].grid(row=3, column=1, sticky=tk.W, padx=10, pady=5)
    
    def _create_advanced_tab(self) -> None:
        """Create Advanced settings tab"""
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="Advanced")
        
        # File Operations
        file_frame = ttk.LabelFrame(tab, text="File Operations", padding=10)
        file_frame.pack(fill=tk.X, pady=5)
        
        self.widgets["file_operations.backup_originals"] = tk.BooleanVar()
        ttk.Checkbutton(
            file_frame,
            text="Backup original files before modifications",
            variable=self.widgets["file_operations.backup_originals"]
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        ttk.Label(file_frame, text="Backup Directory:").grid(row=1, column=0, sticky=tk.W, pady=5)
        backup_frame = ttk.Frame(file_frame)
        backup_frame.grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        
        self.widgets["file_operations.backup_directory"] = ttk.Entry(backup_frame, width=18)
        self.widgets["file_operations.backup_directory"].pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            backup_frame,
            text="Browse...",
            command=self._browse_backup_directory,
            width=8
        ).pack(side=tk.LEFT)
        
        self.widgets["file_operations.validate_pdfs"] = tk.BooleanVar()
        ttk.Checkbutton(
            file_frame,
            text="Validate PDFs before processing",
            variable=self.widgets["file_operations.validate_pdfs"]
        ).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Performance
        perf_frame = ttk.LabelFrame(tab, text="Performance", padding=10)
        perf_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(perf_frame, text="Max File Size (MB):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.widgets["advanced.max_file_size_mb"] = ttk.Entry(perf_frame, width=23)
        self.widgets["advanced.max_file_size_mb"].grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        
        ttk.Label(perf_frame, text="Memory Limit (MB):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.widgets["advanced.memory_limit_mb"] = ttk.Entry(perf_frame, width=23)
        self.widgets["advanced.memory_limit_mb"].grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
    
    def _browse_backup_directory(self) -> None:
        """Browse for backup directory"""
        directory = filedialog.askdirectory(title="Select Backup Directory")
        if directory:
            self.widgets["file_operations.backup_directory"].delete(0, tk.END)
            self.widgets["file_operations.backup_directory"].insert(0, directory)
    
    def _load_current_settings(self) -> None:
        """Load current settings into widgets"""
        # General tab
        self.widgets["ui.theme"].set(config.get("ui.theme", "light"))
        
        window_size = config.get("ui.window_size", {"width": 1200, "height": 800})
        self.widgets["ui.window_size.width"].insert(0, str(window_size.get("width", 1200)))
        self.widgets["ui.window_size.height"].insert(0, str(window_size.get("height", 800)))
        
        self.widgets["ui.show_tooltips"].set(config.get("ui.show_tooltips", True))
        self.widgets["ui.keyboard_shortcuts_enabled"].set(
            config.get("ui.keyboard_shortcuts_enabled", True)
        )
        
        self.widgets["logging.enabled"].set(config.get("logging.enabled", True))
        self.widgets["logging.level"].set(config.get("logging.level", "INFO"))
        self.widgets["logging.log_file"].insert(0, config.get("logging.log_file", "pdf-manipulate.log"))
        
        # Auto-rotation tab
        self.widgets["auto_rotation.enabled"].set(config.get("auto_rotation.enabled", True))
        self.widgets["auto_rotation.confidence_threshold"].insert(
            0, str(config.get("auto_rotation.confidence_threshold", 0.8))
        )
        self.widgets["auto_rotation.ocr_language"].insert(
            0, config.get("auto_rotation.ocr_language", "eng")
        )
        
        batch_config = config.get("auto_rotation.batch_processing", {})
        self.widgets["auto_rotation.batch_processing.max_concurrent"].insert(
            0, str(batch_config.get("max_concurrent", 3))
        )
        self.widgets["auto_rotation.batch_processing.show_progress"].set(
            batch_config.get("show_progress", True)
        )
        
        # Merge tab
        self.widgets["merge.selection_mode"].set(config.get("merge.selection_mode", "click_order"))
        self.widgets["merge.preserve_bookmarks"].set(config.get("merge.preserve_bookmarks", True))
        self.widgets["merge.preserve_metadata"].set(config.get("merge.preserve_metadata", True))
        self.widgets["merge.delete_source_after_merge"].set(
            config.get("merge.delete_source_after_merge", False)
        )
        
        # Naming tab
        self.widgets["naming.date_format"].set(config.get("naming.date_format", "YYYY-MM-DD"))
        self.widgets["naming.default_template"].insert(
            0, config.get("naming.default_template", "{date+7}_{name}")
        )
        self.widgets["naming.prompt_for_name"].set(config.get("naming.prompt_for_name", True))
        self.widgets["naming.sanitize_filenames"].set(config.get("naming.sanitize_filenames", True))
        self.widgets["naming.max_filename_length"].insert(
            0, str(config.get("naming.max_filename_length", 255))
        )
        
        # Preview tab
        self.widgets["preview.thumbnail_size"].insert(
            0, str(config.get("preview.thumbnail_size", 200))
        )
        self.widgets["preview.quality"].set(config.get("preview.quality", "medium"))
        self.widgets["preview.cache_enabled"].set(config.get("preview.cache_enabled", True))
        self.widgets["preview.cache_size_mb"].insert(
            0, str(config.get("preview.cache_size_mb", 100))
        )
        
        # Advanced tab
        self.widgets["file_operations.backup_originals"].set(
            config.get("file_operations.backup_originals", True)
        )
        self.widgets["file_operations.backup_directory"].insert(
            0, config.get("file_operations.backup_directory", "./backups")
        )
        self.widgets["file_operations.validate_pdfs"].set(
            config.get("file_operations.validate_pdfs", True)
        )
        
        self.widgets["advanced.max_file_size_mb"].insert(
            0, str(config.get("advanced.max_file_size_mb", 500))
        )
        self.widgets["advanced.memory_limit_mb"].insert(
            0, str(config.get("advanced.memory_limit_mb", 2048))
        )
    
    def _save_settings(self) -> None:
        """Save settings to configuration file"""
        try:
            # Build new configuration dictionary
            new_config = {}
            
            # General
            new_config["ui"] = {
                "theme": self.widgets["ui.theme"].get(),
                "window_size": {
                    "width": int(self.widgets["ui.window_size.width"].get()),
                    "height": int(self.widgets["ui.window_size.height"].get())
                },
                "show_tooltips": self.widgets["ui.show_tooltips"].get(),
                "keyboard_shortcuts_enabled": self.widgets["ui.keyboard_shortcuts_enabled"].get()
            }
            
            new_config["logging"] = {
                "enabled": self.widgets["logging.enabled"].get(),
                "level": self.widgets["logging.level"].get(),
                "log_file": self.widgets["logging.log_file"].get(),
                # Keep existing values for fields not in UI
                "max_log_size_mb": config.get("logging.max_log_size_mb", 10),
                "rotate_logs": config.get("logging.rotate_logs", True),
                "merge_history_file": config.get("logging.merge_history_file", "merge_history.log")
            }
            
            # Auto-rotation
            new_config["auto_rotation"] = {
                "enabled": self.widgets["auto_rotation.enabled"].get(),
                "confidence_threshold": float(
                    self.widgets["auto_rotation.confidence_threshold"].get()
                ),
                "ocr_language": self.widgets["auto_rotation.ocr_language"].get(),
                "batch_processing": {
                    "max_concurrent": int(
                        self.widgets["auto_rotation.batch_processing.max_concurrent"].get()
                    ),
                    "show_progress": self.widgets["auto_rotation.batch_processing.show_progress"].get()
                }
            }
            
            # Merge
            new_config["merge"] = {
                "selection_mode": self.widgets["merge.selection_mode"].get(),
                "preserve_bookmarks": self.widgets["merge.preserve_bookmarks"].get(),
                "preserve_metadata": self.widgets["merge.preserve_metadata"].get(),
                "delete_source_after_merge": self.widgets["merge.delete_source_after_merge"].get()
            }
            
            # Naming
            new_config["naming"] = {
                "templates": config.get("naming.templates", []),  # Keep existing templates
                "date_format": self.widgets["naming.date_format"].get(),
                "default_template": self.widgets["naming.default_template"].get(),
                "prompt_for_name": self.widgets["naming.prompt_for_name"].get(),
                "sanitize_filenames": self.widgets["naming.sanitize_filenames"].get(),
                "max_filename_length": int(self.widgets["naming.max_filename_length"].get())
            }
            
            # Preview
            new_config["preview"] = {
                "thumbnail_size": int(self.widgets["preview.thumbnail_size"].get()),
                "quality": self.widgets["preview.quality"].get(),
                "cache_enabled": self.widgets["preview.cache_enabled"].get(),
                "cache_size_mb": int(self.widgets["preview.cache_size_mb"].get())
            }
            
            # File operations
            new_config["file_operations"] = {
                "backup_originals": self.widgets["file_operations.backup_originals"].get(),
                "backup_directory": self.widgets["file_operations.backup_directory"].get(),
                "validate_pdfs": self.widgets["file_operations.validate_pdfs"].get(),
                "compression_level": config.get("file_operations.compression_level", "medium")
            }
            
            # Advanced
            new_config["advanced"] = {
                "max_file_size_mb": int(self.widgets["advanced.max_file_size_mb"].get()),
                "memory_limit_mb": int(self.widgets["advanced.memory_limit_mb"].get()),
                "enable_gpu_acceleration": config.get("advanced.enable_gpu_acceleration", False)
            }
            
            # Validate and save
            self._validate_config(new_config)
            
            # Update config manager
            for key, value in self._flatten_dict(new_config).items():
                config.set(key, value)
            
            # Save to file
            config.save()
            
            messagebox.showinfo(
                "Settings Saved",
                "Settings have been saved successfully.\n\n"
                "Some changes may require restarting the application."
            )
            
            logger.info("Settings saved successfully")
            self.dialog.destroy()
            
        except ValueError as e:
            messagebox.showerror(
                "Invalid Value",
                f"Please check your input:\n\n{str(e)}"
            )
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            messagebox.showerror(
                "Error",
                f"Failed to save settings:\n\n{str(e)}"
            )
    
    def _validate_config(self, config_dict: Dict[str, Any]) -> None:
        """
        Validate configuration values.
        
        Args:
            config_dict: Configuration dictionary to validate
        
        Raises:
            ValueError: If validation fails
        """
        # Validate confidence threshold
        threshold = config_dict["auto_rotation"]["confidence_threshold"]
        if not (0.0 <= threshold <= 1.0):
            raise ValueError("Confidence threshold must be between 0.0 and 1.0")
        
        # Validate window size
        width = config_dict["ui"]["window_size"]["width"]
        height = config_dict["ui"]["window_size"]["height"]
        if width < 800 or height < 600:
            raise ValueError("Window size must be at least 800x600")
        
        # Validate max concurrent jobs
        max_concurrent = config_dict["auto_rotation"]["batch_processing"]["max_concurrent"]
        if max_concurrent < 1 or max_concurrent > 10:
            raise ValueError("Max concurrent jobs must be between 1 and 10")
        
        # Validate thumbnail size
        thumb_size = config_dict["preview"]["thumbnail_size"]
        if thumb_size < 50 or thumb_size > 500:
            raise ValueError("Thumbnail size must be between 50 and 500 pixels")
        
        # Validate cache size
        cache_size = config_dict["preview"]["cache_size_mb"]
        if cache_size < 10 or cache_size > 1000:
            raise ValueError("Cache size must be between 10 and 1000 MB")
        
        # Validate max filename length
        max_length = config_dict["naming"]["max_filename_length"]
        if max_length < 50 or max_length > 255:
            raise ValueError("Max filename length must be between 50 and 255")
    
    def _flatten_dict(self, d: Dict[str, Any], parent_key: str = '') -> Dict[str, Any]:
        """
        Flatten nested dictionary with dot notation keys.
        
        Args:
            d: Dictionary to flatten
            parent_key: Parent key prefix
        
        Returns:
            Flattened dictionary
        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    def _reset_to_defaults(self) -> None:
        """Reset all settings to defaults"""
        result = messagebox.askyesno(
            "Reset to Defaults",
            "Are you sure you want to reset all settings to defaults?\n\n"
            "This will discard any custom configuration."
        )
        
        if result:
            try:
                # Load default config from example file
                example_path = Path(__file__).parent.parent.parent / "config.example.json"
                
                if example_path.exists():
                    with open(example_path, 'r') as f:
                        default_config = json.load(f)
                    
                    # Update config manager
                    for key, value in self._flatten_dict(default_config).items():
                        config.set(key, value)
                    
                    # Save to file
                    config.save()
                    
                    # Reload widgets
                    self.dialog.destroy()
                    SettingsDialog(self.parent)
                    
                    messagebox.showinfo(
                        "Reset Complete",
                        "Settings have been reset to defaults."
                    )
                    logger.info("Settings reset to defaults")
                else:
                    messagebox.showerror(
                        "Error",
                        "Could not find default configuration file."
                    )
                    
            except Exception as e:
                logger.error(f"Error resetting settings: {e}")
                messagebox.showerror(
                    "Error",
                    f"Failed to reset settings:\n\n{str(e)}"
                )


def show_settings_dialog(parent: tk.Tk) -> None:
    """
    Show settings dialog.
    
    Args:
        parent: Parent window
    """
    SettingsDialog(parent)
