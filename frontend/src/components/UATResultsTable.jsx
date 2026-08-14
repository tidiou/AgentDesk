function UATResultsTable({ result }) {
  return (
    <div style={{ marginTop: '1.5rem' }}>
      <h3>UAT Test Cases — {result.source_filename}</h3>
      <div style={{ overflowX: 'auto' }}>
        <table style={tableStyle}>
          <thead>
            <tr>
              <th style={thStyle}>ID</th>
              <th style={thStyle}>Requirement</th>
              <th style={thStyle}>Title</th>
              <th style={thStyle}>Steps</th>
              <th style={thStyle}>Expected Result</th>
              <th style={thStyle}>Priority</th>
            </tr>
          </thead>
          <tbody>
            {result.test_cases.map((tc) => (
              <tr key={tc.id}>
                <td style={tdStyle}>{tc.id}</td>
                <td style={tdStyle}>{tc.requirement_ref}</td>
                <td style={tdStyle}>{tc.title}</td>
                <td style={tdStyle}>
                  <ol style={{ margin: 0, paddingLeft: '1.2rem' }}>
                    {tc.steps.map((step, i) => <li key={i}>{step}</li>)}
                  </ol>
                </td>
                <td style={tdStyle}>{tc.expected_result}</td>
                <td style={tdStyle}>{tc.priority}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

const tableStyle = { borderCollapse: 'collapse', width: '100%', fontSize: '0.85rem' }
const thStyle = { textAlign: 'left', padding: '0.5rem', borderBottom: '1px solid #444', color: '#aaa' }
const tdStyle = { padding: '0.5rem', borderBottom: '1px solid #2a2a2a', verticalAlign: 'top' }

export default UATResultsTable