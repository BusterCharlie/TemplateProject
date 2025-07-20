#!/usr/bin/env python3
"""
Test script to verify the Git initialization functionality.
"""
import os
import sys
import tempfile

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from template_project.generators.project_generator import ProjectGenerator

def test_git_initialization():
    """Test the Git initialization feature."""
    print("Testing Git initialization feature...")

    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        test_project_dir = os.path.join(temp_dir, "test_project")

        # Initialize project generator
        generator = ProjectGenerator()

        # Test project parameters
        author_info = {
            "name": "Test Author",
            "email": "test@example.com",
            "github": "testuser",
            "website": "https://test.com"
        }

        print(f"Creating test project in: {test_project_dir}")

        # Test with Git initialization enabled
        try:
            generator.create_project_structure(
                project_dir=test_project_dir,
                project_name="TestProject",
                project_desc="A test project to verify Git initialization",
                author_info=author_info,
                python_version="3.11",
                git_init=True
            )

            # Check if files were created
            print("\n✅ Project structure created successfully!")

            # Check if specific files exist
            expected_files = [
                ".gitignore",
                ".copilot-instructions.md",
                "dev/README.md",
                "pyproject.toml",
                "README.md",
                "LICENSE"
            ]

            for file_path in expected_files:
                full_path = os.path.join(test_project_dir, file_path)
                if os.path.exists(full_path):
                    print(f"✅ {file_path} created")
                else:
                    print(f"❌ {file_path} missing")

            # Check if git repo was initialized
            git_dir = os.path.join(test_project_dir, ".git")
            if os.path.exists(git_dir):
                print("✅ Git repository initialized")
            else:
                print("❌ Git repository not initialized")

            # Check gitignore content
            gitignore_path = os.path.join(test_project_dir, ".gitignore")
            if os.path.exists(gitignore_path):
                with open(gitignore_path, 'r') as f:
                    content = f.read()
                    if "dev/" in content and "config.json" in content:
                        print("✅ Enhanced .gitignore content verified")
                    else:
                        print("❌ Enhanced .gitignore content missing")

            print(f"\n🎉 Test completed! Project created at: {test_project_dir}")

        except Exception as e:
            print(f"❌ Error during project creation: {e}")
            return False

    return True

if __name__ == "__main__":
    success = test_git_initialization()
    sys.exit(0 if success else 1)
