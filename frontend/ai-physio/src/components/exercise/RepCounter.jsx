import { useEffect, useRef } from 'react';

export default function RepCounter({ currentRep = 0, totalReps = 0, currentSet = 0, totalSets = 0 }) {
  const prevRep = useRef(currentRep);
  const counterRef = useRef(null);

  useEffect(() => {
    if (currentRep !== prevRep.current && counterRef.current) {
      counterRef.current.classList.remove('rep-pop');
      // force reflow
      void counterRef.current.offsetWidth;
      counterRef.current.classList.add('rep-pop');
      prevRep.current = currentRep;
    }
  }, [currentRep]);

  return (
    <div className="rep-counter">
      <div className="rep-counter-reps" ref={counterRef}>
        <span className="rep-current">{currentRep}</span>
        <span className="rep-sep">/</span>
        <span className="rep-total">{totalReps}</span>
        <span className="rep-unit">reps</span>
      </div>
      <div className="rep-counter-sets">
        Set <strong>{currentSet}</strong> / {totalSets}
      </div>
    </div>
  );
}
