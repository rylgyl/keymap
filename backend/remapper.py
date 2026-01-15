"""
Core remapping logic that ties together config and event injection
"""
from event_injector import EventInjector
from config_manager import ConfigManager
import threading


class Remapper:
    """Handle button remapping based on configuration"""

    def __init__(self, config_manager, event_injector):
        """
        Initialize the remapper

        Args:
            config_manager (ConfigManager): Configuration manager
            event_injector (EventInjector): Event injector
        """
        self.config_manager = config_manager
        self.event_injector = event_injector
        self.lock = threading.Lock()

        # Listen for config changes
        self.config_manager.on_change(self._on_config_change)

    def _on_config_change(self, new_config):
        """Handle configuration changes"""
        print("Configuration updated, remapping rules reloaded")

    def should_remap(self, button_number):
        """
        Check if a button should be remapped

        Args:
            button_number (int): Button number (e.g., 4, 5)

        Returns:
            bool: True if button has a mapping
        """
        button_key = f"button{button_number}"

        with self.lock:
            mapping = self.config_manager.get_mapping(button_key)
            return mapping is not None

    def remap(self, button_number, position=None):
        """
        Perform button remapping based on current config

        Args:
            button_number (int): Button number that was pressed
            position (tuple): Optional (x, y) cursor position

        Returns:
            bool: True if event was remapped, False if it should pass through
        """
        button_key = f"button{button_number}"

        with self.lock:
            # Get mapping for this button
            mapping = self.config_manager.get_mapping(button_key)

            if not mapping:
                # No mapping, let event pass through
                return False

            action_type = mapping.get('type')

            if action_type == 'click':
                # Remap to a different mouse button
                target_button = mapping.get('button', 'left')
                try:
                    self.event_injector.click(target_button, position)
                    return True
                except Exception as e:
                    print(f"Error injecting click: {e}")
                    return False

            elif action_type == 'keystroke':
                # Remap to a keyboard combination
                keys = mapping.get('keys', [])
                try:
                    self.event_injector.keystroke(keys)
                    return True
                except Exception as e:
                    print(f"Error injecting keystroke: {e}")
                    return False

            elif action_type == 'ignore':
                # Suppress the event
                return True

            else:
                print(f"Unknown action type: {action_type}")
                return False

    def get_current_mappings(self):
        """
        Get current active mappings

        Returns:
            dict: Active button mappings
        """
        config = self.config_manager.get_config()
        return config.get('mappings', {})


if __name__ == '__main__':
    # Test the remapper
    config_manager = ConfigManager()
    event_injector = EventInjector()

    remapper = Remapper(config_manager, event_injector)

    print("Current mappings:")
    mappings = remapper.get_current_mappings()
    print(f"  Active mappings: {mappings}")

    # Set up a test mapping
    test_config = {
        "mappings": {
            "button4": {"type": "click", "button": "middle"},
            "button5": {"type": "keystroke", "keys": ["cmd", "c"]}
        }
    }
    config_manager.save(test_config)

    print("\nTesting remapping...")
    print("Should remap button 4?", remapper.should_remap(4))
    print("Should remap button 3?", remapper.should_remap(3))
