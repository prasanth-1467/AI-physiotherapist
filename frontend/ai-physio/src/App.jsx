import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { GlobalStateProvider } from './context/GlobalStateProvider';
import LandingPage from './pages/LandingPage';
import StartPage from './pages/StartPage';
import DashboardPage from './pages/DashboardPage';
import ReportUploadPage from './pages/ReportUploadPage';
import SummaryConfirmPage from './pages/SummaryConfirmPage';
import SuggestionPage from './pages/SuggestionPage';
import LiveExercisePage from './pages/LiveExercisePage';
import WeeklyReportPage from './pages/WeeklyReportPage';
import MonthlyReportPage from './pages/MonthlyReportPage';
import FeedbackPage from './pages/FeedbackPage';

export default function App() {
  return (
    <GlobalStateProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/start" element={<StartPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/report/upload" element={<ReportUploadPage />} />
          <Route path="/session/summary" element={<SummaryConfirmPage />} />
          <Route path="/session/suggestions" element={<SuggestionPage />} />
          <Route path="/session/live" element={<LiveExercisePage />} />
          <Route path="/progress/weekly" element={<WeeklyReportPage />} />
          <Route path="/progress/monthly" element={<MonthlyReportPage />} />
          <Route path="/feedback" element={<FeedbackPage />} />
          {/* Catch-all */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </GlobalStateProvider>
  );
}
