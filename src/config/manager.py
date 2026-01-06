"""
Configuration management for PDF Manipulate
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional
from ..utils.logger import logger


class ConfigManager:
    """Manages application configuration"""

    DEFAULT_CONFIG = {
        "auto_rotation": {
            "enabled": True,
            "confidence_threshold": 0.8,
            "ocr_language": "eng",
            "batch_processing": {"max_concurrent": 3, "show_progress": True},
        },
        "merge": {
            "selection_mode": "click_order",
            "preserve_bookmarks": True,
            "preserve_metadata": True,
            "delete_source_after_merge": False,
        },
        "naming": {
            "templates": [
                "{date+7}_{name}",
                "{name}_{date}",
                "Invoice_{date}_{name}",
            ],
            "date_format": "YYYY-MM-DD",
            "default_template": "{date+7}_{name}",
            "prompt_for_name": True,
            "sanitize_filenames": True,
            "max_filename_length": 255,
        },
        "preview": {
            "thumbnail_size": 200,
            "quality": "medium",
            "cache_enabled": True,
            "cache_size_mb": 100,
        },
        "ui": {
            "theme": "light",
            "window_size": {"width": 1200, "height": 800},
            "remember_window_position": True,
            "show_tooltips": True,
            "keyboard_shortcuts_enabled": True,
        },
        "file_operations": {
            "backup_originals": True,
            "backup_directory": "./backups",
            "compression_level": "medium",
            "validate_pdfs": True,
        },
        "logging": {
            "enabled": True,
            "level": "INFO",
            "log_file": "pdf-manipulate.log",
            "max_log_size_mb": 10,
            "rotate_logs": True,
            "merge_history_file": "merge_history.log",
        },
        "advanced": {
            "max_file_size_mb": 500,
            "memory_limit_mb": 2048,
            "enable_gpu_acceleration": False,
        },
    }

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration manager.

        Args:
            config_path: Path to config file (uses config.json by default)
        """
        self.config_path = Path(config_path or "config.json")
        self.config = self.DEFAULT_CONFIG.copy()
        self.load()

    def load(self) -> None:
        """Load configuration from file."""
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    user_config = json.load(f)
                    self._merge_config(user_config)
                logger.info(f"Loaded configuration from {self.config_path}")
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON in config file: {e}")
                logger.info("Using default configuration")
            except Exception as e:
                logger.error(f"Error loading config: {e}")
                logger.info("Using default configuration")
        else:
            logger.info("Config file not found, using defaults")

    def _merge_config(self, user_config: Dict[str, Any]) -> None:
        """
        Merge user configuration with defaults.

        Args:
            user_config: User configuration dictionary
        """
        for key, value in user_config.items():
            if key in self.config:
                if isinstance(value, dict) and isinstance(self.config[key], dict):
                    self.config[key].update(value)
                else:
                    self.config[key] = value

    def save(self) -> None:
        """Save current configuration to file."""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2)
            logger.info(f"Saved configuration to {self.config_path}")
        except Exception as e:
            logger.error(f"Error saving config: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.

        Args:
            key: Configuration key (can use dot notation, e.g., 'naming.templates')
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key.split(".")
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.

        Args:
            key: Configuration key (can use dot notation)
            value: Value to set
        """
        keys = key.split(".")
        config = self.config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value


# Global config instance
config = ConfigManager()
