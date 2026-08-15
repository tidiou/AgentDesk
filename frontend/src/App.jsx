import { useState } from 'react'
import UploadZone from './components/UploadZone'
import FilePreviewCard from './components/FilePreviewCard'
import UATResultsTable from './components/UATResultsTable'
import AnalyticsResultsView from './components/AnalyticsResultsView'
import { generateUAT, generateAnalytics } from './api/client'

function App() {
  const [uploadResult, setUploadResult] = useState(null)
  const [uatResult, setUatResult] = useState(null)
  const [uatStatus, setUatStatus] = useState('idle')
  const [uatError, setUatError] = useState('')
  const [analyticsResult, setAnalyticsResult] = useState(null)
  const [analyticsStatus, setAnalyticsStatus] = useState('idle')
  const [analyticsError, setAnalyticsError] = useState('')

  function handleNewUpload(result) {
    setUploadResult(result)
    setUatResult(null)
    setUatStatus('idle')
    setAnalyticsResult(null)
    setAnalyticsStatus('idle')
  }

  async function handleGenerateUAT() {
    setUatStatus('loading')
    setUatError('')
    try {
      const result = await generateUAT(uploadResult.job_id)
      setUatResult(result)
      setUatStatus('idle')
    } catch (err) {
      setUatStatus('error')
      setUatError(err.message)
    }
  }

  async function handleGenerateAnalytics() {
    setAnalyticsStatus('loading')
    setAnalyticsError('')
    try {
      const result = await generateAnalytics(uploadResult.job_id)
      setAnalyticsResult(result)
      setAnalyticsStatus('idle')
    } catch (err) {
      setAnalyticsStatus('error')
      setAnalyticsError(err.message)
    }
  }

  return (
    <div style={{ maxWidth: '900px', margin: '3rem auto', padding: '0 1rem' }}>
      <h1>AgentDesk</h1>
      <p>Agentic document/data transformation toolkit</p>

      <UploadZone onUploadComplete={handleNewUpload} />

      {uploadResult && <FilePreviewCard uploadResult={uploadResult} />}

      {uploadResult && uploadResult.category === 'document' && (
        <div style={{ marginTop: '1rem' }}>
          <button onClick={handleGenerateUAT} disabled={uatStatus === 'loading'}>
            {uatStatus === 'loading' ? 'Generating UAT Spec...' : 'Generate UAT Spec from SRS Document'}
          </button>
          {uatStatus === 'error' && <p style={{ color: '#ff6b6b' }}>Error: {uatError}</p>}
        </div>
      )}

      {uploadResult && uploadResult.category === 'table' && (
        <div style={{ marginTop: '1rem' }}>
          <button onClick={handleGenerateAnalytics} disabled={analyticsStatus === 'loading'}>
            {analyticsStatus === 'loading' ? 'Analyzing Data...' : 'Analyze Data'}
          </button>
          {analyticsStatus === 'error' && <p style={{ color: '#ff6b6b' }}>Error: {analyticsError}</p>}
        </div>
      )}

      {uatResult && <UATResultsTable result={uatResult} />}
      {analyticsResult && <AnalyticsResultsView result={analyticsResult} />}
    </div>
  )
}

export default App