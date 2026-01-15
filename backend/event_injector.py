"""
Event injection for simulating mouse clicks and keyboard inputs
"""
from Quartz import (
    CGEventCreateMouseEvent, CGEventCreateKeyboardEvent,
    CGEventPost, CGEventCreate, CGEventGetLocation,
    kCGSessionEventTap, kCGMouseButtonLeft, kCGMouseButtonRight, kCGMouseButtonCenter,
    kCGEventLeftMouseDown, kCGEventLeftMouseUp,
    kCGEventRightMouseDown, kCGEventRightMouseUp,
    kCGEventOtherMouseDown, kCGEventOtherMouseUp,
    kCGEventKeyDown, kCGEventKeyUp,
    kCGEventSourceStateHIDSystemState, CGEventSourceCreate,
    kCGHIDEventTap, CGEventSetIntegerValueField, kCGKeyboardEventKeycode, CGEventSetFlags
)
import time


class EventInjector:
    """Inject mouse and keyboard events"""

    # Keycode mapping for common modifier keys and characters
    KEYCODE_MAP = {
        # Modifiers
        'cmd': 55,
        'command': 55,
        'shift': 56,
        'option': 58,
        'alt': 58,
        'control': 59,
        'ctrl': 59,
        'fn': 63,
        'capslock': 57,

        # Common keys
        'a': 0, 'b': 11, 'c': 8, 'd': 2, 'e': 14, 'f': 3, 'g': 5, 'h': 4,
        'i': 34, 'j': 38, 'k': 40, 'l': 37, 'm': 46, 'n': 45, 'o': 31,
        'p': 35, 'q': 12, 'r': 15, 's': 1, 't': 17, 'u': 32, 'v': 9,
        'w': 13, 'x': 7, 'y': 16, 'z': 6,

        # Numbers
        '0': 29, '1': 18, '2': 19, '3': 20, '4': 21, '5': 23,
        '6': 22, '7': 26, '8': 28, '9': 25,

        # Special characters
        '[': 33, ']': 30, '\\': 42, ';': 41, "'": 39, ',': 43,
        '.': 47, '/': 44, '`': 50, '-': 27, '=': 24,

        # Function keys
        'f1': 122, 'f2': 120, 'f3': 99, 'f4': 118, 'f5': 96, 'f6': 97,
        'f7': 98, 'f8': 100, 'f9': 101, 'f10': 109, 'f11': 103, 'f12': 111,

        # Navigation
        'space': 49, 'return': 36, 'enter': 36, 'tab': 48, 'delete': 51,
        'backspace': 51, 'escape': 53, 'esc': 53,
        'up': 126, 'down': 125, 'left': 123, 'right': 124,
        'pageup': 116, 'pagedown': 121, 'home': 115, 'end': 119,
    }

    # Modifier flag values
    MODIFIER_FLAGS = {
        'cmd': 0x00100000,      # kCGEventFlagMaskCommand
        'command': 0x00100000,
        'shift': 0x00020000,    # kCGEventFlagMaskShift
        'option': 0x00080000,   # kCGEventFlagMaskAlternate
        'alt': 0x00080000,
        'control': 0x00040000,  # kCGEventFlagMaskControl
        'ctrl': 0x00040000,
    }

    def __init__(self):
        """Initialize the event injector"""
        # Create event source - use HID state to avoid triggering our own event tap
        self.event_source = CGEventSourceCreate(kCGEventSourceStateHIDSystemState)

    def click(self, button='left', position=None):
        """
        Simulate a mouse click

        Args:
            button (str): 'left', 'right', or 'middle'
            position (tuple): Optional (x, y) position. If None, uses current cursor position
        """
        # Get current cursor position if not specified
        if position is None:
            current_event = CGEventCreate(None)
            position = CGEventGetLocation(current_event)

        # Map button to event types and button constants
        button_map = {
            'left': (kCGEventLeftMouseDown, kCGEventLeftMouseUp, kCGMouseButtonLeft),
            'right': (kCGEventRightMouseDown, kCGEventRightMouseUp, kCGMouseButtonRight),
            'middle': (kCGEventOtherMouseDown, kCGEventOtherMouseUp, kCGMouseButtonCenter),
        }

        if button not in button_map:
            raise ValueError(f"Invalid button: {button}. Must be 'left', 'right', or 'middle'")

        down_event_type, up_event_type, button_constant = button_map[button]

        # Create and post mouse down event
        down_event = CGEventCreateMouseEvent(
            self.event_source,
            down_event_type,
            position,
            button_constant
        )
        CGEventPost(kCGSessionEventTap, down_event)

        # Small delay to simulate real click
        time.sleep(0.01)

        # Create and post mouse up event
        up_event = CGEventCreateMouseEvent(
            self.event_source,
            up_event_type,
            position,
            button_constant
        )
        CGEventPost(kCGSessionEventTap, up_event)

    def keystroke(self, keys):
        """
        Simulate a keyboard keystroke or combination

        Args:
            keys (list): List of keys to press (e.g., ['cmd', '['] for CMD+[)
        """
        if not keys:
            return

        # Separate modifiers from regular keys
        modifiers = []
        regular_keys = []

        for key in keys:
            key_lower = key.lower()
            if key_lower in ['cmd', 'command', 'shift', 'option', 'alt', 'control', 'ctrl']:
                modifiers.append(key_lower)
            else:
                regular_keys.append(key_lower)

        # Calculate modifier flags
        modifier_flags = 0
        for mod in modifiers:
            modifier_flags |= self.MODIFIER_FLAGS.get(mod, 0)

        # Press each regular key
        for key in regular_keys:
            keycode = self.KEYCODE_MAP.get(key)
            if keycode is None:
                print(f"Warning: Unknown key '{key}', skipping...")
                continue

            # Create key down event
            down_event = CGEventCreateKeyboardEvent(self.event_source, keycode, True)
            if modifier_flags:
                CGEventSetFlags(down_event, modifier_flags)
            CGEventPost(kCGSessionEventTap, down_event)

            # Small delay
            time.sleep(0.01)

            # Create key up event
            up_event = CGEventCreateKeyboardEvent(self.event_source, keycode, False)
            if modifier_flags:
                CGEventSetFlags(up_event, modifier_flags)
            CGEventPost(kCGSessionEventTap, up_event)

            time.sleep(0.01)


if __name__ == '__main__':
    # Test the event injector
    injector = EventInjector()

    print("Testing left click in 2 seconds...")
    time.sleep(2)
    injector.click('left')

    print("Testing CMD+C in 2 seconds...")
    time.sleep(2)
    injector.keystroke(['cmd', 'c'])
