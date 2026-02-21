import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useGlobalState } from '../context/GlobalStateProvider';
import Button from '../components/ui/Button';
import PageWrapper from '../components/layout/PageWrapper';

const INJURY_TYPES = ['Fracture', 'Sprain', 'Strain', 'Post-surgery', 'Arthritis', 'Tendinitis', 'Other'];
const BODY_PARTS = ['Shoulder', 'Elbow', 'Wrist', 'Hip', 'Knee', 'Ankle', 'Spine', 'Neck', 'Other'];

export default function StartPage() {
  const navigate = useNavigate();
  const { saveUserProfile } = useGlobalState();

  const [form, setForm] = useState({ name: '', injuryType: '', bodyPart: '', rehabGoal: '' });
  const [errors, setErrors] = useState({});

  // Skip to dashboard if already set up
  useEffect(() => {
    try {
      const stored = localStorage.getItem('ai_physio_user');
      if (stored) {
        const parsed = JSON.parse(stored);
        if (parsed.name && parsed.injuryType) {
          navigate('/dashboard', { replace: true });
        }
      }
    } catch (_) {}
  }, [navigate]);

  function validate() {
    const e = {};
    if (!form.name.trim()) e.name = 'Name is required.';
    if (!form.injuryType) e.injuryType = 'Please select an injury type.';
    if (!form.bodyPart) e.bodyPart = 'Please select a body part.';
    if (!form.rehabGoal.trim()) e.rehabGoal = 'Please describe your rehab goal.';
    return e;
  }

  function handleSubmit(e) {
    e.preventDefault();
    const errs = validate();
    if (Object.keys(errs).length) { setErrors(errs); return; }
    saveUserProfile(form);
    navigate('/dashboard');
  }

  function handleChange(field, value) {
    setForm(f => ({ ...f, [field]: value }));
    setErrors(e => ({ ...e, [field]: undefined }));
  }

  return (
    <PageWrapper title="Tell us about yourself">
      <div className="start-form-wrapper">
        <form className="start-form" onSubmit={handleSubmit} noValidate>

          <div className="form-field">
            <label className="form-label">Your name</label>
            <input
              className={`form-input ${errors.name ? 'input-error' : ''}`}
              type="text"
              placeholder="e.g. Sarah"
              value={form.name}
              onChange={e => handleChange('name', e.target.value)}
            />
            {errors.name && <span className="form-error">{errors.name}</span>}
          </div>

          <div className="form-field">
            <label className="form-label">Injury type</label>
            <select
              className={`form-select ${errors.injuryType ? 'input-error' : ''}`}
              value={form.injuryType}
              onChange={e => handleChange('injuryType', e.target.value)}
            >
              <option value="">Select injury type</option>
              {INJURY_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
            </select>
            {errors.injuryType && <span className="form-error">{errors.injuryType}</span>}
          </div>

          <div className="form-field">
            <label className="form-label">Affected body part</label>
            <select
              className={`form-select ${errors.bodyPart ? 'input-error' : ''}`}
              value={form.bodyPart}
              onChange={e => handleChange('bodyPart', e.target.value)}
            >
              <option value="">Select body part</option>
              {BODY_PARTS.map(p => <option key={p} value={p}>{p}</option>)}
            </select>
            {errors.bodyPart && <span className="form-error">{errors.bodyPart}</span>}
          </div>

          <div className="form-field">
            <label className="form-label">Rehab goal</label>
            <textarea
              className={`form-textarea ${errors.rehabGoal ? 'input-error' : ''}`}
              placeholder="e.g. Regain full range of motion in my knee after surgery"
              rows={3}
              value={form.rehabGoal}
              onChange={e => handleChange('rehabGoal', e.target.value)}
            />
            {errors.rehabGoal && <span className="form-error">{errors.rehabGoal}</span>}
          </div>

          <Button type="submit" label="Continue to Dashboard" variant="primary" />
        </form>
      </div>
    </PageWrapper>
  );
}
