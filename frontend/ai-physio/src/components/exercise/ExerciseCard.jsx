import { useState } from 'react';
import Badge from '../ui/Badge';

export default function ExerciseCard({ exercise }) {
  const [expanded, setExpanded] = useState(false);
  const {
    name = '',
    image = null,
    reps = 0,
    sets = 0,
    difficulty = 'moderate',
    reason = '',
    targetJoints = [],
    angleRanges = [],
  } = exercise || {};

  return (
    <div className="exercise-card">
      {image && <img className="exercise-card-img" src={image} alt={name} />}
      <div className="exercise-card-body">
        <div className="exercise-card-header">
          <h3 className="exercise-card-name">{name}</h3>
          <Badge label={difficulty} variant={difficulty} />
        </div>
        <p className="exercise-card-meta">{sets} sets × {reps} reps</p>
        <p className="exercise-card-reason">{reason}</p>
        <button
          className="exercise-card-expand"
          onClick={() => setExpanded(e => !e)}
        >
          {expanded ? 'Hide details ▲' : 'Show angle info ▼'}
        </button>
        {expanded && (
          <div className="exercise-card-details">
            {targetJoints.length > 0 && (
              <p><strong>Target joints:</strong> {targetJoints.join(', ')}</p>
            )}
            {angleRanges.length > 0 && (
              <ul className="angle-range-list">
                {angleRanges.map((ar, i) => (
                  <li key={i}>{ar.joint}: {ar.min}° – {ar.max}°</li>
                ))}
              </ul>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
