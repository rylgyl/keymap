#!/bin/bash

# Wrapper script for LaunchAgent startup
# Adds a delay to avoid macOS venv deadlock during early login

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Wait for system to fully initialize before starting
sleep 5

cd "$SCRIPT_DIR"
exec "$SCRIPT_DIR/venv/bin/python" "$SCRIPT_DIR/backend/main.py"
