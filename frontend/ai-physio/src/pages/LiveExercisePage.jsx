import { useState, useRef, useCallback, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useGlobalState } from '../context/GlobalStateProvider';
import CameraFeed from '../components/stream/CameraFeed';
import WebSocketManager from '../components/stream/WebSocketManager';
import ExerciseOverlay from '../components/exercise/ExerciseOverlay';
import AngleDisplay from '../components/exercise/AngleDisplay';
import RepCounter from '../components/exercise/RepCounter';
import VoiceCueBar from '../components/exercise/VoiceCueBar';
import Gauge from '../components/ui/Gauge';
import Button from '../components/ui/Button';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function LiveExercisePage() {
  const navigate = useNavigate();
  const { exerciseList, currentExerciseIndex, setCurrentExerciseIndex, setSessionResults, logSession } = useGlobalState();

  const cameraRef = useRef(null);
  const canvasRef = useRef(null);
  const videoRef = useRef(null);

  const [keypoints, setKeypoints] = useState([]);
  const [angles, setAngles] = useState([]);
  const [voiceCue, setVoiceCue] = useState('');
  const [repData, setRepData] = useState({ currentRep: 0, totalReps: 0, currentSet: 1, totalSets: 1 });
  const [performanceScore, setPerformanceScore] = useState(0);
  const [paused, setPaused] = useState(false);
  const [wsActive, setWsActive] = useState(true);
  const [sessionComplete, setSessionComplete] = useState(false);
  const [allResults, setAllResults] = useState([]);

  const exercise = exerciseList[currentExerciseIndex] || null;

  // Sync canvas size to video
  useEffect(() => {
    const video = cameraRef.current?.getVideoElement?.();
    if (video && canvasRef.current) {
      canvasRef.current.width = video.videoWidth || 640;
      canvasRef.current.height = video.videoHeight || 480;
    }
  }, [keypoints]);

  const captureFrame = useCallback(() => {
    return cameraRef.current?.captureFrame?.() || null;
  }, []);

  function handleKeypointsReceived(kps) {
    setKeypoints(kps || []);
  }

  function handleAngleReceived(data) {
    if (data.angles) setAngles(data.angles);
    if (data.rep !== undefined) {
      setRepData(r => ({ ...r, currentRep: data.rep, totalReps: data.totalReps || r.totalReps }));
    }
    if (data.score !== undefined) setPerformanceScore(data.score);
  }

  function handleVoiceCue(text) {
    setVoiceCue(text);
  }

  async function handleEndExercise() {
    setWsActive(false);
    // Notify backend
    try {
      await fetch(`${API_BASE}/api/exercise/stop`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ exerciseName: exercise?.name, score: performanceScore }),
      });
    } catch (_) {}

    const result = { name: exercise?.name || '', score: performanceScore };
    const updatedResults = [...allResults, result];
    setAllResults(updatedResults);

    const nextIndex = currentExerciseIndex + 1;
    if (nextIndex >= exerciseList.length) {
      // All done
      const totalScore = Math.round(updatedResults.reduce((s, r) => s + r.score, 0) / updatedResults.length);
      setSessionResults(updatedResults);
      logSession(totalScore);
      setSessionComplete(true);
    } else {
      setCurrentExerciseIndex(nextIndex);
      setKeypoints([]);
      setAngles([]);
      setRepData({ currentRep: 0, totalReps: exerciseList[nextIndex]?.reps || 0, currentSet: 1, totalSets: exerciseList[nextIndex]?.sets || 1 });
      setPerformanceScore(0);
      setWsActive(true);
    }
  }

  function handleTogglePause() {
    setPaused(p => !p);
    setWsActive(p => !p);
  }

  const totalScore = allResults.length
    ? Math.round(allResults.reduce((s, r) => s + r.score, 0) / allResults.length)
    : 0;

  const mainAngle = angles[0] || null;

  return (
    <div className="live-exercise-page">
      <WebSocketManager
        captureFrame={captureFrame}
        onKeypointsReceived={handleKeypointsReceived}
        onAngleReceived={handleAngleReceived}
        onVoiceCueReceived={handleVoiceCue}
        active={wsActive && !paused && !sessionComplete}
      />

      {/* Session complete overlay */}
      {sessionComplete && (
        <div className="session-complete-overlay">
          <div className="session-complete-box">
            <h2>Session Complete! 🎉</h2>
            <p className="session-total-score">Total Score: <strong>{totalScore}</strong></p>
            <ul className="session-results-list">
              {allResults.map((r, i) => (
                <li key={i}>{r.name}: {r.score}</li>
              ))}
            </ul>
            <Button label="View Weekly Report" variant="primary" onClick={() => navigate('/progress/weekly')} />
          </div>
        </div>
      )}

      <div className="live-layout">
        {/* Camera side */}
        <div className="live-camera-side">
          <div className="live-video-wrapper">
            <CameraFeed ref={cameraRef} />
            <canvas ref={canvasRef} className="live-canvas" />
            <ExerciseOverlay canvasRef={canvasRef} keypoints={keypoints} angles={angles} />
            <AngleDisplay
              angles={angles}
              canvasWidth={canvasRef.current?.width || 640}
              canvasHeight={canvasRef.current?.height || 480}
            />
          </div>
        </div>

        {/* Info side */}
        <div className="live-info-side">
          <h2 className="live-exercise-name">{exercise?.name || 'Exercise'}</h2>

          <RepCounter
            currentRep={repData.currentRep}
            totalReps={repData.totalReps || exercise?.reps || 0}
            currentSet={repData.currentSet}
            totalSets={repData.totalSets || exercise?.sets || 1}
          />

          {mainAngle && (
            <Gauge
              idealMin={mainAngle.idealMin || 60}
              idealMax={mainAngle.idealMax || 120}
              currentAngle={Math.round(mainAngle.value)}
            />
          )}

          <div className="live-performance">
            <span className="perf-label">Performance</span>
            <span className="perf-score">{performanceScore}</span>
          </div>

          <div className="live-exercise-counter">
            Exercise {currentExerciseIndex + 1} / {exerciseList.length}
          </div>

          <div className="live-buttons">
            <Button
              label={paused ? 'Resume' : 'Pause'}
              variant="secondary"
              onClick={handleTogglePause}
            />
            <Button
              label="End Exercise"
              variant="danger"
              onClick={handleEndExercise}
            />
          </div>
        </div>
      </div>

      <VoiceCueBar message={voiceCue} />
    </div>
  );
}
