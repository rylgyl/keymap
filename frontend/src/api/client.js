/**
 * API client for communicating with the backend
 */

const API_BASE = '/api';

export const api = {
  // Permissions
  async getPermissions() {
    const response = await fetch(`${API_BASE}/permissions`);
    return response.json();
  },

  async requestPermissions() {
    const response = await fetch(`${API_BASE}/permissions/request`, {
      method: 'POST'
    });
    return response.json();
  },

  // Configuration
  async getConfig() {
    const response = await fetch(`${API_BASE}/config`);
    return response.json();
  },

  async saveConfig(config) {
    const response = await fetch(`${API_BASE}/config`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(config)
    });
    return response.json();
  },

  // Apps
  async getApps() {
    const response = await fetch(`${API_BASE}/apps`);
    return response.json();
  },

  // Context
  async getContext() {
    const response = await fetch(`${API_BASE}/context`);
    return response.json();
  },

  // Status
  async getStatus() {
    const response = await fetch(`${API_BASE}/status`);
    return response.json();
  },

  // Event Tap
  async startEventTap() {
    const response = await fetch(`${API_BASE}/event_tap/start`, {
      method: 'POST'
    });
    return response.json();
  },

  async stopEventTap() {
    const response = await fetch(`${API_BASE}/event_tap/stop`, {
      method: 'POST'
    });
    return response.json();
  }
};
