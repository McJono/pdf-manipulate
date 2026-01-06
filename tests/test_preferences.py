"""
Tests for preferences manager.
"""

import pytest
import json
import tempfile
from pathlib import Path
from src.config.preferences import PreferencesManager


class TestPreferencesManager:
    """Test preferences manager functionality."""
    
    def test_init_with_defaults(self, tmp_path):
        """Test initialization with default preferences."""
        pref_file = tmp_path / "prefs.json"
        prefs = PreferencesManager(pref_file)
        
        assert prefs.get("window.width") == 1200
        assert prefs.get("window.height") == 800
        assert prefs.get("recent_files") == []
    
    def test_save_and_load(self, tmp_path):
        """Test saving and loading preferences."""
        pref_file = tmp_path / "prefs.json"
        
        # Create and save
        prefs1 = PreferencesManager(pref_file)
        prefs1.set("window.width", 1400)
        prefs1.set("test_key", "test_value")
        assert prefs1.save()
        
        # Load in new instance
        prefs2 = PreferencesManager(pref_file)
        assert prefs2.get("window.width") == 1400
        assert prefs2.get("test_key") == "test_value"
    
    def test_get_with_default(self, tmp_path):
        """Test get with default value."""
        pref_file = tmp_path / "prefs.json"
        prefs = PreferencesManager(pref_file)
        
        assert prefs.get("nonexistent", "default") == "default"
        assert prefs.get("nonexistent.nested", 42) == 42
    
    def test_set_nested_keys(self, tmp_path):
        """Test setting nested keys."""
        pref_file = tmp_path / "prefs.json"
        prefs = PreferencesManager(pref_file)
        
        prefs.set("a.b.c", "value")
        assert prefs.get("a.b.c") == "value"
    
    def test_add_recent_file(self, tmp_path):
        """Test adding recent files."""
        pref_file = tmp_path / "prefs.json"
        prefs = PreferencesManager(pref_file)
        
        # Create temp files
        file1 = tmp_path / "test1.pdf"
        file2 = tmp_path / "test2.pdf"
        file1.touch()
        file2.touch()
        
        # Add files
        prefs.add_recent_file(file1)
        prefs.add_recent_file(file2)
        
        recent = prefs.get_recent_files()
        assert len(recent) == 2
        assert recent[0] == str(file2.absolute())  # Most recent first
        assert recent[1] == str(file1.absolute())
    
    def test_add_recent_file_max_limit(self, tmp_path):
        """Test that recent files are limited."""
        pref_file = tmp_path / "prefs.json"
        prefs = PreferencesManager(pref_file)
        
        # Add more than max_recent files
        for i in range(15):
            file = tmp_path / f"test{i}.pdf"
            file.touch()
            prefs.add_recent_file(file, max_recent=10)
        
        recent = prefs.get_recent_files()
        assert len(recent) == 10
    
    def test_add_recent_file_no_duplicates(self, tmp_path):
        """Test that recent files don't have duplicates."""
        pref_file = tmp_path / "prefs.json"
        prefs = PreferencesManager(pref_file)
        
        file1 = tmp_path / "test.pdf"
        file1.touch()
        
        # Add same file twice
        prefs.add_recent_file(file1)
        prefs.add_recent_file(file1)
        
        recent = prefs.get_recent_files()
        assert len(recent) == 1
    
    def test_get_recent_files_filters_missing(self, tmp_path):
        """Test that missing files are filtered out."""
        pref_file = tmp_path / "prefs.json"
        prefs = PreferencesManager(pref_file)
        
        # Add a file that exists
        file1 = tmp_path / "exists.pdf"
        file1.touch()
        prefs.add_recent_file(file1)
        
        # Manually add a file that doesn't exist
        prefs.set("recent_files", [str(file1), "/nonexistent/file.pdf"])
        
        recent = prefs.get_recent_files()
        assert len(recent) == 1
        assert recent[0] == str(file1)
    
    def test_add_recent_directory(self, tmp_path):
        """Test adding recent directories."""
        pref_file = tmp_path / "prefs.json"
        prefs = PreferencesManager(pref_file)
        
        dir1 = tmp_path / "dir1"
        dir2 = tmp_path / "dir2"
        dir1.mkdir()
        dir2.mkdir()
        
        prefs.add_recent_directory(dir1)
        prefs.add_recent_directory(dir2)
        
        recent = prefs.get_recent_directories()
        assert len(recent) == 2
        assert recent[0] == str(dir2.absolute())
    
    def test_add_custom_template(self, tmp_path):
        """Test adding custom templates."""
        pref_file = tmp_path / "prefs.json"
        prefs = PreferencesManager(pref_file)
        
        prefs.add_custom_template("{date}_{name}.pdf")
        prefs.add_custom_template("{name}_{counter}.pdf")
        
        templates = prefs.get_custom_templates()
        assert len(templates) == 2
        assert "{date}_{name}.pdf" in templates
    
    def test_add_custom_template_no_duplicates(self, tmp_path):
        """Test that custom templates don't have duplicates."""
        pref_file = tmp_path / "prefs.json"
        prefs = PreferencesManager(pref_file)
        
        template = "{date}_{name}.pdf"
        prefs.add_custom_template(template)
        prefs.add_custom_template(template)
        
        templates = prefs.get_custom_templates()
        assert len(templates) == 1
    
    def test_window_geometry(self, tmp_path):
        """Test window geometry saving and loading."""
        pref_file = tmp_path / "prefs.json"
        prefs = PreferencesManager(pref_file)
        
        prefs.set_window_geometry(1400, 900, 100, 50)
        geom = prefs.get_window_geometry()
        
        assert geom["width"] == 1400
        assert geom["height"] == 900
        assert geom["x"] == 100
        assert geom["y"] == 50
