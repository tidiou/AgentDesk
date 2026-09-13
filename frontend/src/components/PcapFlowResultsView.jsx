function PcapFlowResultsView({ result }) {
  return (
    <div style={{ marginTop: '1.5rem' }}>
      <h3 style={{ color: '#F1F5F9' }}>Network Flows — {result.source_filename}</h3>
      <p style={{ color: '#F1F5F9' }}>{result.summary}</p>

      <h4 style={{ color: '#F1F5F9' }}>Key Insights</h4>
      <ul>
        {result.key_insights.map((insight, i) => (
          <li key={i} style={{ color: '#F1F5F9', marginBottom: '0.3rem' }}>{insight}</li>
        ))}
      </ul>

      <h4 style={{ color: '#F1F5F9' }}>Conversations ({result.flows.length})</h4>
      <div style={{ overflowX: 'auto' }}>
        <table style={tableStyle}>
          <thead>
            <tr>
              <th style={thStyle}>Endpoint A</th>
              <th style={thStyle}>Endpoint B</th>
              <th style={thStyle}>Protocol</th>
              <th style={thStyle}>Packets</th>
              <th style={thStyle}>Bytes</th>
              <th style={thStyle}>Duration (s)</th>
            </tr>
          </thead>
          <tbody>
            {result.flows.slice(0, 50).map((flow, i) => (
              <tr key={i}>
                <td style={tdStyle}>{flow.endpoint_a}</td>
                <td style={tdStyle}>{flow.endpoint_b}</td>
                <td style={tdStyle}>{flow.protocol}</td>
                <td style={tdStyle}>{flow.packet_count}</td>
                <td style={tdStyle}>{flow.total_bytes.toLocaleString()}</td>
                <td style={tdStyle}>{flow.duration_seconds}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

const tableStyle = { borderCollapse: 'collapse', width: '100%', fontSize: '0.8rem' }
const thStyle = { textAlign: 'left', padding: '0.4rem', borderBottom: '1px solid #334155', color: '#94A3B8' }
const tdStyle = { padding: '0.4rem', borderBottom: '1px solid #334155', color: '#F1F5F9' }

export default PcapFlowResultsView