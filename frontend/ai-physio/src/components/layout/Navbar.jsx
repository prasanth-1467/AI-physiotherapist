import { NavLink, useNavigate } from 'react-router-dom';
import { useGlobalState } from '../../context/GlobalStateProvider';

export default function Navbar() {
  const { name } = useGlobalState();
  const navigate = useNavigate();

  return (
    <nav className="navbar">
      <div className="navbar-inner">
        <button className="navbar-logo" onClick={() => navigate('/dashboard')}>
          AI Physio
        </button>

        <div className="navbar-links">
          <NavLink to="/dashboard" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            Dashboard
          </NavLink>

          <div className="nav-dropdown">
            <span className="nav-link">Progress ▾</span>
            <div className="nav-dropdown-menu">
              <NavLink to="/progress/weekly" className="dropdown-item">Weekly</NavLink>
              <NavLink to="/progress/monthly" className="dropdown-item">Monthly</NavLink>
            </div>
          </div>

          <NavLink to="/feedback" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            Feedback
          </NavLink>
        </div>

        {name && <span className="navbar-user">{name}</span>}
      </div>
    </nav>
  );
}
