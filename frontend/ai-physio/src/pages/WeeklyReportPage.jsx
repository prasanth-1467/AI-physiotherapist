import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/layout/Navbar';
import PageWrapper from '../components/layout/PageWrapper';
import Spinner from '../components/ui/Spinner';
import Badge from '../components/ui/Badge';
import ProgressBar from '../components/ui/ProgressBar';
import Button from '../components/ui/Button';
import PerformanceLineChart from '../components/charts/PerformanceLineChart';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function WeeklyReportPage() {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function fetchReport() {
      try {
        const res = await fetch(`${API_BASE}/api/reports/weekly/latest`);
        if (!res.ok) throw new Error(`Server error ${res.status}`);
        setData(await res.json());
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchReport();
  }, []);

  async function handleDownload() {
    const res = await fetch(`${API_BASE}/api/reports/weekly/export`);
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'weekly_report.pdf'; a.click();
    URL.revokeObjectURL(url);
  }

  if (loading) return <><Navbar /><PageWrapper><div className="centered"><Spinner /></div></PageWrapper></>;
  if (error) return <><Navbar /><PageWrapper><p className="form-error">{error}</p></PageWrapper></>;

  const {
    daysAttended = 0,
    averageScore = 0,
    trend = 'stable',
    exerciseScores = [],
    dailyScores = [],
    weakJoints = [],
    strongJoints = [],
  } = data || {};

  return (
    <>
      <Navbar />
      <PageWrapper title="Weekly Report">
        <div className="weekly-report">

          {/* Summary card */}
          <div className="report-summary-card">
            <div className="report-stat"><span className="rs-val">{daysAttended}</span><span className="rs-label">Days attended</span></div>
            <div className="report-stat"><span className="rs-val">{averageScore}</span><span className="rs-label">Avg score</span></div>
            <div className="report-stat"><Badge label={trend} variant={trend} /></div>
          </div>

          {/* Line chart */}
          <h3 className="section-heading">Daily performance</h3>
          <PerformanceLineChart data={dailyScores} />

          {/* Per-exercise scores */}
          <h3 className="section-heading">Exercise breakdown</h3>
          <div className="exercise-scores">
            {exerciseScores.map((es, i) => (
              <ProgressBar key={i} percentage={es.score} label={es.name} color="#4caf50" />
            ))}
          </div>

          {/* Joint lists */}
          <div className="joint-lists">
            <div className="joint-list-col">
              <h4>Weak joints</h4>
              {weakJoints.length === 0 ? <p>None identified.</p> : <ul>{weakJoints.map((j, i) => <li key={i}>{j}</li>)}</ul>}
            </div>
            <div className="joint-list-col">
              <h4>Strong joints</h4>
              {strongJoints.length === 0 ? <p>None identified.</p> : <ul>{strongJoints.map((j, i) => <li key={i}>{j}</li>)}</ul>}
            </div>
          </div>

          <div className="report-actions">
            <Button label="Download PDF" variant="secondary" onClick={handleDownload} />
            <Button label="Back to Dashboard" variant="ghost" onClick={() => navigate('/dashboard')} />
          </div>
        </div>
      </PageWrapper>
    </>
  );
}
