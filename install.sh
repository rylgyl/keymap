#!/bin/bash

# Installation script for Keymap daemon
# This sets up the app to start automatically on login

set -e

echo "=========================================="
echo "Keymap Auto-Start Installation"
echo "=========================================="
echo ""

# Get the absolute path to the keymap directory
KEYMAP_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "Keymap directory: $KEYMAP_DIR"
echo ""

# Get the current username
USERNAME=$(whoami)
echo "Username: $USERNAME"
echo ""

# Create the plist file with the correct paths
PLIST_PATH="$HOME/Library/LaunchAgents/com.keymap.daemon.plist"

echo "Creating LaunchAgent plist at:"
echo "$PLIST_PATH"
echo ""

cat > "$PLIST_PATH" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.keymap.daemon</string>

    <key>ProgramArguments</key>
    <array>
        <string>$KEYMAP_DIR/venv/bin/python</string>
        <string>$KEYMAP_DIR/backend/main.py</string>
    </array>

    <key>WorkingDirectory</key>
    <string>$KEYMAP_DIR</string>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <true/>

    <key>StandardOutPath</key>
    <string>$HOME/Library/Logs/keymap.log</string>

    <key>StandardErrorPath</key>
    <string>$HOME/Library/Logs/keymap.error.log</string>
</dict>
</plist>
EOF

echo "✓ LaunchAgent plist created"
echo ""

# Load the LaunchAgent
echo "Loading LaunchAgent..."
launchctl load "$PLIST_PATH" 2>/dev/null || launchctl unload "$PLIST_PATH" 2>/dev/null && launchctl load "$PLIST_PATH"

echo "✓ LaunchAgent loaded"
echo ""

# Check if it's running
sleep 2
if launchctl list | grep -q com.keymap.daemon; then
    echo "✓ Keymap daemon is running!"
    echo ""
    echo "Testing server..."
    sleep 2
    if curl -s http://localhost:8080/api/status > /dev/null; then
        echo "✓ Server is responding on http://localhost:8080"
        echo ""
        echo "=========================================="
        echo "Installation Complete!"
        echo "=========================================="
        echo ""
        echo "Keymap will now start automatically on login."
        echo ""
        echo "Web UI: http://localhost:8080"
        echo "Logs:   $HOME/Library/Logs/keymap.log"
        echo ""
        echo "To uninstall, run: ./uninstall.sh"
        echo ""
    else
        echo "⚠ Server is starting up, please wait a few seconds..."
        echo "Then visit: http://localhost:8080"
        echo ""
    fi
else
    echo "⚠ Warning: LaunchAgent may not be running"
    echo "Check logs at: $HOME/Library/Logs/keymap.error.log"
    echo ""
fi
