import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/layout/Navbar';
import PageWrapper from '../components/layout/PageWrapper';
import Spinner from '../components/ui/Spinner';
import Button from '../components/ui/Button';
import RecoveryPredictionCard from '../components/feedback/RecoveryPredictionCard';
import FeedbackMessageCard from '../components/feedback/FeedbackMessageCard';
import FeedbackTimeline from '../components/feedback/FeedbackTimeline';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function FeedbackPage() {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function fetchFeedback() {
      try {
        const res = await fetch(`${API_BASE}/api/feedback/latest`);
        if (!res.ok) throw new Error(`Server error ${res.status}`);
        setData(await res.json());
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchFeedback();
  }, []);

  if (loading) return <><Navbar /><PageWrapper><div className="centered"><Spinner /></div></PageWrapper></>;
  if (error) return <><Navbar /><PageWrapper><p className="form-error">{error}</p></PageWrapper></>;

  const {
    predictedDate = null,
    daysRemaining = null,
    confidence = 0,
    message = '',
    sentiment = 'motivating',
    history = [],
  } = data || {};

  return (
    <>
      <Navbar />
      <PageWrapper title="Feedback & Recovery">
        <div className="feedback-page">
          <RecoveryPredictionCard
            predictedDate={predictedDate}
            daysRemaining={daysRemaining}
            confidence={confidence}
          />
          <FeedbackMessageCard message={message} sentiment={sentiment} />
          <h3 className="section-heading">Past feedback</h3>
          <FeedbackTimeline entries={history} />
          <div className="report-actions">
            <Button label="Back to Dashboard" variant="ghost" onClick={() => navigate('/dashboard')} />
          </div>
        </div>
      </PageWrapper>
    </>
  );
}
