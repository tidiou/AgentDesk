const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api'
export async function uploadFile(file) {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch(`${API_BASE}/ingest/upload`, {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}))
    throw new Error(errorBody.detail || `Upload failed with status ${response.status}`)
  }

  return response.json()
}

export async function generateUAT(jobId) {
  const response = await fetch(`${API_BASE}/functions/uat/generate/${jobId}`, {
    method: 'POST',
  })

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}))
    throw new Error(errorBody.detail || `UAT generation failed with status ${response.status}`)
  }

  return response.json()
}

export async function generateAnalytics(jobId) {
  const response = await fetch(`${API_BASE}/functions/analytics/generate/${jobId}`, {
    method: 'POST',
  })

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}))
    throw new Error(errorBody.detail || `Analytics generation failed with status ${response.status}`)
  }

  return response.json()
}

export async function exportUATExcel(uatResult) {
  const response = await fetch(`${API_BASE}/functions/uat/export`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(uatResult),
  })

  if (!response.ok) {
    throw new Error(`Export failed with status ${response.status}`)
  }

  const blob = await response.blob()
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `UAT_Spec_${uatResult.source_filename.replace(/\.[^/.]+$/, '')}.xlsx`
  document.body.appendChild(a)
  a.click()
  a.remove()
  window.URL.revokeObjectURL(url)
}

export async function shareAnalytics(result) {
  const response = await fetch(`${API_BASE}/functions/analytics/share`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(result),
  })
  if (!response.ok) throw new Error('Failed to create share link')
  return response.json()
}

export async function getSharedAnalytics(shareId) {
  const response = await fetch(`${API_BASE}/functions/analytics/share/${shareId}`)
  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}))
    throw new Error(errorBody.detail || 'Shared report not found')
  }
  return response.json()
}

export async function generateSummary(jobId) {
  const response = await fetch(`${API_BASE}/functions/summary/generate/${jobId}`, {
    method: 'POST',
  })

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}))
    throw new Error(errorBody.detail || `Summary generation failed with status ${response.status}`)
  }

  return response.json()
}

export async function generateJSONFlatten(jobId) {
  const response = await fetch(`${API_BASE}/functions/json-flatten/generate/${jobId}`, {
    method: 'POST',
  })
  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}))
    throw new Error(errorBody.detail || `Flattening failed with status ${response.status}`)
  }
  return response.json()
}

export async function exportFlattenedExcel(result) {
  const response = await fetch(`${API_BASE}/functions/json-flatten/export`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(result),
  })
  if (!response.ok) throw new Error('Export failed')

  const blob = await response.blob()
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `Flattened_${result.source_filename.replace(/\.[^/.]+$/, '')}.xlsx`
  document.body.appendChild(a)
  a.click()
  a.remove()
  window.URL.revokeObjectURL(url)
}