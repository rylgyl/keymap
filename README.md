# Keymap - Mouse & Keyboard Remapper for macOS

A simple, powerful tool to remap mouse buttons and keyboard shortcuts on macOS with per-application support.

## Features

- 🖱️ **Remap Mouse Buttons**: Map extra mouse buttons (4, 5, etc.) to different actions
- ⌨️ **Custom Keystrokes**: Assign keyboard shortcuts to mouse buttons
- 🎯 **Per-App Contexts**: Different mappings for different applications
- 🔍 **Button Detection**: Visual interface to detect which button you're pressing
- 🌐 **Web UI**: Easy-to-use browser-based configuration interface
- 🔄 **Hot Reload**: Changes apply instantly without restarting

## Requirements

- macOS 10.13 or later
- Python 3.11 or higher
- Node.js 18+ (for building the frontend)

## Installation

### 1. Clone or Download

The project is already in `/Users/anujgoyal/Desktop/Coding/keymap`

### 2. Install Backend Dependencies

```bash
cd /Users/anujgoyal/Desktop/Coding/keymap
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Install Frontend Dependencies and Build

```bash
cd frontend
npm install
npm run build
cd ..
```

### 4. Make Startup Script Executable

```bash
chmod +x run.sh
```

## Usage

### Starting the Daemon

```bash
./run.sh
```

This will:
1. Start the backend daemon
2. Open your browser to http://localhost:8080

### First-Time Setup

1. **Grant Accessibility Permissions**:
   - When you first run the daemon, it will prompt you to grant accessibility permissions
   - Go to System Preferences → Security & Privacy → Privacy → Accessibility
   - Add Terminal or your preferred terminal app to the list
   - Restart the daemon

2. **Configure Button Mappings**:
   - Open http://localhost:8080 in your browser
   - Click "Detect Button" to identify button numbers
   - Press the mouse button you want to remap
   - Choose an action:
     - **Mouse Click**: Remap to left/right/middle click
     - **Keyboard Shortcut**: Enter a shortcut (e.g., `cmd+[`)
     - **Ignore**: Suppress the button press
   - Click "Save Configuration"

### Per-Application Contexts

1. In the "Application Context" section, click "Add New App Context"
2. Enter the bundle ID of the app (e.g., `com.google.Chrome`)
   - Or click "Use Current App" to use the frontmost application
3. Configure button mappings specific to that app
4. Save the configuration

The daemon will automatically switch contexts when you switch applications.

## Configuration

Configuration is stored in:
```
~/Library/Application Support/keymap/config.json
```

Example configuration:
```json
{
  "global": {
    "button4": {
      "type": "keystroke",
      "keys": ["cmd", "["]
    },
    "button5": {
      "type": "keystroke",
      "keys": ["cmd", "]"]
    }
  },
  "apps": {
    "com.google.Chrome": {
      "button4": {
        "type": "keystroke",
        "keys": ["cmd", "["]
      }
    }
  }
}
```

## Auto-Start on Login (Optional)

To have Keymap start automatically when you log in:

1. Edit `config/com.keymap.daemon.plist` and replace `YOUR_USERNAME` with your actual username

2. Copy the plist to LaunchAgents:
```bash
cp config/com.keymap.daemon.plist ~/Library/LaunchAgents/
```

3. Load the agent:
```bash
launchctl load ~/Library/LaunchAgents/com.keymap.daemon.plist
```

To stop auto-start:
```bash
launchctl unload ~/Library/LaunchAgents/com.keymap.daemon.plist
rm ~/Library/LaunchAgents/com.keymap.daemon.plist
```

## Troubleshooting

### Daemon Won't Start

1. Check that you activated the virtual environment:
   ```bash
   source venv/bin/activate
   ```

2. Verify dependencies are installed:
   ```bash
   pip list
   ```

### Button Presses Not Detected

1. Ensure accessibility permissions are granted
2. Check that the event tap is running (green indicator in the web UI)
3. Look for errors in the terminal where you ran `./run.sh`

### Changes Not Taking Effect

1. Click "Save Configuration" in the web UI
2. The configuration should reload automatically
3. If not, restart the daemon

### Finding Bundle IDs

To find an app's bundle ID:
```bash
osascript -e 'id of app "App Name"'
```

For example:
```bash
osascript -e 'id of app "Google Chrome"'
# Output: com.google.Chrome
```

## Development

### Running in Development Mode

Backend:
```bash
source venv/bin/activate
python backend/main.py
```

Frontend (separate terminal):
```bash
cd frontend
npm run dev
```

Then visit http://localhost:3000 (Vite dev server with hot reload)

### Project Structure

```
keymap/
├── backend/
│   ├── main.py              # Flask server & API
│   ├── event_tap.py         # CGEventTap wrapper
│   ├── event_injector.py    # Mouse/keyboard simulation
│   ├── remapper.py          # Remapping logic
│   ├── app_detector.py      # App context detection
│   ├── config_manager.py    # Configuration management
│   └── permission_checker.py # Accessibility permissions
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React app
│   │   ├── components/      # React components
│   │   └── api/             # API client
│   └── dist/                # Built static files
├── config/
│   ├── default_config.json  # Default mappings
│   └── com.keymap.daemon.plist # LaunchAgent config
├── venv/                    # Python virtual environment
├── requirements.txt         # Python dependencies
├── run.sh                   # Startup script
└── README.md               # This file
```

## Technical Details

### How It Works

1. **Event Capture**: Uses macOS CGEventTap API to intercept hardware mouse events
2. **App Detection**: Monitors frontmost application using NSWorkspace
3. **Remapping**: When a mapped button is pressed, the original event is suppressed and a new event is injected
4. **Configuration**: JSON-based config with hot reload via file watching
5. **UI**: React web interface communicates with Flask backend via REST API and WebSockets

### Supported Actions

- **Mouse Click**: left, right, middle
- **Keyboard Shortcut**: Any combination of modifiers (cmd, ctrl, shift, alt/option) and keys
- **Ignore**: Suppress the button press entirely

### Known Limitations

- Requires accessibility permissions (this is a macOS security requirement)
- Cannot remap keyboard keys that are already system shortcuts
- Some apps may not respond to injected events (security feature)

## License

This is a personal tool. Use and modify as you wish.

## Credits

Built with:
- Python + PyObjC for macOS integration
- Flask + Flask-SocketIO for the backend
- React + Vite for the frontend
- macOS Core Graphics framework for event handling
