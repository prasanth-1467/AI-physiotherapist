"""Tracker Week Agent - Module 3
Receives weekly summary from Module 2, generates structured weekly progress report.
"""
import json
from datetime import datetime
from utils.logger import get_logger
from utils.helpers import ensure_directory, safe_write_json, timestamp
from config import config

logger = get_logger(__name__)

class TrackerWeekAgent:
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        self.weekly_path = config.DATA_PATH / "sessions" / "weekly"
        self.reports_path = config.OUTPUT_PATH / "reports" / "weekly_reports"
        ensure_directory(self.reports_path)

    def _load_week_sessions(self, user_id, week):
        path = self.weekly_path / f"{user_id}_week{week}.json"
        try:
            with open(path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"No session data for {user_id} week {week}")
            return {"days": []}

    def _build_prompt(self, sessions, analysis):
        return (
            f"Weekly session data:\n{json.dumps(sessions['days'])}\n"
            f"Weekly analysis:\n{json.dumps(analysis)}\n"
            "Generate a structured weekly progress report as JSON with keys: "
            "summary, exercise_breakdown (list), improvement_percentage, "
            "consistency (days_attended out of 7), problem_areas (list), "
            "strengths (list), recommendations (list). Return JSON only."
        )

    def _generate_report_fallback(self, sessions, analysis):
        days = sessions.get("days", [])
        scores = [d.get("average_score", 0) for d in days]
        exercises = {}
        for d in days:
            for r in d.get("results", []):
                name = r.get("exercise_name", r.get("target_joint", "unknown"))
                exercises.setdefault(name, []).append(r.get("performance_score", 0))
        breakdown = [{"exercise": k, "avg_score": round(sum(v)/len(v), 1), "sessions": len(v)}
                     for k, v in exercises.items()]
        avg = round(sum(scores)/len(scores), 1) if scores else 0
        delta = round(scores[-1] - scores[0], 1) if len(scores) > 1 else 0
        weak = analysis.get("weak_joints", [])
        strong = analysis.get("strong_joints", [])
        return {
            "summary": f"Week completed with {len(days)}/7 days. Avg score: {avg}. Trend: {analysis.get('trend', 'stable')}.",
            "exercise_breakdown": breakdown,
            "improvement_percentage": delta,
            "consistency": {"days_attended": len(days), "total_days": 7},
            "problem_areas": weak or ["None identified"],
            "strengths": strong or ["Consistent attendance"],
            "recommendations": analysis.get("recommendations", ["Continue current routine"])
        }

    def generate_weekly_report(self, user_id, week_number, analysis):
        sessions = self._load_week_sessions(user_id, week_number)
        prompt = self._build_prompt(sessions, analysis)
        try:
            raw = self.llm_client.generate(prompt) if self.llm_client else None
            report = json.loads(raw) if raw else self._generate_report_fallback(sessions, analysis)
        except Exception as e:
            logger.error(f"LLM report error: {e}")
            report = self._generate_report_fallback(sessions, analysis)
        result = {
            "user_id": user_id, "week_number": week_number,
            "report_date": datetime.now().strftime("%Y-%m-%d"),
            "report": report, "status": "success"
        }
        safe_write_json(self.reports_path / f"{user_id}_week{week_number}_report_{timestamp()}.json", result)
        logger.info(f"Weekly report generated for {user_id} week {week_number}")
        return result