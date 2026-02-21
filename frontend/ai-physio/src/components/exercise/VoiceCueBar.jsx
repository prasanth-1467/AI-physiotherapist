import { useEffect, useState } from 'react';

export default function VoiceCueBar({ message }) {
  const [visible, setVisible] = useState(false);
  const [displayed, setDisplayed] = useState('');

  useEffect(() => {
    if (!message) return;
    setDisplayed(message);
    setVisible(true);
    const timer = setTimeout(() => setVisible(false), 4000);
    return () => clearTimeout(timer);
  }, [message]);

  return (
    <div className={`voice-cue-bar ${visible ? 'voice-cue-visible' : 'voice-cue-hidden'}`}>
      <span className="voice-cue-icon">🎙</span>
      <span className="voice-cue-text">{displayed}</span>
    </div>
  );
}
