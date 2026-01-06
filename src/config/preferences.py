"""
User preferences persistence system.

Handles saving and loading user-specific preferences like:
- Window size and position
- Recent files and directories
- Custom naming templates
- UI state
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from ..utils.logger import logger


class PreferencesManager:
    """
    Manages user preferences persistence.
    
    Preferences are stored separately from configuration to allow
    user-specific customization without modifying the main config.
    """
    
    def __init__(self, preferences_file: Optional[Path] = None):
        """
        Initialize preferences manager.
        
        Args:
            preferences_file: Path to preferences file.
                            Defaults to ~/.pdf_manipulate_preferences.json
        """
        if preferences_file is None:
            home = Path.home()
            preferences_file = home / ".pdf_manipulate_preferences.json"
        
        self.preferences_file = Path(preferences_file)
        self.preferences: Dict[str, Any] = {}
        self._load_preferences()
    
    def _load_preferences(self) -> None:
        """Load preferences from file."""
        try:
            if self.preferences_file.exists():
                with open(self.preferences_file, 'r', encoding='utf-8') as f:
                    self.preferences = json.load(f)
                logger.info(f"Loaded preferences from {self.preferences_file}")
            else:
                logger.info("No preferences file found, using defaults")
                self.preferences = self._get_default_preferences()
        except Exception as e:
            logger.error(f"Error loading preferences: {e}")
            self.preferences = self._get_default_preferences()
    
    def _get_default_preferences(self) -> Dict[str, Any]:
        """Get default preferences."""
        return {
            "window": {
                "width": 1200,
                "height": 800,
                "x": None,  # Will be centered
                "y": None,
            },
            "recent_files": [],
            "recent_directories": [],
            "custom_templates": [],
            "last_output_directory": str(Path.home()),
            "ui_state": {
                "show_tooltips": True,
                "confirm_before_delete": True,
            }
        }
    
    def save(self) -> bool:
        """
        Save preferences to file.
        
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            # Ensure parent directory exists
            self.preferences_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.preferences_file, 'w', encoding='utf-8') as f:
                json.dump(self.preferences, f, indent=2)
            
            logger.info(f"Saved preferences to {self.preferences_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving preferences: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a preference value.
        
        Args:
            key: Dot-notation key (e.g., "window.width")
            default: Default value if key not found
            
        Returns:
            Preference value or default
        """
        keys = key.split('.')
        value = self.preferences
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a preference value.
        
        Args:
            key: Dot-notation key (e.g., "window.width")
            value: Value to set
        """
        keys = key.split('.')
        
        # Navigate to the parent dict
        current = self.preferences
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        # Set the value
        current[keys[-1]] = value
    
    def add_recent_file(self, filepath: Path, max_recent: int = 10) -> None:
        """
        Add a file to recent files list.
        
        Args:
            filepath: Path to file
            max_recent: Maximum number of recent files to keep
        """
        filepath_str = str(filepath.absolute())
        recent = self.get("recent_files", [])
        
        # Remove if already exists
        if filepath_str in recent:
            recent.remove(filepath_str)
        
        # Add to front
        recent.insert(0, filepath_str)
        
        # Trim to max size
        recent = recent[:max_recent]
        
        self.set("recent_files", recent)
    
    def add_recent_directory(self, dirpath: Path, max_recent: int = 10) -> None:
        """
        Add a directory to recent directories list.
        
        Args:
            dirpath: Path to directory
            max_recent: Maximum number of recent directories to keep
        """
        dirpath_str = str(dirpath.absolute())
        recent = self.get("recent_directories", [])
        
        # Remove if already exists
        if dirpath_str in recent:
            recent.remove(dirpath_str)
        
        # Add to front
        recent.insert(0, dirpath_str)
        
        # Trim to max size
        recent = recent[:max_recent]
        
        self.set("recent_directories", recent)
    
    def get_recent_files(self) -> List[str]:
        """
        Get list of recent files.
        
        Returns:
            List of recent file paths (as strings)
        """
        recent = self.get("recent_files", [])
        # Filter out files that no longer exist
        existing = [f for f in recent if Path(f).exists()]
        if len(existing) != len(recent):
            self.set("recent_files", existing)
        return existing
    
    def get_recent_directories(self) -> List[str]:
        """
        Get list of recent directories.
        
        Returns:
            List of recent directory paths (as strings)
        """
        recent = self.get("recent_directories", [])
        # Filter out directories that no longer exist
        existing = [d for d in recent if Path(d).exists()]
        if len(existing) != len(recent):
            self.set("recent_directories", existing)
        return existing
    
    def add_custom_template(self, template: str) -> None:
        """
        Add a custom naming template.
        
        Args:
            template: Template string
        """
        templates = self.get("custom_templates", [])
        if template not in templates:
            templates.append(template)
            self.set("custom_templates", templates)
    
    def get_custom_templates(self) -> List[str]:
        """
        Get list of custom templates.
        
        Returns:
            List of template strings
        """
        return self.get("custom_templates", [])
    
    def set_window_geometry(self, width: int, height: int, x: int, y: int) -> None:
        """
        Save window geometry.
        
        Args:
            width: Window width
            height: Window height
            x: Window x position
            y: Window y position
        """
        self.set("window.width", width)
        self.set("window.height", height)
        self.set("window.x", x)
        self.set("window.y", y)
    
    def get_window_geometry(self) -> Dict[str, Optional[int]]:
        """
        Get saved window geometry.
        
        Returns:
            Dict with width, height, x, y
        """
        return {
            "width": self.get("window.width", 1200),
            "height": self.get("window.height", 800),
            "x": self.get("window.x"),
            "y": self.get("window.y"),
        }


# Global preferences instance
preferences = PreferencesManager()
