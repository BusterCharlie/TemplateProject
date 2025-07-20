"""Project generator module for creating new Python projects."""
import logging
import os
import shutil
import subprocess

from PIL import Image

from .template_loader import TemplateLoader

# Configure module logger
logger = logging.getLogger(__name__)


class ProjectGenerator:
    """Handles generation of new Python projects from templates."""

    def __init__(self):
        self.template_loader = TemplateLoader()

    def create_project_structure(self, project_dir, project_name, project_desc,
                               icon_path=None, author_info=None, python_version="3.9",
                               git_init=True, **kwargs):
        """Create the complete project structure.

        Args:
            project_dir: Directory where the project will be created
            project_name: Name of the project
            project_desc: Description of the project
            icon_path: Optional path to icon file
            author_info: Dictionary with author information
            python_version: Python version requirement
            git_init: Whether to initialize a git repository
            **kwargs: Additional template variables (features, project_type, etc.)
        """
        package_name = project_name.replace('-', '_')

        # Enhanced template context for Jinja2
        template_context = {
            'project_name': project_name,
            'project_desc': project_desc,
            'python_version': python_version,
            'author_info': author_info or {},
            'package_name': package_name,
            'os_type': 'windows' if os.name == 'nt' else 'unix',
            'git_init': git_init,
            'has_icon': bool(icon_path),
            **kwargs  # Include any additional template variables
        }

        # Create main directories
        os.makedirs(project_dir)
        os.makedirs(os.path.join(project_dir, "src", package_name))
        os.makedirs(os.path.join(project_dir, "src", package_name, "gui"))
        os.makedirs(os.path.join(project_dir, "src", package_name, "assets"))
        os.makedirs(os.path.join(project_dir, "tests"))
        os.makedirs(os.path.join(project_dir, ".github"))
        # Create dev folder for temporary/testing files (excluded from git)
        os.makedirs(os.path.join(project_dir, "dev"))

        # Create dev folder README
        dev_readme_content = self.template_loader.load_template(
            'dev_readme.md.template',
            **template_context
        )
        dev_readme_path = os.path.join(project_dir, "dev", "README.md")
        with open(dev_readme_path, "w", encoding="utf-8") as f:
            f.write(dev_readme_content)

        # Copy and convert icon if provided
        if icon_path:
            self._process_icon(icon_path, project_dir, package_name)

        # Generate all project files with enhanced context
        self._generate_pyproject_toml(project_dir, template_context)
        self._generate_readme(project_dir, template_context)
        self._generate_gitignore(project_dir, template_context)
        self._generate_license(project_dir, template_context)
        self._generate_run_scripts(project_dir, template_context)
        self._generate_source_files(project_dir, template_context)
        self._generate_copilot_instructions(project_dir, template_context)

        # Initialize git repository if requested
        if git_init:
            self._initialize_git_repository(project_dir, author_info)

    def _process_icon(self, icon_path, project_dir, package_name):
        """Process and copy the icon file."""
        icon_filename = "icon.ico"
        dest_path = os.path.join(project_dir, "src", package_name, "assets", icon_filename)
        ext = os.path.splitext(icon_path)[1].lower()

        if ext == ".ico":
            shutil.copy2(icon_path, dest_path)
        else:
            # Convert to square, resize, and save as .ico
            img = Image.open(icon_path)
            # Crop to square
            min_side = min(img.size)
            left = (img.width - min_side) // 2
            top = (img.height - min_side) // 2
            right = left + min_side
            bottom = top + min_side
            img = img.crop((left, top, right, bottom))
            # Resize to 256x256 for ICO
            try:
                # Try newer PIL version
                img = img.resize((256, 256), Image.Resampling.LANCZOS)
            except AttributeError:
                # Fall back to older PIL version
                img = img.resize((256, 256))
            img.save(dest_path, format="ICO")

    def _generate_pyproject_toml(self, project_dir, template_context):
        """Generate pyproject.toml file."""
        content = self.template_loader.load_template(
            'pyproject.toml.template',
            **template_context
        )

        pyproject_path = os.path.join(project_dir, "pyproject.toml")
        with open(pyproject_path, "w", encoding="utf-8") as f:
            f.write(content)

    def _generate_readme(self, project_dir, template_context):
        """Generate README.md file."""
        content = self.template_loader.load_template(
            'README.md.template',
            **template_context
        )

        with open(os.path.join(project_dir, "README.md"), "w") as f:
            f.write(content)

    def _generate_gitignore(self, project_dir, template_context):
        """Generate .gitignore file."""
        content = self.template_loader.load_template(
            '.gitignore.template',
            **template_context
        )
        with open(os.path.join(project_dir, ".gitignore"), "w") as f:
            f.write(content)

    def _generate_license(self, project_dir, template_context):
        """Generate LICENSE file."""
        content = self.template_loader.load_template(
            'LICENSE.template',
            **template_context
        )

        with open(os.path.join(project_dir, "LICENSE"), "w") as f:
            f.write(content)

    def _generate_run_scripts(self, project_dir, template_context):
        """Generate run.bat and run.sh scripts."""
        # Windows batch script
        bat_content = self.template_loader.load_template(
            'run.bat.template',
            **template_context
        )
        with open(os.path.join(project_dir, "run.bat"), "w") as f:
            f.write(bat_content)

        # Unix shell script
        sh_content = self.template_loader.load_template(
            'run.sh.template',
            **template_context
        )
        with open(os.path.join(project_dir, "run.sh"), "w") as f:
            f.write(sh_content)

    def _generate_source_files(self, project_dir, template_context):
        """Generate all source files."""
        package_name = template_context['package_name']

        # Create __init__.py files
        with open(os.path.join(project_dir, "src", package_name, "__init__.py"), "w") as f:
            f.write("")

        with open(os.path.join(project_dir, "src", package_name, "gui", "__init__.py"), "w") as f:
            f.write("")

        # Create config.py
        config_content = self.template_loader.load_template(
            'config.py.template',
            **template_context
        )
        with open(os.path.join(project_dir, "src", package_name, "config.py"), "w") as f:
            f.write(config_content)

        # Create main.py
        main_content = self.template_loader.load_template(
            'main.py.template',
            **template_context
        )
        with open(os.path.join(project_dir, "src", package_name, "main.py"), "w") as f:
            f.write(main_content)

        # Create __main__.py for module execution
        main_module_content = self.template_loader.load_template(
            '__main__.py.template',
            **template_context
        )
        with open(os.path.join(project_dir, "src", package_name, "__main__.py"), "w") as f:
            f.write(main_module_content)

        # Create home_tab.py
        home_tab_content = self.template_loader.load_template(
            'home_tab.py.template',
            **template_context
        )
        with open(os.path.join(project_dir, "src", package_name, "gui", "home_tab.py"), "w") as f:
            f.write(home_tab_content)

        # Create settings_tab.py
        settings_tab_content = self.template_loader.load_template(
            'settings_tab.py.template',
            **template_context
        )
        with open(os.path.join(project_dir, "src", package_name, "gui", "settings_tab.py"), "w") as f:
            f.write(settings_tab_content)

        # Create basic test file
        test_content = self.template_loader.load_template(
            'test_main.py.template',
            **template_context
        )
        with open(os.path.join(project_dir, "tests", "test_main.py"), "w") as f:
            f.write(test_content)

    def _generate_copilot_instructions(self, project_dir, template_context):
        """Generate GitHub Copilot instructions file in .github folder."""
        copilot_content = self.template_loader.load_template(
            '.copilot-instructions.md.template',
            **template_context
        )
        copilot_file_path = os.path.join(
            project_dir, ".github", ".copilot-instructions.md"
        )
        with open(copilot_file_path, "w", encoding="utf-8") as f:
            f.write(copilot_content)

    def _initialize_git_repository(self, project_dir, author_info=None):
        """Initialize a git repository with initial commit.

        Args:
            project_dir: Directory where the project is located
            author_info: Dictionary with author information for git config
        """
        try:
            # Change to project directory
            original_cwd = os.getcwd()
            os.chdir(project_dir)

            logger.info(f"Initializing git repository in {project_dir}")

            # Initialize git repository
            subprocess.run(["git", "init"], check=True, capture_output=True)

            # Configure git user if author info provided
            if author_info:
                if author_info.get("name"):
                    subprocess.run(
                        ["git", "config", "user.name", author_info["name"]],
                        check=True, capture_output=True
                    )
                if author_info.get("email"):
                    subprocess.run(
                        ["git", "config", "user.email", author_info["email"]],
                        check=True, capture_output=True
                    )

            # Add all files to staging
            subprocess.run(["git", "add", "."], check=True, capture_output=True)

            # Create initial commit
            subprocess.run(
                ["git", "commit", "-m", "Initial project setup from template"],
                check=True, capture_output=True
            )

            logger.info("Git repository initialized successfully with initial commit")

        except subprocess.CalledProcessError as e:
            logger.warning(f"Failed to initialize git repository: {e}")
        except FileNotFoundError:
            logger.warning("Git not found in PATH. Skipping git initialization.")
        finally:
            # Always return to original directory
            os.chdir(original_cwd)
