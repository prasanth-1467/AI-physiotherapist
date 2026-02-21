export default function ProgressBar({ percentage = 0, color = '#4caf50', label = '' }) {
  const clamped = Math.min(100, Math.max(0, percentage));
  return (
    <div className="progress-bar-wrapper">
      {label && <span className="progress-bar-label">{label}</span>}
      <div className="progress-bar-track">
        <div
          className="progress-bar-fill"
          style={{ width: `${clamped}%`, backgroundColor: color }}
        />
      </div>
      <span className="progress-bar-pct">{clamped}%</span>
    </div>
  );
}
