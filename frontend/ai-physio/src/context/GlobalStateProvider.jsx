import { createContext, useContext, useState, useEffect } from 'react';

const GlobalStateContext = createContext(null);

const LS_KEY = 'ai_physio_user';
const SESSION_LOG_KEY = 'ai_physio_session_log';

export function GlobalStateProvider({ children }) {
  const [name, setName] = useState('');
  const [injuryType, setInjuryType] = useState('');
  const [bodyPart, setBodyPart] = useState('');
  const [rehabGoal, setRehabGoal] = useState('');
  const [exerciseList, setExerciseList] = useState([]);
  const [currentExerciseIndex, setCurrentExerciseIndex] = useState(0);
  const [sessionResults, setSessionResults] = useState([]);
  const [suggestionData, setSuggestionData] = useState(null);

  // Load persisted user profile on mount
  useEffect(() => {
    try {
      const stored = localStorage.getItem(LS_KEY);
      if (stored) {
        const parsed = JSON.parse(stored);
        if (parsed.name) setName(parsed.name);
        if (parsed.injuryType) setInjuryType(parsed.injuryType);
        if (parsed.bodyPart) setBodyPart(parsed.bodyPart);
        if (parsed.rehabGoal) setRehabGoal(parsed.rehabGoal);
      }
    } catch (_) {}
  }, []);

  function saveUserProfile(profile) {
    setName(profile.name);
    setInjuryType(profile.injuryType);
    setBodyPart(profile.bodyPart);
    setRehabGoal(profile.rehabGoal);
    localStorage.setItem(LS_KEY, JSON.stringify(profile));
  }

  function clearUserProfile() {
    setName('');
    setInjuryType('');
    setBodyPart('');
    setRehabGoal('');
    localStorage.removeItem(LS_KEY);
  }

  function logSession(score) {
    try {
      const today = new Date().toISOString().split('T')[0];
      const log = JSON.parse(localStorage.getItem(SESSION_LOG_KEY) || '[]');
      // Only log once per day
      if (!log.find(e => e.date === today)) {
        log.push({ date: today, score });
        localStorage.setItem(SESSION_LOG_KEY, JSON.stringify(log));
      }
    } catch (_) {}
  }

  function getSessionLog() {
    try {
      return JSON.parse(localStorage.getItem(SESSION_LOG_KEY) || '[]');
    } catch (_) {
      return [];
    }
  }

  const value = {
    name, injuryType, bodyPart, rehabGoal,
    saveUserProfile, clearUserProfile,
    exerciseList, setExerciseList,
    currentExerciseIndex, setCurrentExerciseIndex,
    sessionResults, setSessionResults,
    suggestionData, setSuggestionData,
    logSession, getSessionLog,
  };

  return (
    <GlobalStateContext.Provider value={value}>
      {children}
    </GlobalStateContext.Provider>
  );
}

export function useGlobalState() {
  const ctx = useContext(GlobalStateContext);
  if (!ctx) throw new Error('useGlobalState must be used inside GlobalStateProvider');
  return ctx;
}
