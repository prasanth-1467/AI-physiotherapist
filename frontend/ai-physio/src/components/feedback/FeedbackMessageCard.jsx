export default function FeedbackMessageCard({ message, sentiment = 'motivating' }) {
  // sentiment: 'motivating' → green, 'corrective' → amber
  const isMotivating = sentiment === 'motivating';
  return (
    <div className={`feedback-msg-card ${isMotivating ? 'feedback-green' : 'feedback-amber'}`}>
      <div className="feedback-msg-icon">{isMotivating ? '✅' : '⚠️'}</div>
      <p className="feedback-msg-text">{message}</p>
    </div>
  );
}
