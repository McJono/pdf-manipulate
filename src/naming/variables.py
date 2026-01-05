"""
Variable handling for naming templates
"""

from datetime import datetime, timedelta
from typing import Dict, Any


class VariableHandler:
    """Handles variable substitution in naming templates"""

    @staticmethod
    def get_date(
        format_str: str = "YYYY-MM-DD",
        offset_days: int = 0
    ) -> str:
        """
        Get formatted date with optional offset.

        Args:
            format_str: Date format string
            offset_days: Number of days to add/subtract

        Returns:
            Formatted date string
        """
        target_date = datetime.now() + timedelta(days=offset_days)

        # Convert custom format to Python strftime format
        format_map = {
            "YYYY": "%Y",
            "YY": "%y",
            "MMMM": "%B",  # Full month name
            "MMM": "%b",   # Abbreviated month name
            "MM": "%m",
            "DD": "%d",
        }

        python_format = format_str
        for custom, python in format_map.items():
            python_format = python_format.replace(custom, python)

        return target_date.strftime(python_format)

    @staticmethod
    def get_timestamp() -> str:
        """
        Get current timestamp.

        Returns:
            Timestamp string in format YYYY-MM-DD_HHMMSS
        """
        return datetime.now().strftime("%Y-%m-%d_%H%M%S")

    @staticmethod
    def get_counter(value: int, padding: int = 3) -> str:
        """
        Get padded counter value.

        Args:
            value: Counter value
            padding: Number of digits (zero-padded)

        Returns:
            Padded counter string
        """
        return str(value).zfill(padding)


def get_available_variables() -> Dict[str, str]:
    """
    Get list of available template variables.

    Returns:
        Dictionary mapping variable names to descriptions
    """
    return {
        "{date}": "Current date",
        "{date+N}": "Date N days from now",
        "{date-N}": "Date N days ago",
        "{timestamp}": "Full timestamp",
        "{name}": "User-provided name",
        "{filename}": "Original filename",
        "{counter}": "Sequential number",
        "{counter:N}": "Sequential number with N digits",
    }
