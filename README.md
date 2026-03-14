# Keymap - Mouse & Keyboard Remapper for macOS

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform: macOS](https://img.shields.io/badge/Platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-green.svg)](https://www.python.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

A simple, powerful tool to remap mouse buttons and keyboard shortcuts on macOS.

![Keymap Screenshot](screenshot.png)

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Auto-Start on Login](#auto-start-on-login-optional)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/keymap.git
cd keymap

# Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Build frontend
cd frontend && npm install && npm run build && cd ..

# Make script executable and run
chmod +x run.sh
./run.sh
```

Open http://localhost:8080 in your browser and grant accessibility permissions when prompted.

For detailed instructions, see the [QUICKSTART.md](QUICKSTART.md) guide.

## Features

- 🖱️ **Remap Mouse Buttons**: Map extra mouse buttons (4, 5, etc.) to different actions
- ⌨️ **Custom Keystrokes**: Assign keyboard shortcuts to mouse buttons
- 🔍 **Button Detection**: Visual interface to detect which button you're pressing
- 🌐 **Web UI**: Easy-to-use browser-based configuration interface
- 🔄 **Hot Reload**: Changes apply instantly without restarting

## Requirements

- macOS 10.13 or later
- Python 3.11 or higher
- Node.js 18+ (for building the frontend)

## Installation

### 1. Clone or Download

```bash
git clone https://github.com/YOUR_USERNAME/keymap.git
cd keymap
```

Or download and extract the ZIP file, then navigate to the directory.

### 2. Install Backend Dependencies

```bash
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

## Configuration

Configuration is stored in:
```
~/Library/Application Support/keymap/config.json
```

Example configuration:
```json
{
  "mappings": {
    "button4": {
      "type": "keystroke",
      "keys": ["cmd", "["]
    },
    "button5": {
      "type": "keystroke",
      "keys": ["cmd", "]"]
    }
  }
}
```

## Auto-Start on Login

Run the install script to set up the daemon to start automatically on login:

```bash
./install.sh
```

This will:
1. Copy the frontend to `~/Library/Application Support/keymap/dist/` (required — see note below)
2. Create a LaunchAgent plist at `~/Library/LaunchAgents/com.keymap.daemon.plist`
3. Load and start the daemon

> **Why Application Support?** macOS restricts background processes (LaunchAgents) from reading files in `~/Desktop`. The install script copies the frontend to `~/Library/Application Support/keymap/` where the daemon can serve it freely. If you rebuild the frontend, re-run `./install.sh` to sync the new files.

To check daemon status:
```bash
launchctl list | grep keymap
curl http://localhost:8080/api/status
```

To restart the daemon:
```bash
launchctl kickstart -k gui/$(id -u)/com.keymap.daemon
```

To view logs:
```bash
tail -f ~/Library/Logs/keymap.log
tail -f ~/Library/Logs/keymap.error.log
```

To uninstall auto-start:
```bash
./uninstall.sh
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
2. **Remapping**: When a mapped button is pressed, the original event is suppressed and a new event is injected
3. **Configuration**: JSON-based config with hot reload via file watching
4. **UI**: React web interface communicates with Flask backend via REST API and WebSockets

### Supported Actions

- **Mouse Click**: left, right, middle
- **Keyboard Shortcut**: Any combination of modifiers (cmd, ctrl, shift, alt/option) and keys
- **Ignore**: Suppress the button press entirely

### Known Limitations

- Requires accessibility permissions (this is a macOS security requirement)
- Cannot remap keyboard keys that are already system shortcuts
- Some apps may not respond to injected events (security feature)

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on:
- Reporting bugs
- Suggesting features
- Submitting pull requests
- Development setup

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: Found a bug? [Open an issue](https://github.com/YOUR_USERNAME/keymap/issues)
- **Feature Requests**: Have an idea? [Request a feature](https://github.com/YOUR_USERNAME/keymap/issues/new?template=feature_request.md)
- **Questions**: Check existing [issues](https://github.com/YOUR_USERNAME/keymap/issues) or open a new one

## Credits

Built with:
- Python + PyObjC for macOS integration
- Flask + Flask-SocketIO for the backend
- React + Vite for the frontend
- macOS Core Graphics framework for event handling
