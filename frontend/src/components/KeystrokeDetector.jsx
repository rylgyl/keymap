import { useState, useEffect, useRef } from 'react'

function KeystrokeDetector({ onDetected, isActive, onCancel }) {
  const [pressedKeys, setPressedKeys] = useState([])
  const inputRef = useRef(null)

  useEffect(() => {
    if (!isActive) return

    // Focus the input when detection starts
    if (inputRef.current) {
      inputRef.current.focus()
    }

    const handleKeyDown = (e) => {
      e.preventDefault()
      e.stopPropagation()

      const keys = []

      // Add modifiers
      if (e.metaKey || e.key === 'Meta') keys.push('cmd')
      if (e.ctrlKey || e.key === 'Control') keys.push('ctrl')
      if (e.shiftKey || e.key === 'Shift') keys.push('shift')
      if (e.altKey || e.key === 'Alt') keys.push('alt')

      // Add the actual key (not a modifier)
      if (!['Meta', 'Control', 'Shift', 'Alt'].includes(e.key)) {
        let keyName = e.key

        // Normalize special keys
        if (keyName === ' ') keyName = 'space'
        else if (keyName === 'Escape') keyName = 'esc'
        else if (keyName === 'ArrowUp') keyName = 'up'
        else if (keyName === 'ArrowDown') keyName = 'down'
        else if (keyName === 'ArrowLeft') keyName = 'left'
        else if (keyName === 'ArrowRight') keyName = 'right'
        else if (keyName === 'Backspace') keyName = 'delete'
        else if (keyName.length === 1) keyName = keyName.toLowerCase()

        keys.push(keyName)
      }

      setPressedKeys(keys)

      // Auto-confirm after a short delay if we have a valid combination
      if (keys.length > 0 && !['Meta', 'Control', 'Shift', 'Alt'].includes(e.key)) {
        setTimeout(() => {
          onDetected(keys)
        }, 300)
      }
    }

    const handleKeyUp = (e) => {
      // Don't clear on modifier release, only on regular key release
      if (!['Meta', 'Control', 'Shift', 'Alt'].includes(e.key)) {
        setPressedKeys([])
      }
    }

    window.addEventListener('keydown', handleKeyDown, true)
    window.addEventListener('keyup', handleKeyUp, true)

    return () => {
      window.removeEventListener('keydown', handleKeyDown, true)
      window.removeEventListener('keyup', handleKeyUp, true)
    }
  }, [isActive, onDetected])

  if (!isActive) return null

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'rgba(0, 0, 0, 0.7)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000
      }}
      onClick={onCancel}
    >
      <div
        style={{
          background: 'white',
          padding: '40px',
          borderRadius: '16px',
          maxWidth: '500px',
          textAlign: 'center'
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <h2 style={{ marginBottom: '20px' }}>Press a Key Combination</h2>
        <p style={{ color: '#6e6e73', marginBottom: '20px' }}>
          Press any key combination (e.g., cmd+], ctrl+shift+t)
        </p>

        {/* Hidden input to capture focus */}
        <input
          ref={inputRef}
          type="text"
          style={{
            position: 'absolute',
            opacity: 0,
            pointerEvents: 'none'
          }}
        />

        {/* Display detected keys */}
        <div
          style={{
            background: '#f5f5f7',
            padding: '30px',
            borderRadius: '12px',
            marginBottom: '20px',
            minHeight: '80px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}
        >
          {pressedKeys.length > 0 ? (
            <div style={{ fontSize: '32px', fontWeight: '700', color: '#007aff' }}>
              {pressedKeys.join(' + ')}
            </div>
          ) : (
            <div style={{ fontSize: '16px', color: '#8e8e93' }}>
              Waiting for input...
            </div>
          )}
        </div>

        <button className="secondary" onClick={onCancel}>
          Cancel
        </button>
      </div>
    </div>
  )
}

export default KeystrokeDetector
