"""
Application context detector - identifies the frontmost application
"""
from AppKit import NSWorkspace
import threading
import time


class AppDetector:
    """Detect the frontmost (active) application"""

    def __init__(self, poll_interval=0.5):
        """
        Initialize the app detector

        Args:
            poll_interval (float): How often to check for app changes (seconds)
        """
        self.workspace = NSWorkspace.sharedWorkspace()
        self.current_app = None
        self.current_bundle_id = None
        self.poll_interval = poll_interval
        self.callbacks = []
        self.running = False
        self.thread = None

    def get_frontmost_app(self):
        """
        Get the currently active (frontmost) application

        Returns:
            dict: Application information with 'name' and 'bundle_id'
        """
        frontmost_app = self.workspace.frontmostApplication()
        if frontmost_app:
            name = frontmost_app.localizedName()
            bundle_id = frontmost_app.bundleIdentifier()
            return {
                'name': name,
                'bundle_id': bundle_id
            }
        return None

    def get_bundle_id(self):
        """
        Get the bundle ID of the frontmost application

        Returns:
            str: Bundle identifier (e.g., 'com.google.Chrome')
        """
        app_info = self.get_frontmost_app()
        return app_info['bundle_id'] if app_info else None

    def on_app_change(self, callback):
        """
        Register a callback to be called when the frontmost app changes

        Args:
            callback (callable): Function to call with (old_bundle_id, new_bundle_id)
        """
        self.callbacks.append(callback)

    def start_monitoring(self):
        """Start monitoring for app changes in a background thread"""
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()

    def stop_monitoring(self):
        """Stop monitoring for app changes"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2.0)

    def _monitor_loop(self):
        """Background thread that monitors for app changes"""
        while self.running:
            try:
                app_info = self.get_frontmost_app()
                if app_info:
                    new_bundle_id = app_info['bundle_id']

                    # Check if app changed
                    if new_bundle_id != self.current_bundle_id:
                        old_bundle_id = self.current_bundle_id
                        self.current_bundle_id = new_bundle_id
                        self.current_app = app_info['name']

                        # Notify callbacks
                        for callback in self.callbacks:
                            try:
                                callback(old_bundle_id, new_bundle_id)
                            except Exception as e:
                                print(f"Error in app change callback: {e}")

                time.sleep(self.poll_interval)
            except Exception as e:
                print(f"Error in app monitoring loop: {e}")
                time.sleep(self.poll_interval)


if __name__ == '__main__':
    # Test the app detector
    detector = AppDetector()

    print("Current frontmost app:")
    app = detector.get_frontmost_app()
    print(f"  Name: {app['name']}")
    print(f"  Bundle ID: {app['bundle_id']}")

    print("\nMonitoring for app changes (switch apps to test)...")

    def on_change(old_id, new_id):
        print(f"App changed: {old_id} -> {new_id}")

    detector.on_app_change(on_change)
    detector.start_monitoring()

    try:
        # Monitor for 30 seconds
        time.sleep(30)
    except KeyboardInterrupt:
        print("\nStopping...")

    detector.stop_monitoring()
