"""Template loader utility for loading and processing template files."""
import os


class TemplateLoader:
    """Loads and processes template files with variable substitution."""

    def __init__(self, template_dir=None):
        if template_dir is None:
            # Default to templates directory relative to this file
            template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
        self.template_dir = os.path.abspath(template_dir)

    def load_template(self, filename, **kwargs):
        """Load a template file and substitute variables.

        Args:
            filename: Name of the template file (e.g., 'README.md.template')
            **kwargs: Variables to substitute in the template

        Returns:
            str: Processed template content with variables substituted
        """
        template_path = os.path.join(self.template_dir, filename)

        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template file not found: {template_path}")

        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()

        # Use simple string replacement for {variable} placeholders
        result = template_content
        for key, value in kwargs.items():
            placeholder = "{" + key + "}"
            result = result.replace(placeholder, str(value))

        return result

    def list_templates(self):
        """List all available template files.

        Returns:
            list: List of template filenames
        """
        if not os.path.exists(self.template_dir):
            return []

        return [f for f in os.listdir(self.template_dir)
                if f.endswith('.template')]
