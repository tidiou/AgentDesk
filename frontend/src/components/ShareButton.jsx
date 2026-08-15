import { useState } from 'react'
import { shareAnalytics } from '../api/client'

function ShareButton({ result }) {
  const [shareUrl, setShareUrl] = useState(null)
  const [status, setStatus] = useState('idle') // idle | loading | copied

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
        <button onClick={handleShare} disabled={status === 'loading'}>
          {status === 'loading' ? 'Creating link...' : 'Share this report'}
        </button>
      ) : (
        <div>
          <input readOnly value={shareUrl} style={{ width: '300px', marginRight: '0.5rem' }} />
          <button onClick={handleCopy}>{status === 'copied' ? 'Copied!' : 'Copy'}</button>
        </div>
      )}
    </div>
  )
}

export default ShareButton