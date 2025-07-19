"""Configuration management utilities."""
import json
import os
import tkinter as tk


class ConfigManager:
    """Manages loading and saving of user configuration."""

    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.default_config = {
            # Project fields
            "project_name": "",
            "project_desc": "",
            "output_dir": os.path.expanduser("~/Desktop"),
            "icon_path": "",
            "author_name": "",
            "github": "",
            "email": "",
            "website": "",
            "python_version": "3.9",
            # Theme/settings fields
            "theme": "superhero",
            "mode": "dark"
        }

    def load_config(self):
        """Load configuration from file or return defaults."""
        try:
            abs_path = os.path.abspath(self.config_file)
            if os.path.exists(abs_path):
                with open(abs_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                # Ensure all default keys are present
                for key, value in self.default_config.items():
                    config.setdefault(key, value)
                return config
            else:
                return self.default_config.copy()
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.default_config.copy()



    def get(self, key, default=None):
        config = self.load_config()
        return config.get(key, default)

    def update(self, updates):
        config = self.load_config()
        config.update(updates)
        self.save_config(config)

    def save_config(self, config):
        """Save configuration to file, merging with any existing config to preserve all keys."""
        try:
            abs_path = os.path.abspath(self.config_file)
            print(f"[DEBUG] Writing config to: {abs_path}")
            # Merge with existing config to preserve all keys
            existing = {}
            if os.path.exists(abs_path):
                with open(abs_path, "r", encoding="utf-8") as f:
                    existing = json.load(f)
            merged = existing.copy()
            merged.update(config)
            with open(abs_path, "w", encoding="utf-8") as f:
                json.dump(merged, f, indent=4)
            print(f"[DEBUG] Config successfully written to: {abs_path}")
        except Exception as e:
            print(f"[DEBUG] Error saving config to {abs_path}: {e}")

    def apply_config_to_vars(self, config, var_dict):
        """Apply loaded config to tkinter StringVar objects.

        Args:
            config: Configuration dictionary
            var_dict: Dictionary mapping config keys to StringVar objects
        """
        for key, var in var_dict.items():
            if key in config and isinstance(var, tk.StringVar):
                var.set(config[key])

    def extract_config_from_vars(self, var_dict):
        """Extract configuration from tkinter StringVar objects.

        Args:
            var_dict: Dictionary mapping config keys to StringVar objects

        Returns:
            dict: Configuration dictionary
        """
        config = {}
        for key, var in var_dict.items():
            if isinstance(var, tk.StringVar):
                config[key] = var.get()
        return config
