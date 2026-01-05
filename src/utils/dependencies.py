"""
Dependency checking utilities
"""

from typing import Optional, Tuple


def check_dependency(module_name: str) -> Tuple[bool, Optional[str]]:
    """
    Check if a dependency is installed.

    Args:
        module_name: Name of the module to check

    Returns:
        Tuple of (is_installed, error_message)
    """
    try:
        __import__(module_name)
        return True, None
    except ImportError:
        error_msg = (
            f"{module_name} is not installed. "
            f"Please install it with: pip install -r requirements.txt"
        )
        return False, error_msg


def require_dependency(module_name: str, feature_name: str = "this feature") -> None:
    """
    Require a dependency and raise an error if not available.

    Args:
        module_name: Name of the required module
        feature_name: Name of the feature that requires this module

    Raises:
        ImportError: If the module is not installed
    """
    is_installed, error_msg = check_dependency(module_name)
    if not is_installed:
        raise ImportError(
            f"{module_name} is required for {feature_name}.\n"
            f"Install it with: pip install -r requirements.txt"
        )


# Check critical dependencies at import
PYPDF2_AVAILABLE, PYPDF2_ERROR = check_dependency("PyPDF2")
PILLOW_AVAILABLE, PILLOW_ERROR = check_dependency("PIL")
FITZ_AVAILABLE, FITZ_ERROR = check_dependency("fitz")
