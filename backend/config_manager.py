"""
Configuration manager for loading, saving, and watching config files
"""
import json
import os
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading


class ConfigManager:
    """Manage button remapping configuration"""

    DEFAULT_CONFIG = {
        "mappings": {
            # Example: "button4": {"type": "click", "button": "middle"}
            # Example: "button5": {"type": "keystroke", "keys": ["cmd", "["]}
        }
    }

    def __init__(self, config_path=None):
        """
        Initialize the config manager

        Args:
            config_path (str): Path to config file. If None, uses default location
        """
        if config_path is None:
            # Default to ~/Library/Application Support/keymap/config.json
            app_support = Path.home() / 'Library' / 'Application Support' / 'keymap'
            app_support.mkdir(parents=True, exist_ok=True)
            config_path = app_support / 'config.json'

        self.config_path = Path(config_path)
        self.config = {}
        self.callbacks = []
        self.observer = None
        self.lock = threading.Lock()

        # Load or create config
        self.load()

    def load(self):
        """Load configuration from file"""
        with self.lock:
            if not self.config_path.exists():
                # Create default config
                self.config = self.DEFAULT_CONFIG.copy()
                self._save_unlocked()  # Use unlocked version since we already have the lock
            else:
                try:
                    with open(self.config_path, 'r') as f:
                        self.config = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"Error loading config: {e}")
                    print("Using default configuration")
                    self.config = self.DEFAULT_CONFIG.copy()
                except Exception as e:
                    print(f"Error reading config file: {e}")
                    self.config = self.DEFAULT_CONFIG.copy()

        return self.config

    def _save_unlocked(self):
        """Internal save method that assumes lock is already held"""
        try:
            # Ensure directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)

            # Write config
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
            raise

    def save(self, config=None):
        """
        Save configuration to file

        Args:
            config (dict): Configuration to save. If None, saves current config
        """
        if config is not None:
            self.config = config

        with self.lock:
            self._save_unlocked()

    def get_config(self):
        """
        Get a copy of the current configuration

        Returns:
            dict: Configuration dictionary
        """
        with self.lock:
            return self.config.copy()

    def get_mapping(self, button):
        """
        Get the mapping for a specific button

        Args:
            button (str): Button identifier (e.g., 'button4')

        Returns:
            dict: Mapping configuration or None
        """
        with self.lock:
            mappings = self.config.get('mappings', {})
            return mappings.get(button)

    def on_change(self, callback):
        """
        Register a callback for config changes

        Args:
            callback (callable): Function to call when config changes
        """
        self.callbacks.append(callback)

    def start_watching(self):
        """Start watching the config file for changes"""
        if self.observer is not None:
            return

        class ConfigFileHandler(FileSystemEventHandler):
            def __init__(self, config_manager):
                self.config_manager = config_manager

            def on_modified(self, event):
                if event.src_path == str(self.config_manager.config_path):
                    print(f"Config file changed, reloading...")
                    self.config_manager.load()
                    # Notify callbacks
                    for callback in self.config_manager.callbacks:
                        try:
                            callback(self.config_manager.config)
                        except Exception as e:
                            print(f"Error in config change callback: {e}")

        self.observer = Observer()
        event_handler = ConfigFileHandler(self)
        self.observer.schedule(
            event_handler,
            str(self.config_path.parent),
            recursive=False
        )
        self.observer.start()

    def stop_watching(self):
        """Stop watching the config file"""
        if self.observer:
            self.observer.stop()
            self.observer.join(timeout=2.0)
            self.observer = None


if __name__ == '__main__':
    # Test the config manager
    import tempfile

    # Create temp config for testing
    temp_dir = Path(tempfile.mkdtemp())
    config_path = temp_dir / 'test_config.json'

    manager = ConfigManager(config_path)

    print("Initial config:")
    print(json.dumps(manager.get_config(), indent=2))

    # Test saving
    test_config = {
        "mappings": {
            "button4": {"type": "click", "button": "middle"},
            "button5": {"type": "keystroke", "keys": ["cmd", "["]}
        }
    }
    manager.save(test_config)

    # Test loading
    manager2 = ConfigManager(config_path)
    print("\nLoaded config:")
    print(json.dumps(manager2.get_config(), indent=2))

    # Test get_mapping
    print("\nbutton4 mapping:")
    print(manager2.get_mapping('button4'))

    print("\nbutton5 mapping:")
    print(manager2.get_mapping('button5'))

    # Cleanup
    config_path.unlink()
    temp_dir.rmdir()
