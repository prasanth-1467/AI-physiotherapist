export default function RecoveryPredictionCard({ predictedDate, daysRemaining, confidence }) {
  const confidenceLabel =
    confidence >= 0.8 ? 'High' : confidence >= 0.5 ? 'Moderate' : 'Low';
  const confidenceClass =
    confidence >= 0.8 ? 'conf-high' : confidence >= 0.5 ? 'conf-moderate' : 'conf-low';

  return (
    <div className="recovery-card">
      <h3 className="recovery-card-title">Recovery Prediction</h3>
      <div className="recovery-card-body">
        <div className="recovery-stat">
          <span className="recovery-stat-label">Predicted Date</span>
          <span className="recovery-stat-value">{predictedDate || '—'}</span>
        </div>
        <div className="recovery-stat">
          <span className="recovery-stat-label">Days Remaining</span>
          <span className="recovery-stat-value recovery-days">{daysRemaining ?? '—'}</span>
        </div>
        <div className="recovery-stat">
          <span className="recovery-stat-label">Confidence</span>
          <span className={`recovery-confidence ${confidenceClass}`}>{confidenceLabel}</span>
        </div>
      </div>
    </div>
  );
}
