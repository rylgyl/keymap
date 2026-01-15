"""
Event tap for capturing mouse and keyboard events using CGEventTap
"""
from Quartz import (
    CGEventTapCreate, CGEventTapEnable, CFMachPortCreateRunLoopSource,
    CFRunLoopGetCurrent, CFRunLoopAddSource, CFRunLoopRun, CFRunLoopStop,
    CGEventGetIntegerValueField, CGEventGetLocation,
    kCFRunLoopCommonModes, kCGHIDEventTap, kCGHeadInsertEventTap,
    kCGEventTapOptionDefault, kCGEventOtherMouseDown, kCGEventOtherMouseUp,
    kCGEventLeftMouseDown, kCGEventRightMouseDown,
    kCGMouseEventButtonNumber, kCGEventKeyDown
)
import threading
import time


class EventTap:
    """Capture and filter mouse/keyboard events"""

    def __init__(self, remapper=None):
        """
        Initialize the event tap

        Args:
            remapper (Remapper): Optional remapper instance for automatic remapping
        """
        self.remapper = remapper
        self.tap = None
        self.run_loop_source = None
        self.thread = None
        self.running = False
        self.detection_mode = False
        self.detection_callbacks = []

    def _create_event_tap(self):
        """Create the CGEventTap"""
        # Event mask for the events we want to monitor
        # We're primarily interested in "other" mouse buttons (4, 5, etc.)
        event_mask = (
            (1 << kCGEventOtherMouseDown) |
            (1 << kCGEventOtherMouseUp) |
            (1 << kCGEventLeftMouseDown) |
            (1 << kCGEventRightMouseDown)
        )

        # Create the event tap
        tap = CGEventTapCreate(
            kCGHIDEventTap,              # Tap at the HID level (hardware events)
            kCGHeadInsertEventTap,       # Insert at head of event queue
            kCGEventTapOptionDefault,    # Active filter (can modify events)
            event_mask,                  # Event mask
            self._event_callback,        # Callback function
            None                         # User data (not needed in Python)
        )

        return tap

    def _event_callback(self, proxy, event_type, event, refcon):
        """
        Callback function for event tap

        Args:
            proxy: Event tap proxy
            event_type: Type of event
            event: The event object
            refcon: User data (unused)

        Returns:
            The event (to pass it through) or None (to suppress it)
        """
        try:
            # Get button number and position
            button_number = CGEventGetIntegerValueField(event, kCGMouseEventButtonNumber)
            position = CGEventGetLocation(event)

            # Only process button down events
            if event_type == kCGEventOtherMouseDown:
                # In detection mode, notify listeners instead of remapping
                if self.detection_mode:
                    for callback in self.detection_callbacks:
                        try:
                            callback({
                                'button': button_number,
                                'position': (position.x, position.y)
                            })
                        except Exception as e:
                            print(f"Error in detection callback: {e}")
                    # Suppress the event in detection mode
                    return None

                # Normal remapping mode
                if self.remapper:
                    # Check if this button should be remapped
                    if self.remapper.should_remap(button_number):
                        # Remap the button
                        success = self.remapper.remap(button_number, (position.x, position.y))
                        if success:
                            # Suppress the original event
                            return None

            # Pass through the event if not remapped
            return event

        except Exception as e:
            print(f"Error in event callback: {e}")
            # On error, pass through the event
            return event

    def start(self):
        """Start the event tap in a background thread"""
        if self.running:
            print("Event tap already running")
            return

        print("Starting event tap...")
        self.running = True
        self.thread = threading.Thread(target=self._run_event_tap, daemon=True)
        self.thread.start()

        # Wait a bit for the thread to start
        time.sleep(0.5)

    def stop(self):
        """Stop the event tap"""
        if not self.running:
            return

        print("Stopping event tap...")
        self.running = False

        # Stop the run loop
        if self.run_loop_source:
            try:
                CFRunLoopStop(CFRunLoopGetCurrent())
            except:
                pass

        # Wait for thread to finish
        if self.thread:
            self.thread.join(timeout=2.0)

        # Cleanup
        if self.tap:
            CGEventTapEnable(self.tap, False)
            self.tap = None

        self.run_loop_source = None

    def _run_event_tap(self):
        """Run the event tap in its own run loop (blocking)"""
        try:
            # Create the event tap
            self.tap = self._create_event_tap()

            if not self.tap:
                print("Failed to create event tap. Make sure you have accessibility permissions.")
                self.running = False
                return

            # Create a run loop source
            self.run_loop_source = CFMachPortCreateRunLoopSource(None, self.tap, 0)

            # Add to the current run loop
            run_loop = CFRunLoopGetCurrent()
            CFRunLoopAddSource(run_loop, self.run_loop_source, kCFRunLoopCommonModes)

            # Enable the tap
            CGEventTapEnable(self.tap, True)

            print("Event tap started successfully")

            # Run the run loop (this blocks)
            CFRunLoopRun()

        except Exception as e:
            print(f"Error running event tap: {e}")
        finally:
            self.running = False
            print("Event tap stopped")

    def set_detection_mode(self, enabled):
        """
        Enable or disable button detection mode

        Args:
            enabled (bool): True to enable detection mode
        """
        self.detection_mode = enabled
        if enabled:
            print("Button detection mode enabled")
        else:
            print("Button detection mode disabled")

    def on_button_detected(self, callback):
        """
        Register a callback for button detection events

        Args:
            callback (callable): Function to call with button info dict
        """
        self.detection_callbacks.append(callback)

    def is_running(self):
        """Check if the event tap is running"""
        return self.running


if __name__ == '__main__':
    # Test the event tap
    from permission_checker import PermissionChecker

    # Check permissions
    checker = PermissionChecker()
    if not checker.is_trusted():
        print("Accessibility permissions not granted!")
        print("Opening System Preferences...")
        checker.request_permission()
        print("Please grant permissions and run again.")
        exit(1)

    print("Testing event tap (press buttons 4, 5, etc. or Ctrl+C to stop)...")

    def on_detected(button_info):
        print(f"Detected: Button {button_info['button']} at position {button_info['position']}")

    tap = EventTap()
    tap.set_detection_mode(True)
    tap.on_button_detected(on_detected)
    tap.start()

    try:
        # Keep running until interrupted
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping...")

    tap.stop()
