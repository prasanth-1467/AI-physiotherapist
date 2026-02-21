import { useEffect } from 'react';

export default function Toast({ message, type = 'success', onDismiss }) {
  useEffect(() => {
    const timer = setTimeout(() => onDismiss?.(), 3000);
    return () => clearTimeout(timer);
  }, [onDismiss]);

  return (
    <div className={`toast toast-${type}`}>
      <span>{message}</span>
      <button className="toast-close" onClick={onDismiss}>✕</button>
    </div>
  );
}
