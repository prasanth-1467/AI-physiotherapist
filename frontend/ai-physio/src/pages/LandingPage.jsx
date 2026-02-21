import { useNavigate } from 'react-router-dom';
import Button from '../components/ui/Button';

const FEATURES = [
  { icon: '🎯', title: 'AI-Powered Pose Analysis', desc: 'Real-time keypoint detection and angle measurement during every exercise.' },
  { icon: '📋', title: 'Personalized Plans', desc: 'Exercise suggestions tailored to your injury, body part, and rehab goal.' },
  { icon: '📊', title: 'Progress Tracking', desc: 'Weekly and monthly reports with joint-level performance insights.' },
  { icon: '🔊', title: 'Voice Feedback', desc: 'Live audio cues guide you through every rep in real time.' },
];

export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="landing">
      {/* Hero */}
      <section className="landing-hero">
        <div className="landing-hero-inner">
          <h1 className="landing-title">AI Physiotherapist</h1>
          <p className="landing-tagline">
            Intelligent rehabilitation — guided by AI, driven by your progress.
          </p>
          <Button label="Get Started" variant="primary" onClick={() => navigate('/start')} />
        </div>
      </section>

      {/* Features */}
      <section className="landing-features">
        <h2 className="landing-features-heading">What we offer</h2>
        <div className="landing-features-grid">
          {FEATURES.map((f, i) => (
            <div key={i} className="landing-feature-card">
              <span className="feature-icon">{f.icon}</span>
              <h3 className="feature-title">{f.title}</h3>
              <p className="feature-desc">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <p>© 2026 AI Physiotherapist. All rights reserved.</p>
      </footer>
    </div>
  );
}
