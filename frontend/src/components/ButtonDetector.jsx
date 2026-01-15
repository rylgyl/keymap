import { useState, useEffect } from 'react'

function ButtonDetector({ socket }) {
  const [detecting, setDetecting] = useState(false)
  const [lastDetected, setLastDetected] = useState(null)

  useEffect(() => {
    if (!socket) return

    socket.on('button_detected', (buttonInfo) => {
      setLastDetected(buttonInfo)
    })

    socket.on('detection_started', () => {
      console.log('Detection started')
    })

    socket.on('detection_stopped', () => {
      console.log('Detection stopped')
    })

    return () => {
      socket.off('button_detected')
      socket.off('detection_started')
      socket.off('detection_stopped')
    }
  }, [socket])

  const handleToggleDetection = () => {
    if (!socket) return

    if (detecting) {
      socket.emit('stop_detection')
      setDetecting(false)
    } else {
      socket.emit('start_detection')
      setDetecting(true)
      setLastDetected(null)
    }
  }

  return (
    <div className="card">
      <h2 style={{ marginBottom: '16px' }}>Button Detector</h2>
      <p style={{ color: '#6e6e73', marginBottom: '16px' }}>
        Click "Start Detecting" then press any mouse button to see which button number it is.
      </p>

      <button
        onClick={handleToggleDetection}
        style={{
          background: detecting ? '#ff3b30' : '#007aff',
          marginBottom: '16px'
        }}
      >
        {detecting ? 'Stop Detecting' : 'Start Detecting'}
      </button>

      {detecting && (
        <div
          style={{
            background: '#f5f5f7',
            padding: '20px',
            borderRadius: '8px',
            textAlign: 'center'
          }}
        >
          <p style={{ fontSize: '14px', color: '#6e6e73', marginBottom: '12px' }}>
            Waiting for button press...
          </p>
          {lastDetected && (
            <div style={{ fontSize: '48px', fontWeight: '700', color: '#007aff' }}>
              Button {lastDetected.button}
            </div>
          )}
        </div>
      )}

      {!detecting && lastDetected && (
        <div style={{ color: '#6e6e73', fontSize: '14px' }}>
          Last detected: Button {lastDetected.button}
        </div>
      )}
    </div>
  )
}

export default ButtonDetector
