import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, ScatterChart, Scatter,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
} from 'recharts'

const COLORS = ['#5b9dff', '#63d2a5', '#f0c674', '#f0798a', '#a78bfa']

function AnalyticsResultsView({ result }) {
  return (
    <div style={{ marginTop: '1.5rem' }}>
      <h3>Analytics — {result.source_filename}</h3>
      <p style={{ color: '#ccc' }}>{result.summary}</p>

      <h4>Key Insights</h4>
      <ul>
        {result.key_insights.map((insight, i) => (
          <li key={i} style={{ color: '#ccc', marginBottom: '0.3rem' }}>{insight}</li>
        ))}
      </ul>

      <h4>Charts</h4>
      {result.chart_recommendations.map((chart, i) => (
        <ChartBlock key={i} chart={chart} rawStats={result.raw_stats} />
      ))}
    </div>
  )
}

function ChartBlock({ chart, rawStats }) {
  const data = buildChartData(chart, rawStats)

  return (
    <div style={{ marginBottom: '2rem' }}>
      <p style={{ fontWeight: 600, marginBottom: '0.25rem' }}>{chart.title}</p>
      <p style={{ fontSize: '0.8rem', color: '#999', marginTop: 0 }}>{chart.reason}</p>

      <ResponsiveContainer width="100%" height={280}>
        {chart.chart_type === 'bar' && (
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#333" />
            <XAxis dataKey="name" stroke="#999" />
            <YAxis stroke="#999" />
            <Tooltip />
            <Bar dataKey="value" fill="#5b9dff" />
          </BarChart>
        )}
        {chart.chart_type === 'line' && (
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#333" />
            <XAxis dataKey="name" stroke="#999" />
            <YAxis stroke="#999" />
            <Tooltip />
            <Line type="monotone" dataKey="value" stroke="#5b9dff" />
          </LineChart>
        )}
        {chart.chart_type === 'pie' && (
          <PieChart>
            <Pie data={data} dataKey="value" nameKey="name" outerRadius={100} label>
              {data.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        )}
       {chart.chart_type === 'scatter' && (
  <ScatterChart>
    <CartesianGrid strokeDasharray="3 3" stroke="#333" />
    <XAxis dataKey="index" name="Point #" stroke="#999" />
    <YAxis dataKey="value" name={chart.y_column} stroke="#999" />
    <Tooltip cursor={{ strokeDasharray: '3 3' }} />
    <Scatter data={data} fill="#f0798a" />
  </ScatterChart>
)}
      </ResponsiveContainer>
    </div>
  )
}

// Translates a chart recommendation + raw_stats into recharts' expected
// [{ name, value }] shape. Uses categorical top_values or numeric summary,
// since we don't have row-level data on the frontend — only the stats.
function buildChartData(chart, rawStats) {
  if (chart.chart_type === 'scatter') {
    const outlierStats = rawStats.outliers?.[chart.y_column]
    if (outlierStats?.sample_values) {
      return outlierStats.sample_values.map((value, i) => ({ index: i + 1, value }))
    }
    return []
  }

  const catStats = rawStats.categorical_summary?.[chart.x_column]
  if (catStats?.top_values) {
    return Object.entries(catStats.top_values).map(([name, value]) => ({ name, value }))
  }

  const numStats = rawStats.numeric_summary?.[chart.y_column]
  if (numStats) {
    return [
      { name: 'Min', value: numStats.min },
      { name: 'Mean', value: numStats.mean },
      { name: 'Max', value: numStats.max },
    ]
  }

  return []
}

export default AnalyticsResultsView