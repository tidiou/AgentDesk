import { useState } from 'react'
import UploadZone from './components/UploadZone'
import FilePreviewCard from './components/FilePreviewCard'
import UATResultsTable from './components/UATResultsTable'
import { generateUAT } from './api/client'

function App() {
  const [uploadResult, setUploadResult] = useState(null)
  const [uatResult, setUatResult] = useState(null)
  const [uatStatus, setUatStatus] = useState('idle') // idle | loading | error
  const [uatError, setUatError] = useState('')

  function handleNewUpload(result) {
    setUploadResult(result)
    setUatResult(null)     // clear any previous run's results
    setUatStatus('idle')
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
          {uatStatus === 'error' && (
            <p style={{ color: '#ff6b6b' }}>Error: {uatError}</p>
          )}
        </div>
      )}

      {uatResult && <UATResultsTable result={uatResult} />}
    </div>
  )
}

export default App