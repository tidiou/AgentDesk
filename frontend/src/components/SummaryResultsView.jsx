function SummaryResultsView({ result }) {
  return (
    <div style={{ marginTop: '1.5rem' }}>
      <h3 style={{ color: '#F1F5F9' }}>Summary — {result.source_filename}</h3>

      <h4 style={{ color: '#F1F5F9' }}>Salient Points</h4>
      <ul>
        {result.salient_points.map((point, i) => (
          <li key={i} style={{ color: '#F1F5F9', marginBottom: '0.3rem' }}>{point}</li>
        ))}
      </ul>

      <h4 style={{ color: '#F1F5F9' }}>Red Thread</h4>
      {result.red_thread ? (
        <p style={{ color: '#F1F5F9' }}>{result.red_thread}</p>
      ) : (
        <p style={{ color: '#94A3B8', fontStyle: 'italic' }}>
          No single connecting theme was identified in this document.
        </p>
      )}

      <h4 style={{ color: '#F1F5F9' }}>Takeaways</h4>
      <ul>
        {result.takeaways.map((takeaway, i) => (
          <li key={i} style={{ color: '#F1F5F9', marginBottom: '0.3rem' }}>{takeaway}</li>
        ))}
      </ul>
    </div>
  )
}

export default SummaryResultsView