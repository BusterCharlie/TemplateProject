#!/usr/bin/env python3
"""Test script to verify main.py template renders correctly."""

import os
import sys

# Add the src directory to Python path (go up one level from dev folder)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from template_project.generators.template_loader import TemplateLoader


def test_main_py_template():
    """Test the main.py template for correct indentation."""
    print("Testing main.py template indentation...")

    loader = TemplateLoader()

    # Test context with icon
    test_context_with_icon = {
        'project_name': 'Test App',
        'project_desc': 'A test application',
        'has_icon': True
    }

    # Test context without icon
    test_context_no_icon = {
        'project_name': 'Test App',
        'project_desc': 'A test application',
        'has_icon': False
    }

    try:
        # Test with icon
        print("\n=== Testing with icon ===")
        main_content_with_icon = loader.load_template('main.py.template', **test_context_with_icon)

        # Check for syntax errors by trying to compile
        compile(main_content_with_icon, '<string>', 'exec')
        print("✓ main.py template with icon compiles successfully")

        # Test without icon
        print("\n=== Testing without icon ===")
        main_content_no_icon = loader.load_template('main.py.template', **test_context_no_icon)

        # Check for syntax errors by trying to compile
        compile(main_content_no_icon, '<string>', 'exec')
        print("✓ main.py template without icon compiles successfully")

        # Show a snippet of the generated code around the problematic area
        print("\n=== Generated code snippet (with icon) ===")
        lines = main_content_with_icon.split('\n')
        for i, line in enumerate(lines[30:45], 31):
            print(f"{i:2}: {line}")

        print("\n=== Generated code snippet (without icon) ===")
        lines = main_content_no_icon.split('\n')
        for i, line in enumerate(lines[30:40], 31):
            print(f"{i:2}: {line}")

        return True

    except SyntaxError as e:
        print(f"✗ Syntax error in generated main.py: {e}")
        print(f"Line {e.lineno}: {e.text}")
        return False
    except Exception as e:
        print(f"✗ Error testing main.py template: {e}")
        return False


if __name__ == "__main__":
    print("=== Main.py Template Test ===\n")

    success = test_main_py_template()

    print(f"\n=== Test {'PASSED' if success else 'FAILED'} ===")
    sys.exit(0 if success else 1)
