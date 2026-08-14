function FilePreviewCard({ uploadResult }) {
  const { category, parsed } = uploadResult

  return (
    <div style={cardStyle}>
      <div style={headerStyle}>
        <span style={filenameStyle}>{parsed.filename}</span>
        <span style={badgeStyle}>{parsed.file_type}</span>
      </div>

      {category === 'document' && <DocumentPreview parsed={parsed} />}
      {category === 'table' && <TablePreview parsed={parsed} />}
      {category === 'structured' && <StructuredPreview parsed={parsed} />}
    </div>
  )
}

function DocumentPreview({ parsed }) {
  const snippet = parsed.text.slice(0, 300)
  return (
    <div>
      <p style={metaLineStyle}>
        {parsed.word_count} words
        {parsed.page_count != null && ` · ${parsed.page_count} pages`}
        {parsed.sections.length > 0 && ` · ${parsed.sections.length} sections`}
      </p>
      {parsed.sections.length > 0 && (
        <p style={metaLineStyle}>
          Sections: {parsed.sections.slice(0, 5).join(', ')}
          {parsed.sections.length > 5 && ' …'}
        </p>
      )}
      <p style={snippetStyle}>
        {snippet}{parsed.text.length > 300 && '…'}
      </p>
    </div>
  )
}

function TablePreview({ parsed }) {
  return (
    <div>
      <p style={metaLineStyle}>
        {parsed.row_count} rows · {parsed.columns.length} columns
      </p>
      <div style={{ overflowX: 'auto' }}>
        <table style={tableStyle}>
          <thead>
            <tr>
              {parsed.columns.map((col) => (
                <th key={col} style={thStyle}>{col}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {parsed.preview_rows.map((row, i) => (
              <tr key={i}>
                {parsed.columns.map((col) => (
                  <td key={col} style={tdStyle}>{String(row[col] ?? '')}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

function StructuredPreview({ parsed }) {
  return (
    <div>
      {parsed.top_level_keys.length > 0 && (
        <p style={metaLineStyle}>
          Keys: {parsed.top_level_keys.join(', ')}
        </p>
      )}
      {parsed.item_count != null && (
        <p style={metaLineStyle}>{parsed.item_count} items</p>
      )}
      <pre style={snippetStyle}>
        {JSON.stringify(parsed.data, null, 2).slice(0, 400)}…
      </pre>
    </div>
  )
}

// --- styles ---
const cardStyle = {
  border: '1px solid #333',
  borderRadius: '8px',
  padding: '1.25rem',
  marginTop: '1.5rem',
  backgroundColor: '#1e2128',
}
const headerStyle = {
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  marginBottom: '0.75rem',
}
const filenameStyle = { fontWeight: 600 }
const badgeStyle = {
  fontSize: '0.75rem',
  padding: '0.15rem 0.5rem',
  borderRadius: '4px',
  backgroundColor: '#333',
  color: '#aaa',
}
const metaLineStyle = { fontSize: '0.85rem', color: '#999', margin: '0.25rem 0' }
const snippetStyle = {
  fontSize: '0.85rem',
  color: '#ccc',
  whiteSpace: 'pre-wrap',
  marginTop: '0.5rem',
}
const tableStyle = { borderCollapse: 'collapse', width: '100%', fontSize: '0.8rem' }
const thStyle = { textAlign: 'left', padding: '0.4rem', borderBottom: '1px solid #444', color: '#aaa' }
const tdStyle = { padding: '0.4rem', borderBottom: '1px solid #2a2a2a' }

export default FilePreviewCard