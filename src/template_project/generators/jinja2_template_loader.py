"""Jinja2-based template loader with enhanced features."""
import os
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, select_autoescape


class Jinja2TemplateLoader:
    """Loads and processes template files using Jinja2."""

    def __init__(self, template_dir=None):
        if template_dir is None:
            template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
        self.template_dir = os.path.abspath(template_dir)

        # Configure Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True
        )

        # Add custom filters
        self.env.filters['snake_case'] = self._to_snake_case
        self.env.filters['kebab_case'] = self._to_kebab_case
        self.env.filters['title_case'] = self._to_title_case
        self.env.filters['camel_case'] = self._to_camel_case
        self.env.filters['pascal_case'] = self._to_pascal_case

        # Add global functions
        self.env.globals['now'] = datetime.now
        self.env.globals['current_year'] = datetime.now().year

    def load_template(self, filename, **kwargs):
        """Load and render a template with variables.

        Args:
            filename: Name of the template file (e.g., 'README.md.j2')
            **kwargs: Variables to substitute in the template

        Returns:
            str: Processed template content with variables substituted
        """
        try:
            template = self.env.get_template(filename)
            return template.render(**kwargs)
        except Exception as e:
            print(f"Error loading template {filename}: {e}")
            return ""

    def list_templates(self):
        """List all available template files.

        Returns:
            list: List of template filenames
        """
        if not os.path.exists(self.template_dir):
            return []

        return [f for f in os.listdir(self.template_dir)
                if f.endswith('.j2') or f.endswith('.template')]

    def _to_snake_case(self, text):
        """Convert text to snake_case."""
        import re
        # Replace hyphens and spaces with underscores
        text = text.replace('-', '_').replace(' ', '_')
        # Insert underscore before uppercase letters (for CamelCase)
        text = re.sub('([a-z0-9])([A-Z])', r'\1_\2', text)
        return text.lower()

    def _to_kebab_case(self, text):
        """Convert text to kebab-case."""
        import re
        # Replace underscores and spaces with hyphens
        text = text.replace('_', '-').replace(' ', '-')
        # Insert hyphen before uppercase letters (for CamelCase)
        text = re.sub('([a-z0-9])([A-Z])', r'\1-\2', text)
        return text.lower()

    def _to_title_case(self, text):
        """Convert text to Title Case."""
        return text.replace('-', ' ').replace('_', ' ').title()

    def _to_camel_case(self, text):
        """Convert text to camelCase."""
        # Split on common separators
        words = text.replace('-', ' ').replace('_', ' ').split()
        if not words:
            return text
        # First word lowercase, rest title case
        return words[0].lower() + ''.join(word.capitalize() for word in words[1:])

    def _to_pascal_case(self, text):
        """Convert text to PascalCase."""
        # Split on common separators and capitalize each word
        words = text.replace('-', ' ').replace('_', ' ').split()
        return ''.join(word.capitalize() for word in words)
