#!/bin/bash

# Keymap daemon startup script

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment
source venv/bin/activate

# Start the Flask server
echo "Starting Keymap daemon..."
echo "Web UI will be available at http://localhost:8080"

# Run the main application
python backend/main.py
