# CLAUDE.md — Keymap Project Context

## What this project does
Keymap is a macOS background daemon that remaps mouse side buttons (and other extra buttons) to custom keyboard shortcuts or mouse actions. It uses the macOS CGEventTap API to intercept hardware events and injects replacement events via CoreGraphics. A Flask + React web UI at `http://localhost:8080` handles configuration.

## Architecture
- **`backend/main.py`** — Flask server, REST API, WebSocket (flask-socketio), startup/shutdown logic
- **`backend/event_tap.py`** — CGEventTap wrapper using PyObjC/Quartz; runs in a background thread with its own CFRunLoop
- **`backend/event_injector.py`** — injects synthetic mouse/keyboard events via CoreGraphics
- **`backend/remapper.py`** — maps button numbers to configured actions
- **`backend/config_manager.py`** — reads/writes `~/Library/Application Support/keymap/config.json`; watches for changes
- **`backend/permission_checker.py`** — checks/requests macOS Accessibility permissions (required for CGEventTap)
- **`frontend/`** — React + Vite app; built output goes to `frontend/dist/`

## Running the daemon

```bash
source venv/bin/activate
python backend/main.py
```

Or via the LaunchAgent (auto-start on login):
```bash
launchctl kickstart -k gui/$(id -u)/com.keymap.daemon
```

UI is always at **http://localhost:8080** (port hardcoded in `main.py`).

## Known macOS LaunchAgent issue

**macOS TCC (Transparency, Consent, and Control) blocks LaunchAgent processes from reading files in `~/Desktop`.** This caused two symptoms:

1. Python's venv `site.py` deadlocked on startup (`OSError: [Errno 11] Resource deadlock avoided`)
2. Werkzeug couldn't serve static files from `frontend/dist/`

**Fixes applied:**
- The LaunchAgent plist (`~/Library/LaunchAgents/com.keymap.daemon.plist`) uses the real Homebrew Python binary directly (not the venv symlink) with `PYTHONPATH` set to the venv's site-packages — bypasses venv `site.py` entirely
- `ThrottleInterval: 10` added to prevent rapid crash loops
- `install.sh` copies `frontend/dist/` to `~/Library/Application Support/keymap/dist/` — a location the LaunchAgent can freely read
- `main.py` serves static files from Application Support, not from the project directory

**If you rebuild the frontend**, run `./install.sh` again to sync the new dist files to Application Support.

## Logs
```
~/Library/Logs/keymap.log        # stdout
~/Library/Logs/keymap.error.log  # stderr
```

## Config file
```
~/Library/Application Support/keymap/config.json
```

## Dependencies
- Python 3.13 (via Homebrew `python@3.13`)
- pyobjc-framework-Quartz (CGEventTap, CoreGraphics)
- Flask, flask-cors, flask-socketio
- Node.js / npm (frontend build only)

## Frontend rebuild
```bash
cd frontend
npm install
npm run build
cd ..
./install.sh   # sync new dist to Application Support
```
