import { useState, useEffect } from 'react'
import { io } from 'socket.io-client'
import { api } from './api/client'
import ConfigPanel from './components/ConfigPanel'
import ButtonDetector from './components/ButtonDetector'

function App() {
  const [socket, setSocket] = useState(null)
  const [permissions, setPermissions] = useState(null)
  const [config, setConfig] = useState(null)
  const [status, setStatus] = useState(null)

  // Initialize socket connection
  useEffect(() => {
    const newSocket = io()
    setSocket(newSocket)

    newSocket.on('connect', () => {
      console.log('Connected to server')
    })

    return () => newSocket.close()
  }, [])

  // Load initial data
  useEffect(() => {
    loadPermissions()
    loadConfig()
    loadStatus()

    // Poll status every 5 seconds
    const interval = setInterval(loadStatus, 5000)
    return () => clearInterval(interval)
  }, [])

  const loadPermissions = async () => {
    try {
      const data = await api.getPermissions()
      setPermissions(data)
    } catch (error) {
      console.error('Failed to load permissions:', error)
    }
  }

  const loadConfig = async () => {
    try {
      const data = await api.getConfig()
      setConfig(data)
    } catch (error) {
      console.error('Failed to load config:', error)
    }
  }

  const loadStatus = async () => {
    try {
      const data = await api.getStatus()
      setStatus(data)
    } catch (error) {
      console.error('Failed to load status:', error)
    }
  }

  const handleRequestPermissions = async () => {
    try {
      await api.requestPermissions()
      // Wait a bit for user to grant permissions, then check again
      setTimeout(loadPermissions, 2000)
    } catch (error) {
      console.error('Failed to request permissions:', error)
    }
  }

  const handleSaveConfig = async (newConfig) => {
    try {
      await api.saveConfig(newConfig)
      setConfig(newConfig)
    } catch (error) {
      console.error('Failed to save config:', error)
      alert('Failed to save configuration')
    }
  }

  if (!config || !permissions) {
    return (
      <div className="container">
        <div className="header">
          <h1>Keymap</h1>
          <p>Loading...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="container">
      <div className="header">
        <h1>Keymap</h1>
        <p>Mouse & Keyboard Remapper for macOS</p>
      </div>

      {/* Permission Banner */}
      {!permissions.granted && (
        <div className="banner error">
          <h3>Accessibility Permissions Required</h3>
          <p>{permissions.message}</p>
          <button onClick={handleRequestPermissions} style={{ marginTop: '12px' }}>
            Open System Preferences
          </button>
        </div>
      )}

      {/* Status Card */}
      <div className="card">
        <h2 style={{ marginBottom: '16px' }}>Status</h2>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <div>
            <span className={`status-indicator ${permissions.granted ? 'active' : 'inactive'}`} />
            Permissions: {permissions.granted ? 'Granted' : 'Not Granted'}
          </div>
          {status && (
            <div>
              <span className={`status-indicator ${status.event_tap_running ? 'active' : 'inactive'}`} />
              Event Tap: {status.event_tap_running ? 'Running' : 'Stopped'}
            </div>
          )}
        </div>
      </div>

      {permissions.granted && (
        <>
          {/* Button Detector */}
          <ButtonDetector socket={socket} />

          {/* Config Panel */}
          <ConfigPanel
            config={config}
            onSave={handleSaveConfig}
            socket={socket}
          />
        </>
      )}
    </div>
  )
}

export default App
