import { useMemo, useState } from 'react'
import './App.css'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

function App() {
  const [form, setForm] = useState({
    userId: '',
    rehabGoal: '',
    reportText: '',
    weekNumber: 1,
    fps: 30,
    duration: 10,
  })
  const [reportMode, setReportMode] = useState('text')
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [result, setResult] = useState(null)

  const canRun = useMemo(() => form.userId && form.rehabGoal, [form])

  const handleChange = (key) => (event) => {
    const value = key === 'weekNumber' ? Number(event.target.value) : event.target.value
    setForm((prev) => ({ ...prev, [key]: value }))
  }

  const runPipeline = async () => {
    if (!canRun || loading) return
    setLoading(true)
    setError('')
    setResult(null)
    try {
      let res
      if (reportMode === 'pdf') {
        if (!file) {
          throw new Error('Please upload a PDF report.')
        }
        const body = new FormData()
        body.append('file', file)
        body.append('user_id', form.userId)
        body.append('rehab_goal', form.rehabGoal)
        body.append('week_number', String(form.weekNumber))
        body.append('fps', String(form.fps))
        body.append('duration', String(form.duration))
        res = await fetch(`${API_BASE}/run-pdf`, { method: 'POST', body })
      } else {
        res = await fetch(`${API_BASE}/run`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            user_id: form.userId,
            rehab_goal: form.rehabGoal,
            report_text: form.reportText,
            week_number: form.weekNumber,
            fps: form.fps,
            duration: form.duration,
          }),
        })
      }
      if (!res.ok) {
        throw new Error(`API error ${res.status}`)
      }
      const data = await res.json()
      setResult(data)
    } catch (err) {
      setError(err.message || 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="hero">
        <div className="hero-copy">
          <p className="eyebrow">AI Physiotherapist Platform</p>
          <h1>
            Precision rehab
            <span> powered by real-time biomechanics.</span>
          </h1>
          <p className="subhead">
            Upload a clinical report, stream a live session, and receive a full recovery plan
            with weekly insights and predictions.
          </p>
          <div className="hero-stats">
            <div>
              <h3>Live Pose</h3>
              <p>MediaPipe + OpenCV</p>
            </div>
            <div>
              <h3>3 Modules</h3>
              <p>Insights, tracking, and feedback</p>
            </div>
            <div>
              <h3>Full Reports</h3>
              <p>Weekly + monthly output</p>
            </div>
          </div>
        </div>
        <div className="hero-card">
          <div className="card-header">
            <div>
              <h2>Run Live Session</h2>
              <p>Camera access required for accurate tracking.</p>
            </div>
            <span className="pill">Production Mode</span>
          </div>
          <div className="hero-grid">
            <div>
              <label>Patient ID</label>
              <input placeholder="PT_001" value={form.userId} onChange={handleChange('userId')} />
            </div>
            <div>
              <label>Week</label>
              <input type="number" min="1" value={form.weekNumber} onChange={handleChange('weekNumber')} />
            </div>
          </div>
          <label>Rehab Goal</label>
          <input placeholder="Regain shoulder stability for daily lifting" value={form.rehabGoal} onChange={handleChange('rehabGoal')} />
          <div className="toggle-row">
            <button
              className={reportMode === 'text' ? 'toggle active' : 'toggle'}
              onClick={() => setReportMode('text')}
              type="button"
            >
              Paste Report
            </button>
            <button
              className={reportMode === 'pdf' ? 'toggle active' : 'toggle'}
              onClick={() => setReportMode('pdf')}
              type="button"
            >
              Upload PDF
            </button>
          </div>
          {reportMode === 'text' ? (
            <>
              <label>Report Text</label>
              <textarea rows="5" value={form.reportText} onChange={handleChange('reportText')} />
            </>
          ) : (
            <>
              <label>Report PDF</label>
              <input type="file" accept=".pdf" onChange={(e) => setFile(e.target.files?.[0] || null)} />
            </>
          )}
          <div className="hero-grid">
            <div>
              <label>FPS</label>
              <input type="number" min="5" value={form.fps} onChange={handleChange('fps')} />
            </div>
            <div>
              <label>Duration (sec)</label>
              <input type="number" min="5" value={form.duration} onChange={handleChange('duration')} />
            </div>
          </div>
          <button onClick={runPipeline} disabled={!canRun || loading}>
            {loading ? 'Running session...' : 'Run Full Session'}
          </button>
          {error ? <p className="error">{error}</p> : null}
        </div>
      </header>

      {result ? (
        <main className="dashboard">
          <section className="panel highlight">
            <div>
              <h2>Patient Summary</h2>
              <p>{result.summary?.summary_text}</p>
              <div className="meta">
                <span>Severity: {result.summary?.severity}</span>
                <span>Affected: {result.summary?.affected_body_part}</span>
                <span>Start: {result.summary?.rehab_start_date}</span>
              </div>
            </div>
            <div className="focus-card">
              <h3>Primary Injury</h3>
              <p>{result.summary?.specific_injuries?.[0]}</p>
              <span className="pill ghost">Confirmed</span>
            </div>
          </section>

          <section className="panel">
            <h2>Exercise Suggestions</h2>
            <div className="cards">
              {result.module2?.suggestions?.suggestions?.map((ex) => (
                <div className="card" key={ex.name}>
                  <h3>{ex.name}</h3>
                  <p className="muted">{ex.reason}</p>
                  <div className="tags">
                    <span>{ex.target_joint}</span>
                    <span>
                      {ex.sets}x{ex.reps}
                    </span>
                    <span>
                      {ex.ideal_angle_min}-{ex.ideal_angle_max} deg
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </section>

          <section className="panel">
            <h2>Session Results</h2>
            <div className="meta">
              <span>Average score: {result.module2?.daily_result?.average_score}</span>
              <span>Total exercises: {result.module2?.daily_result?.total_exercises}</span>
            </div>
            <div className="cards">
              {result.module2?.daily_result?.results?.map((res) => (
                <div className="card" key={res.exercise_name}>
                  <h3>{res.exercise_name}</h3>
                  <p className="muted">{res.performance_rating}</p>
                  <div className="tags">
                    <span>Score: {res.performance_score}</span>
                    <span>
                      {res.ideal_angle_min}-{res.ideal_angle_max} deg
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </section>

          <section className="panel">
            <h2>Weekly Tracker</h2>
            <div className="meta">
              <span>Days logged: {result.module2?.tracking?.days_logged}</span>
              <span>
                Week complete: {result.module2?.tracking?.week_completed ? 'Yes' : 'No'}
              </span>
              <span>Trend: {result.module2?.tracking?.analysis?.trend}</span>
            </div>
            {result.module2?.tracking?.analysis ? (
              <div className="chart">
                {result.module2.tracking.analysis.daily_scores?.map((score, idx) => (
                  <div key={idx} className="bar">
                    <div style={{ height: `${score}%` }} />
                    <span>{score}</span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="muted">Log more days to see weekly insights.</p>
            )}
          </section>

          <section className="panel">
            <h2>Pipeline Snapshot</h2>
            <p className="muted">Current predicted joint angles from the core pipeline.</p>
            <div className="tags">
              {Object.entries(result.pipeline?.results?.angles || {}).map(([joint, val]) => (
                <span key={joint}>
                  {joint}: {val} deg
                </span>
              ))}
            </div>
          </section>
        </main>
      ) : null}
    </div>
  )
}

export default App
