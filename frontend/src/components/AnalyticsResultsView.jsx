import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, ScatterChart, Scatter,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
} from 'recharts'

const COLORS = ['#2563EB', '#0EA5E9', '#F59E0B', '#8B5CF6', '#10B981']

function AnalyticsResultsView({ result }) {
  return (
    <div style={{ marginTop: '1.5rem' }}>
      <h3 style={{ color: '#F1F5F9' }}>Analytics — {result.source_filename}</h3>
      <p style={{ color: '#F1F5F9' }}>{result.summary}</p>

      <h4 style={{ color: '#F1F5F9' }}>Key Insights</h4>
      <ul>
        {result.key_insights.map((insight, i) => (
          <li key={i} style={{ color: '#F1F5F9', marginBottom: '0.3rem' }}>{insight}</li>
        ))}
      </ul>

      <h4 style={{ color: '#F1F5F9' }}>Charts</h4>
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
      <p style={{ fontWeight: 600, marginBottom: '0.25rem', color: '#F1F5F9' }}>{chart.title}</p>
      <p style={{ fontSize: '0.8rem', color: '#94A3B8', marginTop: 0 }}>{chart.reason}</p>

      <ResponsiveContainer width="100%" height={280}>
        {chart.chart_type === 'bar' && (
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey="name" stroke="#64748B" />
            <YAxis stroke="#64748B" />
            <Tooltip />
            <Bar dataKey="value" fill="#2563EB" />
          </BarChart>
        )}
        {chart.chart_type === 'line' && (
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey="name" stroke="#64748B" />
            <YAxis stroke="#64748B" />
            <Tooltip />
            <Line type="monotone" dataKey="value" stroke="#2563EB" />
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
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey="index" name="Point #" stroke="#64748B" />
            <YAxis dataKey="value" name={chart.y_column} stroke="#64748B" />
            <Tooltip cursor={{ strokeDasharray: '3 3' }} />
            <Scatter data={data} fill="#EF4444" />
          </ScatterChart>
        )}
      </ResponsiveContainer>
    </div>
  )
}

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