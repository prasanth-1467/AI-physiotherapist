import { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Navbar from '../components/layout/Navbar';
import PageWrapper from '../components/layout/PageWrapper';
import Button from '../components/ui/Button';
import Spinner from '../components/ui/Spinner';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function SummaryConfirmPage() {
  const navigate = useNavigate();
  const { state } = useLocation();
  const findings = state?.findings || {};

  const {
    injuryType = '',
    bodyPart = '',
    severity = '',
    doctorNotes = '',
    source = '',
    options = [],
  } = findings;

  const [selectedOption, setSelectedOption] = useState(options[0] || null);
  const [confirmed, setConfirmed] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  async function handleConfirm() {
    setLoading(true);
    setErrorMsg('');
    try {
      const res = await fetch(`${API_BASE}/api/summary/confirm`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...findings, selectedOption }),
      });
      if (!res.ok) throw new Error(`Server error ${res.status}`);
      navigate('/session/suggestions');
    } catch (err) {
      setErrorMsg(err.message || 'Failed to confirm. Please retry.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <Navbar />
      <PageWrapper title="Confirm AI Findings">
        <div className="summary-wrapper">

          <div className="summary-findings">
            <div className="summary-row"><span className="summary-key">Injury type</span><span className="summary-val">{injuryType || '—'}</span></div>
            <div className="summary-row"><span className="summary-key">Body part</span><span className="summary-val">{bodyPart || '—'}</span></div>
            <div className="summary-row"><span className="summary-key">Severity</span><span className="summary-val">{severity || '—'}</span></div>
            {source && <div className="summary-row"><span className="summary-key">Source</span><span className="summary-val source-label">{source}</span></div>}
            {doctorNotes && (
              <div className="summary-notes">
                <span className="summary-key">Doctor notes</span>
                <p className="summary-notes-text">{doctorNotes}</p>
              </div>
            )}
          </div>

          {/* Confirmation options */}
          {options.length > 0 && (
            <div className="summary-options">
              <p className="options-label">Please confirm your condition:</p>
              <div className="options-buttons">
                {options.map((opt, i) => (
                  <button
                    key={i}
                    className={`option-btn ${selectedOption === opt ? 'option-selected' : ''}`}
                    onClick={() => { setSelectedOption(opt); setConfirmed(false); }}
                  >
                    {opt}
                  </button>
                ))}
              </div>
              {selectedOption && selectedOption !== options[0] && !confirmed && (
                <p className="options-reconfirm-hint">You selected a different option. Click Confirm to proceed.</p>
              )}
            </div>
          )}

          {errorMsg && <p className="form-error">{errorMsg}</p>}

          {loading ? (
            <div className="confirm-loading"><Spinner /><p>Processing…</p></div>
          ) : (
            <Button
              label="Confirm & Generate Plan"
              variant="primary"
              onClick={handleConfirm}
              disabled={!selectedOption}
            />
          )}
        </div>
      </PageWrapper>
    </>
  );
}
