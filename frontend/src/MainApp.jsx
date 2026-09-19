import { useState } from 'react'
import UploadZone from './components/UploadZone'
import FilePreviewCard from './components/FilePreviewCard'
import UATResultsTable from './components/UATResultsTable'
import AnalyticsResultsView from './components/AnalyticsResultsView'
import SummaryResultsView from './components/SummaryResultsView'
import JSONFlattenResultsView from './components/JSONFlattenResultsView'
import PcapFlowResultsView from './components/PcapFlowResultsView'
import ShareButton from './components/ShareButton'
import MCPAgentPanel from './components/MCPAgentPanel'
import {
  generateUAT, generateAnalytics, exportUATExcel, generateSummary,
  generateJSONFlatten, generatePcapFlows,
} from './api/client'

const buttonStyle = {
  backgroundColor: '#3B82F6',
  color: '#F1F5F9',
  border: 'none',
  borderRadius: '6px',
  padding: '0.6rem 1.1rem',
  cursor: 'pointer',
  fontSize: '0.9rem',
}
const buttonDisabledStyle = { ...buttonStyle, backgroundColor: '#1E3A8A', cursor: 'not-allowed' }
const secondaryButtonStyle = {
  backgroundColor: 'transparent',
  color: '#3B82F6',
  border: '1px solid #3B82F6',
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

  const [pcapResult, setPcapResult] = useState(null)
  const [pcapStatus, setPcapStatus] = useState('idle')
  const [pcapError, setPcapError] = useState('')

  function handleNewUpload(result) {
    setUploadResult(result)
    setUatResult(null); setUatStatus('idle')
    setAnalyticsResult(null); setAnalyticsStatus('idle')
    setSummaryResult(null); setSummaryStatus('idle')
    setFlattenResult(null); setFlattenStatus('idle')
    setPcapResult(null); setPcapStatus('idle')
  }

  async function handleGenerateUAT() {
    setUatStatus('loading'); setUatError('')
    try {
      setUatResult(await generateUAT(uploadResult.job_id))
      setUatStatus('idle')
    } catch (err) { setUatStatus('error'); setUatError(err.message) }
  }

  async function handleGenerateAnalytics() {
    setAnalyticsStatus('loading'); setAnalyticsError('')
    try {
      setAnalyticsResult(await generateAnalytics(uploadResult.job_id))
      setAnalyticsStatus('idle')
    } catch (err) { setAnalyticsStatus('error'); setAnalyticsError(err.message) }
  }

  async function handleGenerateSummary() {
    setSummaryStatus('loading'); setSummaryError('')
    try {
      setSummaryResult(await generateSummary(uploadResult.job_id))
      setSummaryStatus('idle')
    } catch (err) { setSummaryStatus('error'); setSummaryError(err.message) }
  }

  async function handleGenerateFlatten() {
    setFlattenStatus('loading'); setFlattenError('')
    try {
      setFlattenResult(await generateJSONFlatten(uploadResult.job_id))
      setFlattenStatus('idle')
    } catch (err) { setFlattenStatus('error'); setFlattenError(err.message) }
  }

  async function handleGeneratePcapFlows() {
    setPcapStatus('loading'); setPcapError('')
    try {
      setPcapResult(await generatePcapFlows(uploadResult.job_id))
      setPcapStatus('idle')
    } catch (err) { setPcapStatus('error'); setPcapError(err.message) }
  }

  return (
    <div style={{ maxWidth: '900px', margin: '3rem auto', padding: '0 1rem' }}>
      <h1 style={{ color: '#3B82F6', marginBottom: '0.2rem' }}>AgentDesk</h1>
      <p style={{ color: '#94A3B8' }}>Agentic document/data transformation toolkit</p>

      <UploadZone onUploadComplete={handleNewUpload} />

      {uploadResult && <FilePreviewCard uploadResult={uploadResult} />}

      {uploadResult && uploadResult.category === 'document' && (
        <div style={{ marginTop: '1rem', display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
          <button onClick={handleGenerateUAT} disabled={uatStatus === 'loading'} style={uatStatus === 'loading' ? buttonDisabledStyle : buttonStyle}>
            {uatStatus === 'loading' ? 'Generating UAT Spec...' : 'Generate UAT Spec from SRS Document'}
          </button>
          <button onClick={handleGenerateSummary} disabled={summaryStatus === 'loading'} style={summaryStatus === 'loading' ? buttonDisabledStyle : buttonStyle}>
            {summaryStatus === 'loading' ? 'Summarizing...' : 'Generate a Summary of the Document'}
          </button>
        </div>
      )}
      {uatStatus === 'error' && <p style={{ color: '#F87171' }}>Error: {uatError}</p>}
      {summaryStatus === 'error' && <p style={{ color: '#F87171' }}>Error: {summaryError}</p>}

      {uploadResult && uploadResult.category === 'table' && (
        <div style={{ marginTop: '1rem' }}>
          <button onClick={handleGenerateAnalytics} disabled={analyticsStatus === 'loading'} style={analyticsStatus === 'loading' ? buttonDisabledStyle : buttonStyle}>
            {analyticsStatus === 'loading' ? 'Analyzing Data...' : 'Analyze Data'}
          </button>
          {analyticsStatus === 'error' && <p style={{ color: '#F87171' }}>Error: {analyticsError}</p>}
        </div>
      )}

      {uploadResult && uploadResult.category === 'structured' && (
        <div style={{ marginTop: '1rem' }}>
          <button onClick={handleGenerateFlatten} disabled={flattenStatus === 'loading'} style={flattenStatus === 'loading' ? buttonDisabledStyle : buttonStyle}>
            {flattenStatus === 'loading' ? 'Flattening...' : 'Flatten JSON to Table'}
          </button>
          {flattenStatus === 'error' && <p style={{ color: '#F87171' }}>Error: {flattenError}</p>}
        </div>
      )}

      {uploadResult && uploadResult.category === 'network' && (
        <div style={{ marginTop: '1rem' }}>
          <button onClick={handleGeneratePcapFlows} disabled={pcapStatus === 'loading'} style={pcapStatus === 'loading' ? buttonDisabledStyle : buttonStyle}>
            {pcapStatus === 'loading' ? 'Reconstructing Flows...' : 'Reconstruct Network Flows'}
          </button>
          {pcapStatus === 'error' && <p style={{ color: '#F87171' }}>Error: {pcapError}</p>}
        </div>
      )}

      {uatResult && (
        <>
          <UATResultsTable result={uatResult} />
          <button onClick={() => exportUATExcel(uatResult)} style={{ ...secondaryButtonStyle, marginTop: '0.5rem' }}>
            Download as Excel
          </button>
        </>
      )}

      {summaryResult && <SummaryResultsView result={summaryResult} />}
      {flattenResult && <JSONFlattenResultsView result={flattenResult} />}
      {pcapResult && <PcapFlowResultsView result={pcapResult} />}

      {analyticsResult && (
        <>
          <AnalyticsResultsView result={analyticsResult} />
          <ShareButton result={analyticsResult} />
        </>
      )}
  <MCPAgentPanel />
    </div>
  )
}

export default MainApp