import { useState, useRef, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/layout/Navbar';
import PageWrapper from '../components/layout/PageWrapper';
import Button from '../components/ui/Button';
import ProgressBar from '../components/ui/ProgressBar';
import Spinner from '../components/ui/Spinner';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const POLL_INTERVAL_MS = 2000;

function formatBytes(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1048576) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1048576).toFixed(1)} MB`;
}

export default function ReportUploadPage() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [status, setStatus] = useState('idle'); // idle | uploading | analyzing | error
  const [errorMsg, setErrorMsg] = useState('');
  const fileInputRef = useRef(null);
  const pollRef = useRef(null);

  function handleFile(f) {
    if (!f) return;
    const ext = f.name.split('.').pop().toLowerCase();
    if (!['pdf', 'txt'].includes(ext)) {
      setErrorMsg('Only PDF or .txt files are supported.');
      return;
    }
    setErrorMsg('');
    setFile(f);
  }

  function handleDrop(e) {
    e.preventDefault();
    setDragOver(false);
    handleFile(e.dataTransfer.files[0]);
  }

  function pollStatus(taskId) {
    pollRef.current = setInterval(async () => {
      try {
        const res = await fetch(`${API_BASE}/api/report/status?task_id=${taskId}`);
        const data = await res.json();
        if (data.status === 'done') {
          clearInterval(pollRef.current);
          navigate('/session/summary', { state: { findings: data.findings } });
        } else if (data.status === 'error') {
          clearInterval(pollRef.current);
          setStatus('error');
          setErrorMsg(data.message || 'Analysis failed. Please try again.');
        }
      } catch (_) {
        clearInterval(pollRef.current);
        setStatus('error');
        setErrorMsg('Lost connection while polling. Please retry.');
      }
    }, POLL_INTERVAL_MS);
  }

  async function handleUpload() {
    if (!file) return;
    setStatus('uploading');
    setUploadProgress(0);
    setErrorMsg('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      // Simulate progress with XHR for real progress events
      const taskId = await new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.upload.addEventListener('progress', e => {
          if (e.lengthComputable) {
            setUploadProgress(Math.round((e.loaded / e.total) * 100));
          }
        });
        xhr.addEventListener('load', () => {
          if (xhr.status >= 200 && xhr.status < 300) {
            try { resolve(JSON.parse(xhr.responseText).task_id); }
            catch (_) { reject(new Error('Invalid server response.')); }
          } else {
            reject(new Error(`Upload failed (${xhr.status}).`));
          }
        });
        xhr.addEventListener('error', () => reject(new Error('Network error during upload.')));
        xhr.open('POST', `${API_BASE}/api/report/upload`);
        xhr.send(formData);
      });

      setStatus('analyzing');
      pollStatus(taskId);
    } catch (err) {
      setStatus('error');
      setErrorMsg(err.message);
    }
  }

  return (
    <>
      <Navbar />
      <PageWrapper title="Upload Patient Report">
        <div className="report-upload-wrapper">

          {/* Drop zone */}
          <div
            className={`drop-zone ${dragOver ? 'drop-zone-active' : ''} ${file ? 'drop-zone-filled' : ''}`}
            onDragOver={e => { e.preventDefault(); setDragOver(true); }}
            onDragLeave={() => setDragOver(false)}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,.txt"
              style={{ display: 'none' }}
              onChange={e => handleFile(e.target.files[0])}
            />
            {file ? (
              <div className="drop-zone-preview">
                <span className="drop-file-name">{file.name}</span>
                <span className="drop-file-size">{formatBytes(file.size)}</span>
              </div>
            ) : (
              <div className="drop-zone-prompt">
                <span className="drop-icon">📁</span>
                <p>Drag & drop your PDF or .txt report here, or click to browse</p>
              </div>
            )}
          </div>

          {errorMsg && <p className="upload-error">{errorMsg}</p>}

          {/* Upload progress */}
          {status === 'uploading' && (
            <div className="upload-progress">
              <ProgressBar percentage={uploadProgress} label="Uploading..." color="#4caf50" />
            </div>
          )}

          {/* Analyzing state */}
          {status === 'analyzing' && (
            <div className="analyzing-state">
              <Spinner />
              <p>Analyzing your report with AI…</p>
            </div>
          )}

          {/* Upload button */}
          {status === 'idle' || status === 'error' ? (
            <Button
              label="Upload Report"
              variant="primary"
              disabled={!file}
              onClick={handleUpload}
            />
          ) : null}
        </div>
      </PageWrapper>
    </>
  );
}
