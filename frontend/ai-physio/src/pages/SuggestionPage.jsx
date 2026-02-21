import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useGlobalState } from '../context/GlobalStateProvider';
import Navbar from '../components/layout/Navbar';
import PageWrapper from '../components/layout/PageWrapper';
import ExerciseCard from '../components/exercise/ExerciseCard';
import Button from '../components/ui/Button';
import Spinner from '../components/ui/Spinner';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function SuggestionPage() {
  const navigate = useNavigate();
  const { setExerciseList, setSuggestionData } = useGlobalState();
  const [exercises, setExercises] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function fetchSuggestions() {
      try {
        const res = await fetch(`${API_BASE}/api/session/suggestions`);
        if (!res.ok) throw new Error(`Server error ${res.status}`);
        const data = await res.json();
        setExercises(data.exercises || []);
      } catch (err) {
        setError(err.message || 'Failed to load suggestions.');
      } finally {
        setLoading(false);
      }
    }
    fetchSuggestions();
  }, []);

  function handleBeginSession() {
    setExerciseList(exercises);
    setSuggestionData(exercises);
    navigate('/session/live');
  }

  return (
    <>
      <Navbar />
      <PageWrapper title="Your Personalized Exercise Plan">
        {loading && <div className="centered"><Spinner /></div>}
        {error && <p className="form-error">{error}</p>}
        {!loading && !error && (
          <>
            <div className="suggestion-grid">
              {exercises.map((ex, i) => (
                <ExerciseCard key={i} exercise={ex} />
              ))}
            </div>
            <div className="suggestion-cta">
              <Button
                label="Begin Session"
                variant="primary"
                onClick={handleBeginSession}
                disabled={exercises.length === 0}
              />
            </div>
          </>
        )}
      </PageWrapper>
    </>
  );
}
