const API_BASE = 'http://localhost:8000/api'

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