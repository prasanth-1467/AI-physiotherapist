export default function ScoreCircle({ score = 0, size = 120 }) {
  const radius = 45;
  const circumference = 2 * Math.PI * radius;
  const clamped = Math.min(100, Math.max(0, score));
  const offset = circumference - (clamped / 100) * circumference;

  const color = clamped >= 80 ? '#4caf50' : clamped >= 50 ? '#ffc107' : '#f44336';

  return (
    <div className="score-circle" style={{ width: size, height: size }}>
      <svg viewBox="0 0 100 100" width={size} height={size}>
        <circle cx="50" cy="50" r={radius} fill="none" stroke="#e0e0e0" strokeWidth="8" />
        <circle
          cx="50" cy="50" r={radius}
          fill="none"
          stroke={color}
          strokeWidth="8"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          transform="rotate(-90 50 50)"
          style={{ transition: 'stroke-dashoffset 0.6s ease' }}
        />
        <text x="50" y="54" textAnchor="middle" fontSize="18" fontWeight="bold" fill={color}>
          {clamped}
        </text>
      </svg>
    </div>
  );
}
