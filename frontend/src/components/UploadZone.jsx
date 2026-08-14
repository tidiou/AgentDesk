import { useState, useRef } from 'react'
import { uploadFile } from '../api/client'

const ACCEPTED_EXTENSIONS = ['.pdf', '.docx', '.pptx', '.txt', '.csv', '.xlsx', '.xls', '.json']

function UploadZone({ onUploadComplete }) {
  const [isDragging, setIsDragging] = useState(false)
  const [status, setStatus] = useState('idle') // idle | uploading | error
  const [errorMessage, setErrorMessage] = useState('')
  const fileInputRef = useRef(null)

  async function handleFile(file) {
    setStatus('uploading')
    setErrorMessage('')
    try {
      const result = await uploadFile(file)
      setStatus('idle')
      onUploadComplete(result)
    } catch (err) {
      setStatus('error')
      setErrorMessage(err.message)
    }
  }

  function handleDrop(e) {
    e.preventDefault()
    setIsDragging(false)
    const file = e.dataTransfer.files[0]
    if (file) handleFile(file)
  }

  function handleBrowseSelect(e) {
    const file = e.target.files[0]
    if (file) handleFile(file)
  }

  return (
    <div
      onDragOver={(e) => { e.preventDefault(); setIsDragging(true) }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={handleDrop}
      onClick={() => fileInputRef.current.click()}
      style={{
        border: `2px dashed ${isDragging ? '#5b9dff' : '#555'}`,
        borderRadius: '8px',
        padding: '3rem',
        textAlign: 'center',
        cursor: 'pointer',
        backgroundColor: isDragging ? '#22262e' : 'transparent',
      }}
    >
      <input
        ref={fileInputRef}
        type="file"
        accept={ACCEPTED_EXTENSIONS.join(',')}
        onChange={handleBrowseSelect}
        style={{ display: 'none' }}
      />

      {status === 'uploading' && <p>Uploading...</p>}
      {status === 'idle' && (
        <p>Drag & drop a file here, or click to browse<br />
          <small>{ACCEPTED_EXTENSIONS.join(', ')}</small>
        </p>
      )}
      {status === 'error' && <p style={{ color: '#ff6b6b' }}>Error: {errorMessage}</p>}
    </div>
  )
}

export default UploadZone