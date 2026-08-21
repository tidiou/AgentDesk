import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import AnalyticsResultsView from '../components/AnalyticsResultsView'
import { getSharedAnalytics } from '../api/client'

function SharedAnalyticsView() {
  const { shareId } = useParams()
  const [result, setResult] = useState(null)
  const [status, setStatus] = useState('loading')
  const [error, setError] = useState('')

  useEffect(() => {
    getSharedAnalytics(shareId)
      .then((data) => {
        setResult(data)
        setStatus('ready')
      })
      .catch((err) => {
        setError(err.message)
        setStatus('error')
      })
  }, [shareId])

  return (
    <div style={{ maxWidth: '900px', margin: '3rem auto', padding: '0 1rem' }}>
      <h1 style={{ color: '#2563EB' }}>AgentDesk</h1>
      {status === 'loading' && <p style={{ color: '#64748B' }}>Loading shared report...</p>}
      {status === 'error' && <p style={{ color: '#DC2626' }}>Error: {error}</p>}
      {status === 'ready' && <AnalyticsResultsView result={result} />}
    </div>
  )
}

export default SharedAnalyticsView