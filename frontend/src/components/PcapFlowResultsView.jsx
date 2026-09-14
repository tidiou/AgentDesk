import { useState, useMemo } from 'react'

function PcapFlowResultsView({ result }) {
  const [protocolFilter, setProtocolFilter] = useState('All protocols')

  const availableProtocols = useMemo(() => {
    const found = new Set(result.packets.map((p) => p.protocol))
    return ['All protocols', ...Array.from(found).sort()]
  }, [result.packets])

  const filteredPackets = useMemo(() => {
    if (protocolFilter === 'All protocols') return result.packets
    return result.packets.filter((p) => p.protocol === protocolFilter)
  }, [result.packets, protocolFilter])

  return (
    <div style={{ marginTop: '1.5rem' }}>
      <h3 style={{ color: '#F1F5F9' }}>Packet Capture — {result.source_filename}</h3>
      <p style={{ color: '#F1F5F9' }}>{result.summary}</p>

      <h4 style={{ color: '#F1F5F9' }}>Key Insights</h4>
      <ul>
        {result.key_insights.map((insight, i) => (
          <li key={i} style={{ color: '#F1F5F9', marginBottom: '0.3rem' }}>{insight}</li>
        ))}
      </ul>

      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginTop: '1rem' }}>
        <label style={{ color: '#94A3B8', fontSize: '0.85rem' }}>Filter by protocol:</label>
        <select
          value={protocolFilter}
          onChange={(e) => setProtocolFilter(e.target.value)}
          style={selectStyle}
        >
          {availableProtocols.map((p) => (
            <option key={p} value={p}>{p}</option>
          ))}
        </select>
      </div>

      <p style={{ color: '#94A3B8', fontSize: '0.8rem', marginTop: '0.5rem' }}>
        Showing {filteredPackets.length} of {result.total_packet_count} packets
        {result.total_packet_count > result.packets.length && ` (capped at ${result.packets.length} for display)`}
      </p>

      <div style={{ overflowX: 'auto', maxHeight: '500px', overflowY: 'auto' }}>
        <table style={tableStyle}>
          <thead>
            <tr>
              <th style={thStyle}>Time</th>
              <th style={thStyle}>Source</th>
              <th style={thStyle}>Destination</th>
              <th style={thStyle}>Protocol</th>
              <th style={thStyle}>Info</th>
            </tr>
          </thead>
          <tbody>
            {filteredPackets.map((pkt, i) => (
              <tr key={i}>
                <td style={tdStyle}>{pkt.time.toFixed(6)}</td>
                <td style={tdStyle}>{pkt.source}</td>
                <td style={tdStyle}>{pkt.destination}</td>
                <td style={tdStyle}>{pkt.protocol}</td>
                <td style={{ ...tdStyle, fontFamily: 'monospace', fontSize: '0.75rem' }}>{pkt.info}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

const selectStyle = {
  backgroundColor: '#1E293B',
  color: '#F1F5F9',
  border: '1px solid #334155',
  borderRadius: '6px',
  padding: '0.3rem 0.6rem',
  fontSize: '0.85rem',
}
const tableStyle = { borderCollapse: 'collapse', width: '100%', fontSize: '0.8rem' }
const thStyle = { textAlign: 'left', padding: '0.4rem', borderBottom: '1px solid #334155', color: '#94A3B8', position: 'sticky', top: 0, backgroundColor: '#0F172A' }
const tdStyle = { padding: '0.4rem', borderBottom: '1px solid #334155', color: '#F1F5F9' }

export default PcapFlowResultsView