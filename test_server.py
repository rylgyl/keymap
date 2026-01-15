#!/usr/bin/env python3
"""Minimal test server"""
from flask import Flask, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/api/status')
def status():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    print("Starting test server on http://localhost:8080")
    socketio.run(app, host='0.0.0.0', port=8080, debug=False)
