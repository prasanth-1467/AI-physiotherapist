import Badge from '../ui/Badge';

export default function FeedbackTimeline({ entries = [] }) {
  // entries: [{ week: 1, tone: 'motivating'|'corrective', summary: '...' }]
  return (
    <div className="feedback-timeline">
      {entries.length === 0 && (
        <p className="timeline-empty">No past feedback yet.</p>
      )}
      {entries.map((entry, i) => (
        <div key={i} className="timeline-entry">
          <div className="timeline-line">
            <div className="timeline-dot" />
            {i < entries.length - 1 && <div className="timeline-connector" />}
          </div>
          <div className="timeline-content">
            <div className="timeline-header">
              <span className="timeline-week">Week {entry.week}</span>
              <Badge
                label={entry.tone === 'motivating' ? 'Motivating' : 'Corrective'}
                variant={entry.tone === 'motivating' ? 'improving' : 'regressing'}
              />
            </div>
            <p className="timeline-summary">{entry.summary}</p>
          </div>
        </div>
      ))}
    </div>
  );
}
