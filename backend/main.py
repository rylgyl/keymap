#!/usr/bin/env python3
"""
Main Flask application for keymap daemon
Provides REST API and WebSocket interface for configuration
"""
import sys
import os

# Ensure unbuffered output
sys.stdout.reconfigure(line_buffering=True) if hasattr(sys.stdout, 'reconfigure') else None
sys.stderr.reconfigure(line_buffering=True) if hasattr(sys.stderr, 'reconfigure') else None

print("Loading Flask modules...", flush=True)
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from pathlib import Path

print("Loading keymap modules...", flush=True)
# Import our modules
from permission_checker import PermissionChecker
from config_manager import ConfigManager
from app_detector import AppDetector
from event_injector import EventInjector
from event_tap import EventTap
from remapper import Remapper

print("All modules loaded successfully!", flush=True)

# Initialize Flask app
print("Initializing Flask app...", flush=True)
app = Flask(__name__, static_folder='../frontend/dist', static_url_path='')
# Only allow CORS from localhost for security
CORS(app, origins=["http://localhost:*", "http://127.0.0.1:*"])
socketio = SocketIO(app, cors_allowed_origins=["http://localhost:*", "http://127.0.0.1:*"], async_mode='threading')
print("Flask app initialized", flush=True)

# Initialize components
print("Initializing components...", flush=True)
config_manager = ConfigManager()
print("  - ConfigManager OK", flush=True)
app_detector = AppDetector()
print("  - AppDetector OK", flush=True)
event_injector = EventInjector()
print("  - EventInjector OK", flush=True)
remapper = Remapper(config_manager, app_detector, event_injector)
print("  - Remapper OK", flush=True)
event_tap = EventTap(remapper)
print("  - EventTap OK", flush=True)
permission_checker = PermissionChecker()
print("Components initialized successfully!", flush=True)


# =============================================================================
# REST API Endpoints
# =============================================================================

@app.route('/')
def index():
    """Serve the frontend"""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/permissions', methods=['GET'])
def get_permissions():
    """Check accessibility permission status"""
    status = permission_checker.get_status()
    return jsonify(status)


@app.route('/api/permissions/request', methods=['POST'])
def request_permissions():
    """Request accessibility permissions"""
    permission_checker.request_permission()
    return jsonify({'success': True})


@app.route('/api/config', methods=['GET'])
def get_config():
    """Get current configuration"""
    config = config_manager.get_config()
    return jsonify(config)


@app.route('/api/config', methods=['POST'])
def save_config():
    """Save configuration"""
    try:
        new_config = request.json
        config_manager.save(new_config)
        return jsonify({'success': True, 'config': new_config})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/apps', methods=['GET'])
def get_apps():
    """Get information about detected apps"""
    current_app_info = app_detector.get_frontmost_app()

    # Get list of apps from config
    config = config_manager.get_config()
    configured_apps = list(config.get('apps', {}).keys())

    return jsonify({
        'current': current_app_info,
        'configured': configured_apps
    })


@app.route('/api/context', methods=['GET'])
def get_context():
    """Get current remapping context"""
    context = remapper.get_current_context()
    return jsonify(context)


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get overall system status"""
    return jsonify({
        'event_tap_running': event_tap.is_running(),
        'detection_mode': event_tap.detection_mode,
        'permissions_granted': permission_checker.is_trusted(),
        'current_app': app_detector.get_frontmost_app()
    })


@app.route('/api/event_tap/start', methods=['POST'])
def start_event_tap():
    """Start the event tap"""
    if not permission_checker.is_trusted():
        return jsonify({'success': False, 'error': 'Accessibility permissions not granted'}), 403

    event_tap.start()
    return jsonify({'success': True})


@app.route('/api/event_tap/stop', methods=['POST'])
def stop_event_tap():
    """Stop the event tap"""
    event_tap.stop()
    return jsonify({'success': True})


# =============================================================================
# WebSocket Events
# =============================================================================

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected')
    emit('connected', {'status': 'ok'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')


@socketio.on('start_detection')
def handle_start_detection():
    """Start button detection mode"""
    print('Starting button detection mode')
    event_tap.set_detection_mode(True)
    emit('detection_started', {'status': 'ok'})


@socketio.on('stop_detection')
def handle_stop_detection():
    """Stop button detection mode"""
    print('Stopping button detection mode')
    event_tap.set_detection_mode(False)
    emit('detection_stopped', {'status': 'ok'})


# Button detection callback
def on_button_detected(button_info):
    """Called when a button is detected in detection mode"""
    print(f"Button detected: {button_info}")
    socketio.emit('button_detected', button_info)


# Register the detection callback
event_tap.on_button_detected(on_button_detected)


# App change callback
def on_app_change(old_bundle_id, new_bundle_id):
    """Called when the frontmost app changes"""
    app_info = app_detector.get_frontmost_app()
    print(f"App changed: {old_bundle_id} -> {new_bundle_id}")
    socketio.emit('app_changed', app_info)


# Register the app change callback
app_detector.on_app_change(on_app_change)


# =============================================================================
# Startup & Initialization
# =============================================================================

def initialize():
    """Initialize the daemon"""
    print("Initializing keymap daemon...")

    # Check permissions
    if not permission_checker.is_trusted():
        print("WARNING: Accessibility permissions not granted!")
        print("The daemon will not work until you grant permissions.")
        print("Opening System Preferences...")
        permission_checker.request_permission()
    else:
        print("Accessibility permissions OK")

    # Start monitoring apps
    print("Starting app detector...")
    app_detector.start_monitoring()

    # Start watching config
    print("Starting config watcher...")
    config_manager.start_watching()

    # Start event tap if permissions are granted
    if permission_checker.is_trusted():
        print("Starting event tap...")
        event_tap.start()

    print("Initialization complete!")


def shutdown():
    """Clean shutdown"""
    print("Shutting down...")
    event_tap.stop()
    app_detector.stop_monitoring()
    config_manager.stop_watching()
    print("Shutdown complete")


# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':
    try:
        # Initialize
        initialize()

        # Run Flask app
        print("Starting web server on http://localhost:8080")
        print("Open your browser to configure button mappings")
        socketio.run(app, host='0.0.0.0', port=8080, debug=False, allow_unsafe_werkzeug=True)

    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        shutdown()
