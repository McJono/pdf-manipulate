"""
Template parser for naming system
"""

import re
from typing import Dict, Optional
from .variables import VariableHandler
from ..utils.validators import sanitize_filename
from ..utils.logger import logger


class TemplateParser:
    """Parses and processes naming templates"""

    def __init__(self, date_format: str = "YYYY-MM-DD"):
        """
        Initialize template parser.

        Args:
            date_format: Default date format for {date} variables
        """
        self.date_format = date_format
        self.variable_handler = VariableHandler()
        self.counter = 0

    def parse(
        self,
        template: str,
        user_variables: Optional[Dict[str, str]] = None,
        filename: Optional[str] = None,
    ) -> str:
        """
        Parse a naming template and substitute variables.

        Args:
            template: Template string (e.g., "{date}_{name}.pdf")
            user_variables: Dictionary of user-provided variables
            filename: Original filename for {filename} variable

        Returns:
            Parsed filename string
        """
        if user_variables is None:
            user_variables = {}

        result = template

        # Replace date variables with offset
        # Pattern: {date+7}, {date-30}, etc.
        date_pattern = r'\{date([+\-]\d+)?\}'
        matches = re.finditer(date_pattern, result)

        for match in matches:
            full_match = match.group(0)
            offset_str = match.group(1)

            offset = 0
            if offset_str:
                offset = int(offset_str)

            date_value = self.variable_handler.get_date(self.date_format, offset)
            result = result.replace(full_match, date_value, 1)

        # Replace timestamp
        if "{timestamp}" in result:
            result = result.replace("{timestamp}", self.variable_handler.get_timestamp())

        # Replace counter with optional padding
        # Pattern: {counter:3}, {counter}, etc.
        counter_pattern = r'\{counter(?::(\d+))?\}'
        matches = re.finditer(counter_pattern, result)

        for match in matches:
            full_match = match.group(0)
            padding_str = match.group(1)

            padding = int(padding_str) if padding_str else 3
            counter_value = self.variable_handler.get_counter(self.counter, padding)
            result = result.replace(full_match, counter_value, 1)

        # Replace user variables
        for var_name, var_value in user_variables.items():
            placeholder = f"{{{var_name}}}"
            if placeholder in result:
                result = result.replace(placeholder, var_value)

        # Replace filename
        if filename and "{filename}" in result:
            result = result.replace("{filename}", filename)

        # Sanitize the result
        result = sanitize_filename(result)

        logger.debug(f"Parsed template '{template}' to '{result}'")
        return result

    def increment_counter(self) -> None:
        """Increment the counter for sequential numbering."""
        self.counter += 1

    def reset_counter(self) -> None:
        """Reset the counter to 0."""
        self.counter = 0

    def validate_template(self, template: str) -> bool:
        """
        Validate a template string.

        Args:
            template: Template to validate

        Returns:
            True if valid, False otherwise
        """
        # Check for balanced braces
        open_braces = template.count("{")
        close_braces = template.count("}")

        if open_braces != close_braces:
            logger.error("Template has unbalanced braces")
            return False

        # Check for known variables
        known_vars = [
            "date", "timestamp", "name", "filename", "counter"
        ]

        # Extract all variables
        pattern = r'\{([^}]+)\}'
        variables = re.findall(pattern, template)

        for var in variables:
            # Remove counter padding specification
            var_base = re.sub(r'counter:\d+', 'counter', var)
            # Remove date offset specification
            var_base = re.sub(r'date[+\-]\d+', 'date', var_base)

            if var_base not in known_vars:
                logger.warning(f"Unknown variable in template: {var}")

        return True


def parse_template(
    template: str,
    name: Optional[str] = None,
    filename: Optional[str] = None,
    date_format: str = "YYYY-MM-DD",
) -> str:
    """
    Parse a naming template (convenience function).

    Args:
        template: Template string
        name: User-provided name
        filename: Original filename
        date_format: Date format

    Returns:
        Parsed filename
    """
    parser = TemplateParser(date_format)
    user_vars = {}
    if name:
        user_vars["name"] = name

    return parser.parse(template, user_vars, filename)
