import { useState, useEffect } from 'react'
import KeystrokeDetector from './KeystrokeDetector'

function ConfigPanel({ config, currentContext, onSave, socket }) {
  const [mappings, setMappings] = useState({})
  const [editingButton, setEditingButton] = useState(null)
  const [detecting, setDetecting] = useState(false)
  const [detectingKeystroke, setDetectingKeystroke] = useState(null) // Track which button is detecting keystroke

  useEffect(() => {
    // Load mappings for current context
    if (config) {
      if (currentContext === 'global') {
        setMappings(config.global || {})
      } else {
        setMappings(config.apps?.[currentContext] || {})
      }
    }
  }, [config, currentContext])

  useEffect(() => {
    if (!socket) return

    socket.on('button_detected', (buttonInfo) => {
      if (detecting && editingButton !== null) {
        const buttonKey = `button${buttonInfo.button}`
        addMapping(buttonKey)
        socket.emit('stop_detection')
        setDetecting(false)
      }
    })

    return () => {
      socket.off('button_detected')
    }
  }, [socket, detecting, editingButton])

  const addMapping = (buttonKey) => {
    const newMappings = {
      ...mappings,
      [buttonKey]: { type: 'click', button: 'left' }
    }
    setMappings(newMappings)
    setEditingButton(buttonKey)
  }

  const updateMapping = (buttonKey, field, value) => {
    const newMappings = {
      ...mappings,
      [buttonKey]: {
        ...mappings[buttonKey],
        [field]: value
      }
    }
    setMappings(newMappings)
  }

  const removeMapping = (buttonKey) => {
    const newMappings = { ...mappings }
    delete newMappings[buttonKey]
    setMappings(newMappings)
    setEditingButton(null)
  }

  const handleDetectButton = () => {
    if (socket) {
      socket.emit('start_detection')
      setDetecting(true)
      setEditingButton('detecting')
    }
  }

  const handleStopDetecting = () => {
    if (socket) {
      socket.emit('stop_detection')
      setDetecting(false)
      setEditingButton(null)
    }
  }

  const handleSave = () => {
    const newConfig = { ...config }
    if (currentContext === 'global') {
      newConfig.global = mappings
    } else {
      if (!newConfig.apps) newConfig.apps = {}
      newConfig.apps[currentContext] = mappings
    }
    onSave(newConfig)
    alert('Configuration saved!')
  }

  const handleKeystrokeChange = (buttonKey, value) => {
    // Parse keystroke input (e.g., "cmd+[" -> ["cmd", "["])
    const keys = value.split('+').map(k => k.trim()).filter(k => k)
    updateMapping(buttonKey, 'keys', keys)
  }

  const handleDetectKeystroke = (buttonKey) => {
    setDetectingKeystroke(buttonKey)
  }

  const handleKeystrokeDetected = (keys) => {
    if (detectingKeystroke) {
      updateMapping(detectingKeystroke, 'keys', keys)
      setDetectingKeystroke(null)
    }
  }

  const handleCancelKeystrokeDetection = () => {
    setDetectingKeystroke(null)
  }

  const buttonKeys = Object.keys(mappings).sort()

  return (
    <div className="card">
      <h2 style={{ marginBottom: '16px' }}>Button Mappings</h2>
      <p style={{ color: '#6e6e73', marginBottom: '16px', fontSize: '14px' }}>
        Configuring for: <strong>{currentContext === 'global' ? 'All Apps' : currentContext}</strong>
      </p>

      {/* Add New Mapping */}
      <div style={{ marginBottom: '20px' }}>
        {!detecting ? (
          <button onClick={handleDetectButton}>Detect Button</button>
        ) : (
          <div>
            <p style={{ marginBottom: '8px', color: '#007aff' }}>
              Press a mouse button to detect...
            </p>
            <button className="secondary" onClick={handleStopDetecting}>Cancel</button>
          </div>
        )}
      </div>

      {/* Existing Mappings */}
      {buttonKeys.length === 0 ? (
        <p style={{ color: '#8e8e93', textAlign: 'center', padding: '20px' }}>
          No button mappings configured. Click "Detect Button" to add one.
        </p>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {buttonKeys.map((buttonKey) => {
            const mapping = mappings[buttonKey]
            const buttonNumber = buttonKey.replace('button', '')

            return (
              <div
                key={buttonKey}
                style={{
                  background: '#f5f5f7',
                  padding: '16px',
                  borderRadius: '8px',
                  border: editingButton === buttonKey ? '2px solid #007aff' : '2px solid transparent'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                  <h3 style={{ fontSize: '16px', fontWeight: '600' }}>
                    Button {buttonNumber}
                  </h3>
                  <button
                    className="danger"
                    onClick={() => removeMapping(buttonKey)}
                    style={{ fontSize: '12px', padding: '4px 12px' }}
                  >
                    Remove
                  </button>
                </div>

                {/* Action Type */}
                <div style={{ marginBottom: '12px' }}>
                  <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>
                    Action:
                  </label>
                  <select
                    value={mapping.type || 'click'}
                    onChange={(e) => updateMapping(buttonKey, 'type', e.target.value)}
                    style={{ width: '100%' }}
                  >
                    <option value="click">Mouse Click</option>
                    <option value="keystroke">Keyboard Shortcut</option>
                    <option value="ignore">Ignore (Suppress)</option>
                  </select>
                </div>

                {/* Click Target */}
                {mapping.type === 'click' && (
                  <div>
                    <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>
                      Click Type:
                    </label>
                    <select
                      value={mapping.button || 'left'}
                      onChange={(e) => updateMapping(buttonKey, 'button', e.target.value)}
                      style={{ width: '100%' }}
                    >
                      <option value="left">Left Click</option>
                      <option value="right">Right Click</option>
                      <option value="middle">Middle Click</option>
                    </select>
                  </div>
                )}

                {/* Keystroke */}
                {mapping.type === 'keystroke' && (
                  <div>
                    <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>
                      Keyboard Shortcut:
                    </label>
                    <div style={{ display: 'flex', gap: '8px', marginBottom: '8px' }}>
                      <input
                        type="text"
                        value={(mapping.keys || []).join('+')}
                        onChange={(e) => handleKeystrokeChange(buttonKey, e.target.value)}
                        placeholder="e.g., cmd+[ or ctrl+shift+t"
                        style={{ flex: 1 }}
                      />
                      <button
                        onClick={() => handleDetectKeystroke(buttonKey)}
                        style={{ padding: '8px 16px', whiteSpace: 'nowrap' }}
                      >
                        Detect
                      </button>
                    </div>
                    <p style={{ fontSize: '12px', color: '#6e6e73' }}>
                      Click "Detect" and press any key combination, or type it manually (e.g., cmd+[)
                    </p>
                  </div>
                )}
              </div>
            )
          })}
        </div>
      )}

      {/* Save Button */}
      {buttonKeys.length > 0 && (
        <button
          onClick={handleSave}
          style={{
            marginTop: '20px',
            width: '100%',
            padding: '12px',
            fontSize: '16px',
            fontWeight: '600'
          }}
        >
          Save Configuration
        </button>
      )}

      {/* Keystroke Detector Modal */}
      <KeystrokeDetector
        isActive={detectingKeystroke !== null}
        onDetected={handleKeystrokeDetected}
        onCancel={handleCancelKeystrokeDetection}
      />
    </div>
  )
}

export default ConfigPanel
