import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/layout/Navbar';
import PageWrapper from '../components/layout/PageWrapper';
import Spinner from '../components/ui/Spinner';
import ScoreCircle from '../components/ui/ScoreCircle';
import Button from '../components/ui/Button';
import JointBarChart from '../components/charts/JointBarChart';
import ComparisonChart from '../components/charts/ComparisonChart';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function MonthlyReportPage() {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function fetchReport() {
      try {
        const res = await fetch(`${API_BASE}/api/reports/monthly/latest`);
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
    const res = await fetch(`${API_BASE}/api/reports/monthly/export`);
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'monthly_report.pdf'; a.click();
    URL.revokeObjectURL(url);
  }

  if (loading) return <><Navbar /><PageWrapper><div className="centered"><Spinner /></div></PageWrapper></>;
  if (error) return <><Navbar /><PageWrapper><p className="form-error">{error}</p></PageWrapper></>;

  const {
    day1Score = 0,
    day30Score = 0,
    overallImprovement = 0,
    consistencyScore = 0,
    jointImprovements = [],
    exerciseComparison = [],
    llmSummary = '',
  } = data || {};

  return (
    <>
      <Navbar />
      <PageWrapper title="Monthly Report">
        <div className="monthly-report">

          {/* Day 1 vs Day 30 */}
          <div className="comparison-scores">
            <div className="comp-score-card">
              <span className="comp-day-label">Day 1</span>
              <ScoreCircle score={day1Score} size={100} />
            </div>
            <div className="comp-arrow">→</div>
            <div className="comp-score-card">
              <span className="comp-day-label">Day 30</span>
              <ScoreCircle score={day30Score} size={100} />
            </div>
          </div>

          {/* Overall improvement */}
          <div className="improvement-stat">
            <span className="improvement-pct">{overallImprovement > 0 ? '+' : ''}{overallImprovement}%</span>
            <span className="improvement-label">Overall improvement</span>
          </div>

          {/* Consistency score */}
          <div className="consistency-section">
            <h3 className="section-heading">Consistency</h3>
            <ScoreCircle score={consistencyScore} size={120} />
          </div>

          {/* Exercise comparison chart */}
          <h3 className="section-heading">Exercise comparison</h3>
          <ComparisonChart data={exerciseComparison} />

          {/* Joint improvement bars */}
          <h3 className="section-heading">Per-joint improvement</h3>
          <JointBarChart data={jointImprovements} />

          {/* LLM summary */}
          {llmSummary && (
            <div className="llm-summary">
              <h3 className="section-heading">AI Summary</h3>
              <p className="llm-text">{llmSummary}</p>
            </div>
          )}

          {/* Recovery prediction link */}
          <div className="recovery-preview">
            <p>View your recovery prediction →{' '}
              <button className="inline-link" onClick={() => navigate('/feedback')}>Feedback & Prediction</button>
            </p>
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
