import { useState } from 'react'
import UploadZone from './components/UploadZone'
import FilePreviewCard from './components/FilePreviewCard'
import UATResultsTable from './components/UATResultsTable'
import AnalyticsResultsView from './components/AnalyticsResultsView'
import SummaryResultsView from './components/SummaryResultsView'
import ShareButton from './components/ShareButton'
import JSONFlattenResultsView from './components/JSONFlattenResultsView'
import { generateUAT, generateAnalytics, exportUATExcel, generateSummary, generateJSONFlatten } from './api/client'

const buttonStyle = {
  backgroundColor: '#2563EB',
  color: '#FFFFFF',
  border: 'none',
  borderRadius: '6px',
  padding: '0.6rem 1.1rem',
  cursor: 'pointer',
  fontSize: '0.9rem',
}
const buttonDisabledStyle = { ...buttonStyle, backgroundColor: '#93C5FD', cursor: 'not-allowed' }
const secondaryButtonStyle = {
  backgroundColor: '#FFFFFF',
  color: '#2563EB',
  border: '1px solid #2563EB',
  borderRadius: '6px',
  padding: '0.5rem 1rem',
  cursor: 'pointer',
  fontSize: '0.9rem',
}

function MainApp() {
  const [uploadResult, setUploadResult] = useState(null)
  const [uatResult, setUatResult] = useState(null)
  const [uatStatus, setUatStatus] = useState('idle')
  const [uatError, setUatError] = useState('')
  const [analyticsResult, setAnalyticsResult] = useState(null)
  const [analyticsStatus, setAnalyticsStatus] = useState('idle')
  const [analyticsError, setAnalyticsError] = useState('')
  const [summaryResult, setSummaryResult] = useState(null)
  const [summaryStatus, setSummaryStatus] = useState('idle')
  const [summaryError, setSummaryError] = useState('')
  const [flattenResult, setFlattenResult] = useState(null)
  const [flattenStatus, setFlattenStatus] = useState('idle')
  const [flattenError, setFlattenError] = useState('')

  function handleNewUpload(result) {
    setUploadResult(result)
    setUatResult(null)
    setUatStatus('idle')
    setAnalyticsResult(null)
    setAnalyticsStatus('idle')
    setSummaryResult(null)
    setSummaryStatus('idle')
    setFlattenResult(null)
    setFlattenStatus('idle')
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

  async function handleGenerateSummary() {
    setSummaryStatus('loading')
    setSummaryError('')
    try {
      const result = await generateSummary(uploadResult.job_id)
      setSummaryResult(result)
      setSummaryStatus('idle')
    } catch (err) {
      setSummaryStatus('error')
      setSummaryError(err.message)
    }
  }

  async function handleGenerateFlatten() {
  setFlattenStatus('loading')
  setFlattenError('')
  try {
    const result = await generateJSONFlatten(uploadResult.job_id)
    setFlattenResult(result)
    setFlattenStatus('idle')
  } catch (err) {
    setFlattenStatus('error')
    setFlattenError(err.message)
  }
}
  return (
    <div style={{ maxWidth: '900px', margin: '3rem auto', padding: '0 1rem' }}>
      <h1 style={{ color: '#2563EB', marginBottom: '0.2rem' }}>AgentDesk</h1>
      <p style={{ color: '#64748B' }}>Agentic document/data transformation toolkit</p>

      <UploadZone onUploadComplete={handleNewUpload} />

      {uploadResult && <FilePreviewCard uploadResult={uploadResult} />}

      {uploadResult && uploadResult.category === 'document' && (
        <div style={{ marginTop: '1rem', display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
          <button
            onClick={handleGenerateUAT}
            disabled={uatStatus === 'loading'}
            style={uatStatus === 'loading' ? buttonDisabledStyle : buttonStyle}
          >
            {uatStatus === 'loading' ? 'Generating UAT Spec...' : 'Generate UAT Spec from SRS Document'}
          </button>
          <button
            onClick={handleGenerateSummary}
            disabled={summaryStatus === 'loading'}
            style={summaryStatus === 'loading' ? buttonDisabledStyle : buttonStyle}
          >
            {summaryStatus === 'loading' ? 'Summarizing...' : 'Generate a Summary of the Document'}
          </button>
        </div>
      )}
      {uatStatus === 'error' && <p style={{ color: '#F87171' }}>Error: {uatError}</p>}
      {summaryStatus === 'error' && <p style={{ color: '#F87171' }}>Error: {summaryError}</p>}

      {uploadResult && uploadResult.category === 'table' && (
        <div style={{ marginTop: '1rem' }}>
          <button
            onClick={handleGenerateAnalytics}
            disabled={analyticsStatus === 'loading'}
            style={analyticsStatus === 'loading' ? buttonDisabledStyle : buttonStyle}
          >
            {analyticsStatus === 'loading' ? 'Analyzing Data...' : 'Analyze Data'}
          </button>
          {analyticsStatus === 'error' && <p style={{ color: '#F87171' }}>Error: {analyticsError}</p>}
        </div>
      )}

      {uploadResult && uploadResult.category === 'structured' && (
  <div style={{ marginTop: '1rem' }}>
    <button
      onClick={handleGenerateFlatten}
      disabled={flattenStatus === 'loading'}
      style={flattenStatus === 'loading' ? buttonDisabledStyle : buttonStyle}
    >
      {flattenStatus === 'loading' ? 'Flattening...' : 'Flatten JSON to Table'}
    </button>
    {flattenStatus === 'error' && <p style={{ color: '#F87171' }}>Error: {flattenError}</p>}
  </div>
)}

      {uatResult && (
        <>
          <UATResultsTable result={uatResult} />
          <button
            onClick={() => exportUATExcel(uatResult)}
            style={{ ...secondaryButtonStyle, marginTop: '0.5rem' }}
          >
            Download as Excel
          </button>
        </>
      )}

      {summaryResult && <SummaryResultsView result={summaryResult} />}

      {analyticsResult && (
        <>
          <AnalyticsResultsView result={analyticsResult} />
          <ShareButton result={analyticsResult} />
        </>
      )}

     {flattenResult && <JSONFlattenResultsView result={flattenResult} />}
    </div>
  )
}

export default MainApp