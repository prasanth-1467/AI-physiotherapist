import { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useGlobalState } from '../context/GlobalStateProvider';
import Navbar from '../components/layout/Navbar';
import PageWrapper from '../components/layout/PageWrapper';
import ExerciseCard from '../components/exercise/ExerciseCard';

const SESSION_LOG_KEY = 'ai_physio_session_log';

function getLast7Days() {
  const days = [];
  for (let i = 6; i >= 0; i--) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    days.push(d.toISOString().split('T')[0]);
  }
  return days;
}

export default function DashboardPage() {
  const navigate = useNavigate();
  const { name, suggestionData } = useGlobalState();
  const [sessionLog, setSessionLog] = useState([]);
  const [weeklyReady, setWeeklyReady] = useState(false);
  const [monthlyDue, setMonthlyDue] = useState(false);

  useEffect(() => {
    try {
      const log = JSON.parse(localStorage.getItem(SESSION_LOG_KEY) || '[]');
      setSessionLog(log);
      setWeeklyReady(log.length >= 5);
      setMonthlyDue(log.length >= 28);
    } catch (_) {}
  }, []);

  const last7 = getLast7Days();
  const logDates = new Set(sessionLog.map(e => e.date));
  const sessionsThisWeek = last7.filter(d => logDates.has(d)).length;
  const weekNumber = Math.ceil(sessionLog.length / 5) || 1;
  const avgScore = sessionLog.length
    ? Math.round(sessionLog.reduce((s, e) => s + (e.score || 0), 0) / sessionLog.length)
    : 0;

  return (
    <>
      <Navbar />
      <PageWrapper>
        <div className="dashboard">
          {/* Notification banners */}
          {weeklyReady && (
            <div className="notification-banner banner-info">
              Your weekly report is ready!{' '}
              <Link to="/progress/weekly" className="banner-link">View now →</Link>
            </div>
          )}
          {monthlyDue && (
            <div className="notification-banner banner-warn">
              Monthly assessment due.{' '}
              <Link to="/progress/monthly" className="banner-link">View monthly report →</Link>
            </div>
          )}

          {/* Greeting */}
          <h1 className="dashboard-greeting">Hello, {name || 'there'} 👋</h1>

          {/* Quick stats */}
          <div className="dashboard-stats">
            <div className="stat-card">
              <span className="stat-value">{sessionLog.length}</span>
              <span className="stat-label">Sessions done</span>
            </div>
            <div className="stat-card">
              <span className="stat-value">Week {weekNumber}</span>
              <span className="stat-label">Current week</span>
            </div>
            <div className="stat-card">
              <span className="stat-value">{avgScore}</span>
              <span className="stat-label">Avg score</span>
            </div>
          </div>

          {/* 7-day streak */}
          <div className="streak-section">
            <h3 className="streak-title">7-day streak</h3>
            <div className="streak-dots">
              {last7.map(day => (
                <div key={day} className={`streak-dot ${logDates.has(day) ? 'dot-done' : 'dot-miss'}`} title={day} />
              ))}
            </div>
          </div>

          {/* Action cards */}
          <div className="dashboard-actions">
            <div className="action-card" onClick={() => navigate('/session/live')}>
              <span className="action-icon">🏃</span>
              <h3>Start Live Exercise Session</h3>
              <p>Begin a guided session with real-time AI feedback.</p>
            </div>
            <div className="action-card" onClick={() => navigate('/report/upload')}>
              <span className="action-icon">📄</span>
              <h3>Upload Patient Report</h3>
              <p>Upload a PDF or text report to generate a personalised plan.</p>
            </div>
          </div>

          {/* Today's exercise preview */}
          {suggestionData && suggestionData.length > 0 && (
            <div className="dashboard-preview">
              <h3 className="preview-title">Today's exercise</h3>
              <ExerciseCard exercise={suggestionData[0]} />
            </div>
          )}

          {/* Report links */}
          {sessionLog.length > 0 && (
            <div className="dashboard-links">
              <Link to="/progress/weekly" className="report-link">📊 Weekly Report</Link>
              {sessionLog.length >= 28 && (
                <Link to="/progress/monthly" className="report-link">📈 Monthly Report</Link>
              )}
            </div>
          )}
        </div>
      </PageWrapper>
    </>
  );
}
