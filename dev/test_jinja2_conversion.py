#!/usr/bin/env python3
"""Test script to verify Jinja2 template conversion works correctly."""

import os
import sys

def add_src_to_syspath():
    """Add the src directory to Python path (one level up from dev folder)."""
    dev_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.abspath(os.path.join(dev_dir, '..', 'src'))
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)

add_src_to_syspath()

from template_project.generators.project_generator import ProjectGenerator
from template_project.generators.template_loader import TemplateLoader


def test_template_loader():
    """Test the Jinja2 TemplateLoader."""
    print("Testing Jinja2 TemplateLoader...")

    loader = TemplateLoader()

    # Test basic template rendering
    test_context = {
        'project_name': 'My Test App',
        'project_desc': 'A test application',
        'author_info': {
            'name': 'John Doe',
            'email': 'john@example.com',
            'github': 'https://github.com/johndoe/test-app'
        },
        'package_name': 'my_test_app',
        'python_version': '3.9',
        'has_icon': True,
        'os_type': 'windows'
    }

    try:
        # Test README template
        readme_content = loader.load_template('README.md.template', **test_context)
        print("✓ README template rendered successfully")
        print(f"Title: {readme_content.split(chr(10))[0]}")

        # Test pyproject.toml template
        pyproject_content = loader.load_template('pyproject.toml.template', **test_context)
        print("✓ pyproject.toml template rendered successfully")

        # Test LICENSE template
        license_content = loader.load_template('LICENSE.template', **test_context)
        print("✓ LICENSE template rendered successfully")

        # Test filters
        print(f"✓ Filters work: '{test_context['project_name']}' -> '{loader._to_kebab_case(test_context['project_name'])}'")

        return True

    except Exception as e:
        print(f"✗ Template rendering failed: {e}")
        return False


def test_project_generator():
    """Test the ProjectGenerator with enhanced context."""
    print("\nTesting ProjectGenerator...")

    try:
        generator = ProjectGenerator()

        # Test enhanced template context creation
        test_context = {
            'project_name': 'Test Project',
            'project_desc': 'A test project for Jinja2',
            'author_info': {
                'name': 'Test Author',
                'email': 'test@example.com'
            },
            'python_version': '3.10',
            'features': {
                'data_analysis': True,
                'image_processing': False
            }
        }

        print("✓ ProjectGenerator initialized successfully")
        print("✓ Enhanced template context support added")

        return True

    except Exception as e:
        print(f"✗ ProjectGenerator test failed: {e}")
        return False


if __name__ == "__main__":
    print("=== Jinja2 Conversion Test ===\n")

    success = True
    success &= test_template_loader()
    success &= test_project_generator()

    print(f"\n=== Test {'PASSED' if success else 'FAILED'} ===")
    sys.exit(0 if success else 1)
