"""
Validation utilities for PDF Manipulate
"""

import os
import re
from pathlib import Path
from typing import Union


def is_valid_pdf(file_path: Union[str, Path]) -> bool:
    """
    Check if a file is a valid PDF.

    Args:
        file_path: Path to the file

    Returns:
        True if file exists and is a PDF, False otherwise
    """
    path = Path(file_path)

    # Check if file exists
    if not path.exists() or not path.is_file():
        return False

    # Check file extension
    if path.suffix.lower() != ".pdf":
        return False

    # Check file signature (PDF magic bytes)
    try:
        with open(path, "rb") as f:
            header = f.read(5)
            return header == b"%PDF-"
    except Exception:
        return False


def sanitize_filename(filename: str, max_length: int = 255) -> str:
    """
    Sanitize a filename by removing invalid characters.

    Args:
        filename: Original filename
        max_length: Maximum filename length

    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    # Invalid chars: / \\ : * ? " < > |
    sanitized = re.sub(r'[/\\:*?"<>|]', "", filename)

    # Replace multiple spaces with single space
    sanitized = re.sub(r"\s+", " ", sanitized)

    # Trim whitespace
    sanitized = sanitized.strip()

    # Ensure it's not empty
    if not sanitized:
        sanitized = "unnamed"

    # Truncate if too long
    if len(sanitized) > max_length:
        # Keep extension if present
        path = Path(sanitized)
        if path.suffix:
            max_name_length = max_length - len(path.suffix)
            sanitized = path.stem[:max_name_length] + path.suffix
        else:
            sanitized = sanitized[:max_length]

    return sanitized


def has_write_permission(directory: Union[str, Path]) -> bool:
    """
    Check if we have write permission to a directory.

    Args:
        directory: Path to directory

    Returns:
        True if writable, False otherwise
    """
    path = Path(directory)

    # Create directory if it doesn't exist
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception:
        return False

    return os.access(path, os.W_OK)


def check_disk_space(directory: Union[str, Path], required_mb: int) -> bool:
    """
    Check if there's enough disk space available.

    Args:
        directory: Path to check
        required_mb: Required space in MB

    Returns:
        True if enough space, False otherwise
    """
    try:
        import shutil
        stat = shutil.disk_usage(str(directory))
        # Available space in MB
        available_mb = stat.free / (1024 * 1024)
        return available_mb >= required_mb
    except Exception:
        # If we can't check, assume there's space
        return True


def ensure_extension(filename: str, extension: str = ".pdf") -> str:
    """
    Ensure a filename has the specified extension.
    
    Args:
        filename: The filename to check
        extension: The extension to ensure (with leading dot)
        
    Returns:
        Filename with extension
    """
    if not extension.startswith("."):
        extension = "." + extension
    
    if not filename.lower().endswith(extension.lower()):
        return filename + extension
    
    return filename
