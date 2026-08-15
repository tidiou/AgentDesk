import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import AnalyticsResultsView from '../components/AnalyticsResultsView'
import { getSharedAnalytics } from '../api/client'

function SharedAnalyticsView() {
  const { shareId } = useParams()
  const [result, setResult] = useState(null)
  const [status, setStatus] = useState('loading') // loading | error | ready
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
      <h1>AgentDesk</h1>
      {status === 'loading' && <p>Loading shared report...</p>}
      {status === 'error' && <p style={{ color: '#ff6b6b' }}>Error: {error}</p>}
      {status === 'ready' && <AnalyticsResultsView result={result} />}
    </div>
  )
}

export default SharedAnalyticsView