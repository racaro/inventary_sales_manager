import json
import os
import logging

class ConfigManager:
    def __init__(self, base_path):
        self.base_path = base_path
        self.data_dir = os.path.join(base_path, "data")
        self.config_file = os.path.join(self.data_dir, "config.json")

        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)

        # Load or create config
        self.config = self.load_config()

    def load_config(self):
        """Load configuration from JSON file or create default if not exists"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    print(f"Configuration loaded from {self.config_file}")
                    return config
            else:
                # Create default configuration
                default_config = {
                    "initial_stock": {
                        "Sembra 2023": 1850,
                        "Otro": 0
                    },
                    "app_settings": {
                        "auto_save_interval": 30000,
                        "backup_on_startup": True
                    }
                }
                self.save_config(default_config)
                print(f"Default configuration created at {self.config_file}")
                return default_config

        except Exception as e:
            logging.error(f"Error loading config: {e}")
            print(f"Error loading config: {e}")
            # Return default config if there's an error
            return {
                "initial_stock": {
                    "Sembra 2023": 1850,
                    "Otro": 0
                },
                "app_settings": {
                    "auto_save_interval": 30000,
                    "backup_on_startup": True
                }
            }

    def save_config(self, config=None):
        """Save configuration to JSON file"""
        try:
            config_to_save = config if config is not None else self.config
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_to_save, f, indent=2, ensure_ascii=False)
            print(f"Configuration saved to {self.config_file}")

        except Exception as e:
            logging.error(f"Error saving config: {e}")
            print(f"Error saving config: {e}")

    def get_initial_stock(self, product):
        """Get initial stock for a specific product"""
        return self.config.get("initial_stock", {}).get(product, 0)

    def set_initial_stock(self, product, quantity):
        """Set initial stock for a specific product"""
        if "initial_stock" not in self.config:
            self.config["initial_stock"] = {}

        self.config["initial_stock"][product] = quantity
        self.save_config()

    def get_app_setting(self, setting_name, default_value=None):
        """Get application setting"""
        return self.config.get("app_settings", {}).get(setting_name, default_value)

    def set_app_setting(self, setting_name, value):
        """Set application setting"""
        if "app_settings" not in self.config:
            self.config["app_settings"] = {}

        self.config["app_settings"][setting_name] = value
        self.save_config()

    def get_all_initial_stock(self):
        """Get all initial stock data"""
        return self.config.get("initial_stock", {})
