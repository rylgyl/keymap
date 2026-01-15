import { useState } from 'react'

function AppSelector({ apps, config, currentContext, onContextChange }) {
  const [showAddApp, setShowAddApp] = useState(false)
  const [newAppId, setNewAppId] = useState('')

  const configuredApps = config?.apps ? Object.keys(config.apps) : []

  const handleAddApp = () => {
    if (newAppId.trim()) {
      onContextChange(newAppId.trim())
      setNewAppId('')
      setShowAddApp(false)
    }
  }

  return (
    <div className="card">
      <h2 style={{ marginBottom: '16px' }}>Application Context</h2>
      <p style={{ color: '#6e6e73', marginBottom: '16px', fontSize: '14px' }}>
        Configure different button mappings for different applications.
      </p>

      <div style={{ marginBottom: '16px' }}>
        <label style={{ display: 'block', marginBottom: '8px', fontSize: '14px', fontWeight: '500' }}>
          Configure for:
        </label>
        <select
          value={currentContext}
          onChange={(e) => onContextChange(e.target.value)}
          style={{ width: '100%' }}
        >
          <option value="global">Global (All Apps)</option>
          {configuredApps.map((bundleId) => (
            <option key={bundleId} value={bundleId}>
              {bundleId}
            </option>
          ))}
        </select>
      </div>

      {!showAddApp ? (
        <button className="secondary" onClick={() => setShowAddApp(true)}>
          Add New App Context
        </button>
      ) : (
        <div>
          <p style={{ fontSize: '14px', marginBottom: '8px', color: '#6e6e73' }}>
            Enter bundle ID (e.g., com.google.Chrome):
            {apps.current && (
              <span style={{ display: 'block', marginTop: '4px' }}>
                Current app: <strong>{apps.current.bundle_id}</strong>
              </span>
            )}
          </p>
          <div style={{ display: 'flex', gap: '8px' }}>
            <input
              type="text"
              value={newAppId}
              onChange={(e) => setNewAppId(e.target.value)}
              placeholder="com.example.app"
              style={{ flex: 1 }}
              onKeyPress={(e) => {
                if (e.key === 'Enter') handleAddApp()
              }}
            />
            <button onClick={handleAddApp}>Add</button>
            <button className="secondary" onClick={() => setShowAddApp(false)}>
              Cancel
            </button>
          </div>
          {apps.current && (
            <button
              className="secondary"
              onClick={() => {
                setNewAppId(apps.current.bundle_id)
              }}
              style={{ marginTop: '8px', fontSize: '12px' }}
            >
              Use Current App ({apps.current.name})
            </button>
          )}
        </div>
      )}
    </div>
  )
}

export default AppSelector
