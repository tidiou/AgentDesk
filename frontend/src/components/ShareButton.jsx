import { useState } from 'react'
import { shareAnalytics } from '../api/client'

function ShareButton({ result }) {
  const [shareUrl, setShareUrl] = useState(null)
  const [status, setStatus] = useState('idle')

  async function handleShare() {
    setStatus('loading')
    const { share_id } = await shareAnalytics(result)
    const url = `${window.location.origin}/share/${share_id}`
    setShareUrl(url)
    setStatus('idle')
  }

  async function handleCopy() {
    await navigator.clipboard.writeText(shareUrl)
    setStatus('copied')
    setTimeout(() => setStatus('idle'), 2000)
  }

  return (
    <div style={{ marginTop: '0.75rem' }}>
      {!shareUrl ? (
        <button onClick={handleShare} disabled={status === 'loading'} style={primaryButtonStyle}>
          {status === 'loading' ? 'Creating link...' : 'Share this report'}
        </button>
      ) : (
        <div>
          <input readOnly value={shareUrl} style={inputStyle} />
          <button onClick={handleCopy} style={secondaryButtonStyle}>
            {status === 'copied' ? 'Copied!' : 'Copy'}
          </button>
        </div>
      )}
    </div>
  )
}

const primaryButtonStyle = {
  backgroundColor: '#2563EB',
  color: '#FFFFFF',
  border: 'none',
  borderRadius: '6px',
  padding: '0.5rem 1rem',
  cursor: 'pointer',
  fontSize: '0.9rem',
}
const secondaryButtonStyle = {
  backgroundColor: '#FFFFFF',
  color: '#2563EB',
  border: '1px solid #2563EB',
  borderRadius: '6px',
  padding: '0.5rem 1rem',
  cursor: 'pointer',
  fontSize: '0.9rem',
}
const inputStyle = {
  width: '300px',
  marginRight: '0.5rem',
  padding: '0.4rem',
  border: '1px solid #E2E8F0',
  borderRadius: '6px',
  color: '#1E293B',
}

export default ShareButton