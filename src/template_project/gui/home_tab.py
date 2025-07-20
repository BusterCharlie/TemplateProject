import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox

import ttkbootstrap as ttkb

from ..generators import ProjectGenerator
from ..utils import ConfigManager


class HomeTab(ttkb.Frame):
    def __init__(self, parent, settings, config_manager=None):
        super().__init__(parent)
        self.settings = settings
        self.project_generator = ProjectGenerator()
        self.config_manager = config_manager or ConfigManager()
        self._loading_config = False
        self.create_widgets()
        self.load_config()

    # Desired window size (match Settings tab width)
    DESIRED_WIDTH = 820
    DESIRED_HEIGHT = 600

    def create_widgets(self):
        self.master.update_idletasks()
        if hasattr(self.master, 'geometry'):
            self.master.geometry(f"{self.DESIRED_WIDTH}x{self.DESIRED_HEIGHT}")
        if hasattr(self.master, 'minsize'):
            self.master.minsize(self.DESIRED_WIDTH, self.DESIRED_HEIGHT)

        # Center the main frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Only use scroll if content is off screen
        self.container = ttkb.Frame(self)
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        # Project Name
        name_frame = ttkb.Frame(self.container)
        name_frame.pack(fill="x", pady=(10, 5))
        ttkb.Label(name_frame, text="Project Name:", font=("Helvetica", 12)).pack(anchor="w")

        self.project_name_var = tk.StringVar()
        self.project_name_entry = ttkb.Entry(name_frame, textvariable=self.project_name_var, font=("Helvetica", 11))
        self.project_name_entry.pack(fill="x", pady=(5, 0))

        # Label to show the sanitized project name
        self.sanitized_name_var = tk.StringVar()
        self.sanitized_name_label = ttkb.Label(
            name_frame,
            textvariable=self.sanitized_name_var,
            font=("Helvetica", 9, "italic"),
            foreground="#888"
        )
        self.sanitized_name_label.pack(anchor="w", pady=(2, 0))

        def update_sanitized_name(*_):
            raw = self.project_name_var.get()
            sanitized = self.project_generator.sanitize_project_name(raw)
            self.sanitized_name_var.set(f"Sanitized project name: {sanitized}")

        self.project_name_var.trace_add("write", lambda *a: (self.save_config(), update_sanitized_name()))
        update_sanitized_name()

        # Project Description
        desc_frame = ttkb.Frame(self.container)
        desc_frame.pack(fill="x", pady=(0, 10))
        ttkb.Label(desc_frame, text="Project Description:", font=("Helvetica", 12)).pack(anchor="w")
        self.project_desc_var = tk.StringVar()
        self.project_desc_entry = ttkb.Entry(desc_frame, textvariable=self.project_desc_var, font=("Helvetica", 11))
        self.project_desc_entry.pack(fill="x", pady=(5, 0))
        self.project_desc_var.trace_add("write", lambda *a: self.save_config())

        # Output Directory
        dir_frame = ttkb.Frame(self.container)
        dir_frame.pack(fill="x", pady=(0, 10))
        ttkb.Label(dir_frame, text="Output Directory:", font=("Helvetica", 12)).pack(anchor="w")
        dir_select_frame = ttkb.Frame(dir_frame)
        dir_select_frame.pack(fill="x", pady=(5, 0))
        self.output_dir_var = tk.StringVar()
        self.output_dir_entry = ttkb.Entry(dir_select_frame, textvariable=self.output_dir_var, font=("Helvetica", 11))
        self.output_dir_entry.pack(side="left", fill="x", expand=True)
        self.output_dir_var.trace_add("write", lambda *a: self.save_config())
        browse_btn = ttkb.Button(dir_select_frame, text="Browse", command=self.browse_directory)
        browse_btn.pack(side="right", padx=(10, 0))

        # Icon and Author Info side by side
        icon_author_frame = ttkb.Frame(self.container)
        icon_author_frame.pack(fill="x", pady=(10, 10))

        # App Icon (button + preview)
        icon_col = ttkb.Frame(icon_author_frame)
        icon_col.pack(side="left", fill="y", padx=(0, 10))
        ttkb.Label(icon_col, text="App Icon (optional):", font=("Helvetica", 12)).pack(anchor="w")
        self.icon_path_var = tk.StringVar()
        self.icon_image = None
        self.icon_preview_label = ttkb.Label(icon_col)
        self.icon_preview_label.pack(pady=(5, 0))
        icon_btn = ttkb.Button(icon_col, text="Choose Icon", command=self.browse_icon)
        icon_btn.pack(pady=(5, 0))
        ttkb.Label(icon_col, text=".ico, .png, .jpg, .gif", font=("Helvetica", 9)).pack(anchor="w", pady=(2, 0))

        # Author Info
        author_col = ttkb.LabelFrame(icon_author_frame, text="Author Info (Optional)", padding=10)
        author_col.pack(side="left", fill="both", expand=True)
        self.author_name_var = tk.StringVar()
        self.github_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.website_var = tk.StringVar()
        ttkb.Label(author_col, text="Author Name:").grid(row=0, column=0, sticky="w")
        ttkb.Entry(author_col, textvariable=self.author_name_var, font=("Helvetica", 10)).grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        self.author_name_var.trace_add("write", lambda *a: self.save_config())
        ttkb.Label(author_col, text="GitHub Repository:").grid(row=1, column=0, sticky="w")
        ttkb.Entry(author_col, textvariable=self.github_var, font=("Helvetica", 10)).grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        self.github_var.trace_add("write", lambda *a: self.save_config())
        ttkb.Label(author_col, text="Email:").grid(row=2, column=0, sticky="w")
        ttkb.Entry(author_col, textvariable=self.email_var, font=("Helvetica", 10)).grid(row=2, column=1, sticky="ew", padx=5, pady=2)
        self.email_var.trace_add("write", lambda *a: self.save_config())
        ttkb.Label(author_col, text="Website:").grid(row=3, column=0, sticky="w")
        ttkb.Entry(author_col, textvariable=self.website_var, font=("Helvetica", 10)).grid(row=3, column=1, sticky="ew", padx=5, pady=2)
        self.website_var.trace_add("write", lambda *a: self.save_config())
        author_col.columnconfigure(1, weight=1)

        # Generate Button
        # Python version variable (sync with settings)
        self.python_version_var = tk.StringVar(value=self.settings.get("python_version", "3.9"))
        def update_python_version_from_settings(*args):
            # Save to settings and config
            self.settings["python_version"] = self.python_version_var.get()
            self.save_config()
        self.python_version_var.trace_add("write", update_python_version_from_settings)

        # Generate Button (hard-coded green bg, white font)
        style = ttkb.Style()
        style.configure("CustomSuccess.TButton", foreground="#FFFFFF", font=("Helvetica", 11, "bold"))
        generate_btn = ttkb.Button(
            self.container,
            text="Generate Project",
            command=self.generate_project,
            style="CustomSuccess.TButton",
            width=28
        )
        generate_btn.pack(pady=(20, 10))

        # Status
        self.status_var = tk.StringVar(value=f"Ready to generate Python {self.python_version_var.get()} project")
        status_label = ttkb.Label(self.container, textvariable=self.status_var, font=("Helvetica", 10))
        status_label.pack(pady=(5, 0))

        # Update status when python_version_var changes
        def update_status_text(*args):
            self.status_var.set(f"Ready to generate Python {self.python_version_var.get()} project")
        self.python_version_var.trace_add("write", update_status_text)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir_var.set(directory)

    def browse_icon(self):
        filetypes = [
            ("Icon Files", "*.ico *.png *.jpg *.jpeg *.gif"),
            ("All Files", "*.*")
        ]
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.icon_path_var.set(filename)
            self.save_config()
            self.show_icon_preview(filename)
        else:
            self.show_icon_preview(None)

    def show_icon_preview(self, path):
        # Show a preview of the icon or a placeholder

        from PIL import Image, ImageTk
        if not path or not os.path.exists(path):
            # Show a placeholder icon (simple square)
            img = Image.new('RGBA', (32, 32), (200, 200, 200, 255))
            self.icon_image = ImageTk.PhotoImage(img)
        else:
            try:
                img = Image.open(path)
                img.thumbnail((32, 32))
                self.icon_image = ImageTk.PhotoImage(img)
            except Exception:
                img = Image.new('RGBA', (32, 32), (200, 200, 200, 255))
                self.icon_image = ImageTk.PhotoImage(img)
        self.icon_preview_label.configure(image=self.icon_image)

    def validate_project_name(self, name):
        if not name:
            return False, "Project name cannot be empty"

        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_-]*$', name):
            return False, "Project name must start with a letter and contain only letters, numbers, hyphens, and underscores"

        if len(name) > 50:
            return False, "Project name must be 50 characters or less"

        return True, ""

    def generate_project(self):
        project_name = self.project_name_var.get().strip()
        project_desc = self.project_desc_var.get().strip()
        output_dir = self.output_dir_var.get().strip()
        icon_path = self.icon_path_var.get().strip()
        author_name = self.author_name_var.get().strip()
        github = self.github_var.get().strip()
        email = self.email_var.get().strip()
        website = self.website_var.get().strip()
        python_version = self.python_version_var.get().strip() or "3.9"

        # Validate inputs
        is_valid, error_msg = self.validate_project_name(project_name)
        if not is_valid:
            messagebox.showerror("Error", error_msg)
            return

        if not project_desc:
            project_desc = "A Python application built with ttkbootstrap"

        if not os.path.exists(output_dir):
            messagebox.showerror("Error", "Output directory does not exist")
            return

        # Validate icon path if provided
        if icon_path and not os.path.exists(icon_path):
            messagebox.showerror("Error", "Icon file does not exist")
            return

        # Create project directory
        project_dir = os.path.join(output_dir, project_name)
        if os.path.exists(project_dir):
            if not messagebox.askyesno("Directory Exists",
                                     f"Directory '{project_name}' already exists. Overwrite?"):
                return

        try:
            self.status_var.set("Generating project...")
            self.update()

            # Use the modular project generator
            author_info = {
                "name": author_name,
                "github": github,
                "email": email,
                "website": website,
            }
            self.project_generator.create_project_structure(
                project_dir=project_dir,
                project_name=project_name,
                project_desc=project_desc,
                icon_path=icon_path,
                author_info=author_info,
                python_version=python_version,
                git_init=self.settings.get("git_init", True)
            )

            self.status_var.set(f"Project '{project_name}' created successfully!")
            messagebox.showinfo("Success", f"Project created at:\n{project_dir}")

        except Exception as e:
            self.status_var.set("Error occurred during project generation")
            messagebox.showerror("Error", f"Failed to create project: {str(e)}")

    def load_config(self):
        """Load configuration and set UI values"""
        print("[DEBUG] HomeTab.load_config called")
        self._loading_config = True
        # Remove traces to prevent save_config during set
        traces = []
        traces.append((self.project_name_var, self.project_name_var.trace_info()))
        traces.append((self.project_desc_var, self.project_desc_var.trace_info()))
        traces.append((self.output_dir_var, self.output_dir_var.trace_info()))
        traces.append((self.icon_path_var, self.icon_path_var.trace_info()))
        traces.append((self.author_name_var, self.author_name_var.trace_info()))
        traces.append((self.github_var, self.github_var.trace_info()))
        traces.append((self.email_var, self.email_var.trace_info()))
        traces.append((self.website_var, self.website_var.trace_info()))
        # Remove all traces
        for var, info in traces:
            for t in info:
                if t[0] == 'write':
                    var.trace_remove('write', t[1])
        try:
            config = self.config_manager.load_config()
            print(f"[DEBUG] Loaded config: {config}")
            var_dict = {
                'project_name': self.project_name_var,
                'project_desc': self.project_desc_var,
                'output_dir': self.output_dir_var,
                'icon_path': self.icon_path_var,
                'author_name': self.author_name_var,
                'github': self.github_var,
                'email': self.email_var,
                'website': self.website_var,
            }
            # Also load python_version and theme if present
            if 'python_version' in config:
                self.python_version_var.set(config['python_version'])
            if 'theme' in config:
                self.settings['theme'] = config['theme']
            self.config_manager.apply_config_to_vars(config, var_dict)
            # Update all settings fields from config
            if hasattr(self, 'settings') and isinstance(self.settings, dict):
                for k, v in config.items():
                    self.settings[k] = v
            # Show icon preview if available
            self.show_icon_preview(self.icon_path_var.get())
        finally:
            self._loading_config = False
            # Re-add traces
            self.project_name_var.trace_add("write", lambda *a: self.save_config())
            self.project_desc_var.trace_add("write", lambda *a: self.save_config())
            self.output_dir_var.trace_add("write", lambda *a: self.save_config())
            self.icon_path_var.trace_add("write", lambda *a: self.save_config())
            self.author_name_var.trace_add("write", lambda *a: self.save_config())
            self.github_var.trace_add("write", lambda *a: self.save_config())
            self.email_var.trace_add("write", lambda *a: self.save_config())
            self.website_var.trace_add("write", lambda *a: self.save_config())

    def save_config(self):
        """Save current configuration"""
        if self._loading_config:
            print("[DEBUG] save_config called while loading config, skipping.")
            return

        var_dict = {
            'project_name': self.project_name_var,
            'project_desc': self.project_desc_var,
            'output_dir': self.output_dir_var,
            'icon_path': self.icon_path_var,
            'author_name': self.author_name_var,
            'github': self.github_var,
            'email': self.email_var,
            'website': self.website_var,
            'python_version': self.python_version_var,
            'theme': self.settings.get('theme', None),
        }
        config = self.config_manager.extract_config_from_vars(var_dict)
        # Save python_version and theme explicitly
        config['python_version'] = self.python_version_var.get()
        if self.settings.get('theme'):
            config['theme'] = self.settings['theme']
        print(f"[DEBUG] Saving config: {config}")
        self.config_manager.save_config(config)
