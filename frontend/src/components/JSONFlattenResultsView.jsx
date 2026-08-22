import { exportFlattenedExcel } from '../api/client'

function JSONFlattenResultsView({ result }) {
  return (
    <div style={{ marginTop: '1.5rem' }}>
      <h3 style={{ color: '#F1F5F9' }}>Flattened Table — {result.source_filename}</h3>
      <p style={{ color: '#94A3B8', fontSize: '0.85rem' }}>
        {result.row_count} rows · {result.columns.length} columns
        {result.row_count > result.preview_rows.length && ` (showing first ${result.preview_rows.length})`}
      </p>

      <div style={{ overflowX: 'auto' }}>
        <table style={tableStyle}>
          <thead>
            <tr>
              {result.columns.map((col) => (
                <th key={col} style={thStyle}>{col}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {result.preview_rows.map((row, i) => (
              <tr key={i}>
                {result.columns.map((col) => (
                  <td key={col} style={tdStyle}>{String(row[col] ?? '')}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <button
        onClick={() => exportFlattenedExcel(result)}
        style={{
          marginTop: '0.75rem',
          backgroundColor: 'transparent',
          color: '#3B82F6',
          border: '1px solid #3B82F6',
          borderRadius: '6px',
          padding: '0.5rem 1rem',
          cursor: 'pointer',
          fontSize: '0.9rem',
        }}
      >
        Download as Excel
      </button>
    </div>
  )
}

const tableStyle = { borderCollapse: 'collapse', width: '100%', fontSize: '0.8rem' }
const thStyle = { textAlign: 'left', padding: '0.4rem', borderBottom: '1px solid #334155', color: '#94A3B8' }
const tdStyle = { padding: '0.4rem', borderBottom: '1px solid #334155', color: '#F1F5F9' }

export default JSONFlattenResultsView