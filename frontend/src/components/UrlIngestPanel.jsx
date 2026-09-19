import { useState } from 'react'
import { ingestFromUrl } from '../api/client'

function UrlIngestPanel({ onUploadComplete }) {
  const [url, setUrl] = useState('')
  const [status, setStatus] = useState('idle')
  const [error, setError] = useState('')

  async function handleFetch() {
    setStatus('loading')
    setError('')
    try {
      const result = await ingestFromUrl(url)
      onUploadComplete(result)
      setStatus('idle')
    } catch (err) {
      setStatus('error')
      setError(err.message)
    }
  }

  return (
    <div style={{ marginTop: '1rem', display: 'flex', gap: '0.5rem' }}>
      <input
        placeholder="Or paste a URL to fetch (JSON API or webpage)..."
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        style={{
          flex: 1,
          backgroundColor: '#1E293B',
          color: '#F1F5F9',
          border: '1px solid #334155',
          borderRadius: '6px',
          padding: '0.5rem',
          fontSize: '0.85rem',
        }}
      />
      <button
        onClick={handleFetch}
        disabled={status === 'loading' || !url}
        style={{
          backgroundColor: '#3B82F6',
          color: '#F1F5F9',
          border: 'none',
          borderRadius: '6px',
          padding: '0.5rem 1rem',
          cursor: 'pointer',
          fontSize: '0.85rem',
        }}
      >
        {status === 'loading' ? 'Fetching...' : 'Fetch'}
      </button>
      {status === 'error' && <p style={{ color: '#F87171', fontSize: '0.85rem' }}>Error: {error}</p>}
    </div>
  )
}

export default UrlIngestPanel