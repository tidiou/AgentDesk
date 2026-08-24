import { exportFlattenedExcel } from '../api/client'

function JSONFlattenResultsView({ result }) {
  return (
    <div style={{ marginTop: '1.5rem' }}>
      <h3 style={{ color: '#F1F5F9' }}>Flattened Tables — {result.source_filename}</h3>

      {result.tables.map((table) => (
        <div key={table.table_name} style={{ marginBottom: '1.5rem' }}>
          <p style={{ color: '#F1F5F9', fontWeight: 600, marginBottom: '0.25rem' }}>
            {table.table_name}
          </p>
          <p style={{ color: '#94A3B8', fontSize: '0.85rem', marginTop: 0 }}>
            {table.row_count} rows · {table.columns.length} columns
          </p>
          <div style={{ overflowX: 'auto' }}>
            <table style={tableStyle}>
              <thead>
                <tr>
                  {table.columns.map((col) => (
                    <th key={col} style={thStyle}>{col}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {table.preview_rows.map((row, i) => (
                  <tr key={i}>
                    {table.columns.map((col) => (
                      <td key={col} style={tdStyle}>{String(row[col] ?? '')}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ))}

      <button
        onClick={() => exportFlattenedExcel(result)}
        style={{
          backgroundColor: 'transparent',
          color: '#3B82F6',
          border: '1px solid #3B82F6',
          borderRadius: '6px',
          padding: '0.5rem 1rem',
          cursor: 'pointer',
          fontSize: '0.9rem',
        }}
      >
        Download as Excel (one sheet per table)
      </button>
    </div>
  )
}

const tableStyle = { borderCollapse: 'collapse', width: '100%', fontSize: '0.8rem' }
const thStyle = { textAlign: 'left', padding: '0.4rem', borderBottom: '1px solid #334155', color: '#94A3B8' }
const tdStyle = { padding: '0.4rem', borderBottom: '1px solid #334155', color: '#F1F5F9' }

export default JSONFlattenResultsView