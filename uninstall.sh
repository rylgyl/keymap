#!/bin/bash

# Uninstallation script for Keymap daemon
# This removes the auto-start on login

set -e

echo "=========================================="
echo "Keymap Auto-Start Uninstallation"
echo "=========================================="
echo ""

PLIST_PATH="$HOME/Library/LaunchAgents/com.keymap.daemon.plist"

if [ -f "$PLIST_PATH" ]; then
    echo "Stopping daemon..."
    launchctl unload "$PLIST_PATH" 2>/dev/null || true
    echo "✓ Daemon stopped"
    echo ""

    echo "Removing LaunchAgent plist..."
    rm "$PLIST_PATH"
    echo "✓ LaunchAgent removed"
    echo ""

    echo "=========================================="
    echo "Uninstallation Complete!"
    echo "=========================================="
    echo ""
    echo "Keymap will no longer start automatically on login."
    echo ""
    echo "To start manually, run: ./run.sh"
    echo "To reinstall auto-start, run: ./install.sh"
    echo ""
else
    echo "LaunchAgent not found. Nothing to uninstall."
    echo ""
fi
