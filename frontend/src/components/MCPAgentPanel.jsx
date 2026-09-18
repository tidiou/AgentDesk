import { useState } from 'react'
import { runMCPAgent } from '../api/client'

function MCPAgentPanel() {
  const [serverUrl, setServerUrl] = useState('')
  const [credential, setCredential] = useState('')
  const [task, setTask] = useState('')
  const [result, setResult] = useState(null)
  const [status, setStatus] = useState('idle')
  const [error, setError] = useState('')

  async function handleRun() {
    setStatus('loading')
    setError('')
    setResult(null)
    try {
      const data = await runMCPAgent(serverUrl, credential, task)
      setResult(data)
      setStatus('idle')
    } catch (err) {
      setStatus('error')
      setError(err.message)
    }
  }

  return (
    <div style={{ marginTop: '3rem', borderTop: '1px solid #334155', paddingTop: '1.5rem' }}>
      <h2 style={{ color: '#3B82F6' }}>MCP Agent</h2>
      <p style={{ color: '#94A3B8', fontSize: '0.85rem' }}>
        Connect to an MCP server and describe a task for the agent to complete.
      </p>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', maxWidth: '500px' }}>
        <input
          placeholder="MCP server URL"
          value={serverUrl}
          onChange={(e) => setServerUrl(e.target.value)}
          style={inputStyle}
        />
        <input
          placeholder="Auth credential (token)"
          type="password"
          value={credential}
          onChange={(e) => setCredential(e.target.value)}
          style={inputStyle}
        />
        <textarea
          placeholder="Describe the task..."
          value={task}
          onChange={(e) => setTask(e.target.value)}
          rows={3}
          style={{ ...inputStyle, resize: 'vertical' }}
        />
        <button
          onClick={handleRun}
          disabled={status === 'loading' || !serverUrl || !task}
          style={buttonStyle}
        >
          {status === 'loading' ? 'Running Agent...' : 'Run Agent'}
        </button>
      </div>

      {status === 'error' && <p style={{ color: '#F87171' }}>Error: {error}</p>}

      {result && (
        <div style={{ marginTop: '1rem' }}>
          <p style={{ color: '#94A3B8', fontSize: '0.8rem' }}>
            Completed in {result.iterations_used} step{result.iterations_used !== 1 ? 's' : ''}
          </p>
          <h4 style={{ color: '#F1F5F9' }}>Steps</h4>
          <ol>
            {result.steps.map((step, i) => (
              <li key={i} style={{ color: '#F1F5F9', marginBottom: '0.4rem' }}>
                <strong>{step.action}</strong>
                <div style={{ color: '#94A3B8', fontSize: '0.8rem' }}>{step.detail}</div>
              </li>
            ))}
          </ol>
          <h4 style={{ color: '#F1F5F9' }}>Final Answer</h4>
          <p style={{ color: '#F1F5F9', whiteSpace: 'pre-wrap' }}>{result.final_answer}</p>
        </div>
      )}
    </div>
  )
}

const inputStyle = {
  backgroundColor: '#1E293B',
  color: '#F1F5F9',
  border: '1px solid #334155',
  borderRadius: '6px',
  padding: '0.5rem',
  fontSize: '0.85rem',
}
const buttonStyle = {
  backgroundColor: '#3B82F6',
  color: '#F1F5F9',
  border: 'none',
  borderRadius: '6px',
  padding: '0.6rem 1.1rem',
  cursor: 'pointer',
  fontSize: '0.9rem',
}

export default MCPAgentPanel