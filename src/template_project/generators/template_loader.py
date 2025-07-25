"""Jinja2-based template loader with enhanced features."""
import os
import re
from datetime import datetime

from jinja2 import Environment, FileSystemLoader


class TemplateLoader:
    """Loads and processes template files using Jinja2."""

    def __init__(self, template_dir=None):
        if template_dir is None:
            # Default to templates directory relative to this file
            template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
        self.template_dir = os.path.abspath(template_dir)

        # Configure Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True
        )

        # Add custom filters
        self.env.filters['snake_case'] = self._to_snake_case
        self.env.filters['kebab_case'] = self._to_kebab_case
        self.env.filters['title_case'] = self._to_title_case
        self.env.filters['class_name'] = self._to_class_name

        # Add global functions
        self.env.globals['now'] = datetime.now
        self.env.globals['current_year'] = datetime.now().year

    def load_template(self, filename, **kwargs):
        """Load and render a template with variables.

        Args:
            filename: Name of the template file (e.g., 'README.md.template')
            **kwargs: Variables to substitute in the template

        Returns:
            str: Processed template content with variables substituted
        """
        import logging
        try:
            template = self.env.get_template(filename)
            return template.render(**kwargs)
        except Exception as e:
            logging.error(f"Error loading template {filename}: {e}")
            return ""

    def list_templates(self):
        """List all available template files.

        Returns:
            list: List of template filenames
        """
        if not os.path.exists(self.template_dir):
            return []

        return [f for f in os.listdir(self.template_dir)
                if f.endswith('.template')]

    def _to_snake_case(self, text):
        """Convert text to snake_case."""
        if not text:
            return ""
        # Replace spaces and hyphens with underscores, then convert to lowercase
        text = re.sub(r'[-\s]+', '_', text)
        # Insert underscore before uppercase letters (except at start)
        text = re.sub(r'(?<!^)(?=[A-Z])', '_', text)
        return text.lower()

    def _to_kebab_case(self, text):
        """Convert text to kebab-case."""
        if not text:
            return ""
        # Replace spaces and underscores with hyphens, then convert to lowercase
        text = re.sub(r'[_\s]+', '-', text)
        # Insert hyphen before uppercase letters (except at start)
        text = re.sub(r'(?<!^)(?=[A-Z])', '-', text)
        return text.lower()

    def _to_title_case(self, text):
        """Convert text to Title Case."""
        if not text:
            return ""
        # Replace hyphens and underscores with spaces
        text = re.sub(r'[-_]+', ' ', text)
        return text.title()

    def _to_class_name(self, text):
        """Convert text to ClassName (PascalCase)."""
        if not text:
            return ""
        # Replace hyphens, underscores, and spaces
        text = re.sub(r'[-_\s]+', ' ', text)
        # Convert to title case and remove spaces
        return ''.join(word.capitalize() for word in text.split())
