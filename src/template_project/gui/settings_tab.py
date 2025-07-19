import tkinter as tk
from tkinter.constants import X

import ttkbootstrap as ttkb
from ttkbootstrap.constants import BOTH


class SettingsTab(ttkb.Frame):
    # Map of theme to button color (from ttkbootstrap docs)
    THEME_BUTTON_COLORS = {
        # Light themes
        "litera": {"button_bg": "#007bff", "button_fg": "#fff"},
        "flatly": {"button_bg": "#18bc9c", "button_fg": "#fff"},
        "cosmo": {"button_bg": "#2780e3", "button_fg": "#fff"},
        "journal": {"button_bg": "#eb6864", "button_fg": "#fff"},
        "minty": {"button_bg": "#78c2ad", "button_fg": "#fff"},
        "pulse": {"button_bg": "#593196", "button_fg": "#fff"},
        "sandstone": {"button_bg": "#93c54b", "button_fg": "#fff"},
        "yeti": {"button_bg": "#008cba", "button_fg": "#fff"},
        "cerulean": {"button_bg": "#2fa4e7", "button_fg": "#fff"},
        "morph": {"button_bg": "#6c63ff", "button_fg": "#fff"},
        "simplex": {"button_bg": "#6c757d", "button_fg": "#fff"},
        # Dark themes
        "superhero": {"button_bg": "#375a7f", "button_fg": "#fff"},
        "darkly": {"button_bg": "#222", "button_fg": "#fff"},
        "cyborg": {"button_bg": "#060606", "button_fg": "#fff"},
        "solar": {"button_bg": "#b58900", "button_fg": "#fff"},
        "vapor": {"button_bg": "#ff61e6", "button_fg": "#fff"},
    }

    def _create_custom_theme_styles(self):
        # Always recreate styles to override theme changes
        s = ttkb.Style()
        for theme, colors in self.THEME_BUTTON_COLORS.items():
            style_name = f"{theme}.Custom.TButton"
            s.configure(
                style_name,
                background=colors["button_bg"],
                foreground=colors["button_fg"],
                bordercolor=colors["button_bg"],
                focuscolor=colors["button_bg"],
                lightcolor=colors["button_bg"],
                darkcolor=colors["button_bg"]
            )
            # Also configure the active and pressed states
            s.map(style_name,
                background=[('active', colors["button_bg"]), ('pressed', colors["button_bg"])],
                foreground=[('active', colors["button_fg"]), ('pressed', colors["button_fg"])],
                bordercolor=[('active', colors["button_bg"]), ('pressed', colors["button_bg"])]
            )
    def __init__(self, parent, settings, apply_callback):
        super().__init__(parent)
        self.settings = settings
        self.apply_callback = apply_callback
        self.available_themes = sorted(ttkb.Style().theme_names())
        self.create_widgets()

    # --- Theme color definitions and pairs ---
    THEME_COLORS = {
        # Light themes
        "litera": {"bg": "#f8f9fa", "fg": "#212529"},
        "flatly": {"bg": "#e9ecef", "fg": "#2c3e50"},
        "cosmo": {"bg": "#ffffff", "fg": "#2c3e50"},
        "journal": {"bg": "#f4f4f4", "fg": "#222"},
        "minty": {"bg": "#e6f9f5", "fg": "#2c3e50"},
        "pulse": {"bg": "#f5f5fa", "fg": "#2c3e50"},
        "sandstone": {"bg": "#fdf6e3", "fg": "#2c3e50"},
        "yeti": {"bg": "#f8f9fa", "fg": "#2c3e50"},
        "cerulean": {"bg": "#f0f8ff", "fg": "#2c3e50"},
        "morph": {"bg": "#f8f9fa", "fg": "#2c3e50"},
        "simplex": {"bg": "#ffffff", "fg": "#212529"},
        # Dark themes
        "superhero": {"bg": "#2b3e50", "fg": "#fff"},
        "darkly": {"bg": "#222", "fg": "#fff"},
        "cyborg": {"bg": "#212529", "fg": "#fff"},
        "solar": {"bg": "#282c34", "fg": "#fff"},
        "vapor": {"bg": "#22223b", "fg": "#fff"},
    }
    THEME_PAIRS = {
        "litera": "superhero", "superhero": "litera",
        "flatly": "darkly", "darkly": "flatly",
        "cosmo": "cyborg", "cyborg": "cosmo",
        "journal": "solar", "solar": "journal",
        "minty": "vapor", "vapor": "minty",
        "pulse": "superhero", "cerulean": "darkly",
        "sandstone": "solar", "yeti": "cyborg",
        "morph": "darkly", "simplex": "superhero",
    }
    # Updated to match ttkbootstrap docs
    DARK_THEMES = [
        "superhero", "darkly", "cyborg", "solar", "vapor"
    ]
    LIGHT_THEMES = [
        "litera", "flatly", "cosmo", "journal", "minty", "pulse", "sandstone", "yeti", "cerulean", "morph", "simplex"
    ]
    DEFAULT_LIGHT = "litera"
    DEFAULT_DARK = "superhero"

    def create_widgets(self):
        self._create_custom_theme_styles()
        self.status_var = tk.StringVar()
        self.container = ttkb.Frame(self, padding=20)
        self.container.pack(expand=True, fill=BOTH)

        # --- Python Version Selection ---
        python_version_label = ttkb.Label(self.container, text="Python Version:", font=("-size", 12))
        python_version_label.pack(fill=X, pady=(0, 5))
        self.python_version_var = tk.StringVar(value=self.settings.get("python_version", "3.9"))
        python_versions = ["3.9", "3.10", "3.11", "3.12"]
        python_version_menu = ttkb.Combobox(
            self.container,
            textvariable=self.python_version_var,
            values=python_versions,
            font=("Helvetica", 10),
            state="readonly",
            width=10
        )
        python_version_menu.pack(fill=X, pady=(0, 15))
        def on_python_version_change(*args):
            self.settings["python_version"] = self.python_version_var.get()
            self.apply_callback(self.settings)
            self.status_var.set(f"Python version set to {self.python_version_var.get()}.")
        self.python_version_var.trace_add("write", on_python_version_change)

        # --- Git Repository Initialization ---
        git_label = ttkb.Label(self.container, text="Git Repository:", font=("-size", 12))
        git_label.pack(fill=X, pady=(15, 5))

        self.git_init_var = tk.BooleanVar(value=self.settings.get("git_init", True))
        git_checkbox = ttkb.Checkbutton(
            self.container,
            text="Initialize Git repository with initial commit",
            variable=self.git_init_var
        )
        git_checkbox.pack(fill=X, pady=(0, 15))

        def on_git_init_change(*args):
            self.settings["git_init"] = self.git_init_var.get()
            self.apply_callback(self.settings)
            status_text = (
                "Git initialization enabled" if self.git_init_var.get()
                else "Git initialization disabled"
            )
            self.status_var.set(f"{status_text}.")
        self.git_init_var.trace_add("write", on_git_init_change)

        theme_label = ttkb.Label(self.container, text="Theme:", font=("-size", 12))
        theme_label.pack(fill=X, pady=(0, 5))

        # --- Theme Selection Grid (always create on load) ---
        self.theme_var = tk.StringVar(value=self.settings.get("theme", self.DEFAULT_DARK))
        self._create_theme_grid()
    # Removed mode toggle logic; only theme selection now
    def _create_theme_grid(self):
        # Always re-apply custom styles after a theme change
        self._create_custom_theme_styles()
        # Only create the theme button grid once
        if not hasattr(self, 'grid_frame'):
            self.grid_frame = ttkb.Frame(self.container)
            self.grid_frame.pack(fill=X, pady=(0, 20))
        # Remove any existing buttons from the grid
        if hasattr(self, 'theme_buttons'):
            for _, btn in self.theme_buttons:
                btn.destroy()
        if hasattr(self, 'theme_cells'):
            for cell in self.theme_cells:
                cell.destroy()
        self.theme_buttons = []
        self.theme_cells = []

        # --- Dark Themes Header ---
        dark_label = ttkb.Label(
            self.grid_frame,
            text="Dark Themes",
            font=("Helvetica", 11, "bold")
        )
        dark_label.grid(row=0, column=0, columnspan=5, sticky="w", pady=(0, 2))
        self.theme_cells.append(dark_label)

        # --- Dark themes: 1 row, 5 themes ---
        dark_themes = [t for t in self.DARK_THEMES if t in self.available_themes]
        for col, theme in enumerate(dark_themes):
            style_name = f"{theme}.Custom.TButton"
            btn = ttkb.Button(
                self.grid_frame,
                text=theme,
                width=15,
                style=style_name,
                command=lambda t=theme: self.select_theme(t)
            )
            btn.grid(row=1, column=col, padx=4, pady=4, sticky="ew")
            self.theme_buttons.append((theme, btn))
            self.theme_cells.append(btn)

        # --- Separator ---
        sep = ttkb.Separator(self.grid_frame, orient="horizontal")
        sep.grid(row=2, column=0, columnspan=5, sticky="ew", pady=(8, 8))
        self.theme_cells.append(sep)

        # --- Light Themes Header ---
        light_label = ttkb.Label(
            self.grid_frame,
            text="Light Themes",
            font=("Helvetica", 11, "bold")
        )
        light_label.grid(row=3, column=0, columnspan=5, sticky="w", pady=(0, 2))
        self.theme_cells.append(light_label)

        # --- Light themes: 3 rows, 5 per row (last row remainder) ---
        light_themes = [t for t in self.LIGHT_THEMES if t in self.available_themes]
        for i, theme in enumerate(light_themes):
            row, col = divmod(i, 5)
            style_name = f"{theme}.Custom.TButton"
            btn = ttkb.Button(
                self.grid_frame,
                text=theme,
                width=15,
                style=style_name,
                command=lambda t=theme: self.select_theme(t)
            )
            btn.grid(row=4 + row, column=col, padx=4, pady=4, sticky="ew")
            self.theme_buttons.append((theme, btn))
            self.theme_cells.append(btn)

        # --- Status Label ---
        self.status_var = tk.StringVar()
        self.status_label = ttkb.Label(
            self.container,
            textvariable=self.status_var,
            font=("Helvetica", 10)
        )
        self.status_label.pack(pady=(10, 0))

        # Update theme buttons to show current selection
        self.update_theme_buttons()

    # set_mode removed (no mode switching)

    def select_theme(self, theme):
        # When a theme button is clicked, select exactly that theme
        self.theme_var.set(theme)
        self.settings["theme"] = theme
        self.apply_callback(self.settings)
        self.update_theme_buttons()
        self.status_var.set(f"Theme changed to {theme}.")

    def update_theme_buttons(self):
        # Re-apply custom styles in case theme was changed
        self._create_custom_theme_styles()
        # Update button highlight for selected theme
        if not hasattr(self, 'theme_buttons') or not self.theme_buttons:
            return
        for theme, btn in self.theme_buttons:
            # Always use the custom theme-specific style
            style_name = f"{theme}.Custom.TButton"
            btn.configure(style=style_name)

            if theme == self.theme_var.get():
                # Add visual indication for selected theme (e.g., border or text change)
                btn.configure(text=f"* {theme}")  # Add asterisk indicator
            else:
                # Remove selection indicator
                btn.configure(text=theme)
