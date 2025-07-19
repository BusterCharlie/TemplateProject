import ttkbootstrap as ttkb

from .gui.home_tab import HomeTab
from .gui.settings_tab import SettingsTab
from .utils import ConfigManager


class MainApplication(ttkb.Window):
    def __init__(self, title, size):
        # Load config first
        self.config_manager = ConfigManager()
        self.settings = self.config_manager.load_config()

        # Set a larger default window size and minimum size
        super().__init__(
            title=title,
            themename=self.settings.get("theme", "superhero"), # Default to a dark theme
            size=(800, 700),
            minsize=(800, 600),
        )

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttkb.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Create tabs
        home_frame = HomeTab(self.notebook, self.settings, config_manager=self.config_manager)
        settings_frame = SettingsTab(self.notebook, self.settings, self.apply_settings)

        # Add tabs to notebook
        self.notebook.add(home_frame, text="Project Generator")
        self.notebook.add(settings_frame, text="Settings")

    def apply_settings(self, new_settings):
        """Apply new settings and update the theme."""
        self.settings.update(new_settings)
        self.config_manager.save_config(self.settings)
        theme_name = self.settings["theme"]
        self.style.theme_use(theme_name)
        # Re-render widgets if theme changes don't apply automatically
        print(f"Theme changed to: {theme_name}")

    def on_closing(self):
        """Handle window closing event."""
        # Don't save settings here - HomeTab already handles config saving
        # self.config_manager.save_config(self.settings)
        self.destroy()

if __name__ == "__main__":
    app = MainApplication(title="Python Project Generator", size=(800, 600))
    app.mainloop()
