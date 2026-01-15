"""
Accessibility permission checker for macOS
"""
import subprocess
import ctypes
import ctypes.util


class PermissionChecker:
    """Check and request accessibility permissions"""

    @staticmethod
    def is_trusted():
        """
        Check if the application has accessibility permissions

        Returns:
            bool: True if trusted, False otherwise
        """
        try:
            # Load ApplicationServices framework via ctypes
            app_services_path = ctypes.util.find_library('ApplicationServices')
            if not app_services_path:
                # Fallback: Try to create an event tap which will fail without permissions
                try:
                    from Quartz import CGEventTapCreate, kCGHIDEventTap, kCGHeadInsertEventTap, kCGEventTapOptionDefault
                    tap = CGEventTapCreate(
                        kCGHIDEventTap,
                        kCGHeadInsertEventTap,
                        kCGEventTapOptionDefault,
                        0,  # No events
                        lambda *args: None,
                        None
                    )
                    return tap is not None
                except:
                    return False

            app_services = ctypes.cdll.LoadLibrary(app_services_path)
            AXIsProcessTrusted = app_services.AXIsProcessTrusted
            AXIsProcessTrusted.restype = ctypes.c_bool
            return AXIsProcessTrusted()
        except Exception as e:
            print(f"Error checking accessibility permissions: {e}")
            # If we can't check, assume we don't have permissions
            return False

    @staticmethod
    def request_permission():
        """
        Request accessibility permission by opening System Preferences
        """
        # Open System Preferences to Privacy & Security > Accessibility
        try:
            subprocess.run([
                'open',
                'x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility'
            ])
        except Exception as e:
            print(f"Failed to open System Preferences: {e}")

    @staticmethod
    def get_status():
        """
        Get permission status with message

        Returns:
            dict: Status information
        """
        is_trusted = PermissionChecker.is_trusted()
        return {
            'granted': is_trusted,
            'message': 'Accessibility permissions granted' if is_trusted
                      else 'Accessibility permissions required. Please grant permissions in System Preferences.'
        }


if __name__ == '__main__':
    # Test the permission checker
    checker = PermissionChecker()
    status = checker.get_status()
    print(f"Permission Status: {status}")

    if not status['granted']:
        print("Opening System Preferences...")
        checker.request_permission()
