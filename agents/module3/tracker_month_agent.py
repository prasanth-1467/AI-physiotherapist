"""Tracker Month Agent - Module 3
Compares Day 1 baseline vs Day 30 performance, generates monthly progress report.
"""
import json
from datetime import datetime
from utils.logger import get_logger
from utils.helpers import ensure_directory, safe_write_json, timestamp
from config import config

logger = get_logger(__name__)

class TrackerMonthAgent:
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        self.history_path = config.DATA_PATH / "user_profiles" / "rehab_history"
        self.weekly_path = config.DATA_PATH / "sessions" / "weekly"
        self.reports_path = config.OUTPUT_PATH / "reports" / "monthly_reports"
        ensure_directory(self.reports_path)

    def _load_baseline(self, user_id):
        path = self.history_path / f"{user_id}_history.json"
        try:
            with open(path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"No baseline for {user_id}")
            return {}

    def _load_weekly_summaries(self, user_id, weeks=4):
        summaries = []
        for w in range(1, weeks + 1):
            path = self.weekly_path / f"{user_id}_week{w}.json"
            try:
                with open(path, "r") as f:
                    summaries.append(json.load(f))
            except FileNotFoundError:
                continue
        return summaries

    def _compare(self, baseline, current_result, weekly_data):
        b_scores = {j["joint"]: j.get("deviation", 0) for j in baseline.get("affected_joints", [])}
        c_scores = {}
        for r in current_result.get("results", []):
            c_scores[r.get("target_joint", "unknown")] = r.get("performance_score", 0)
        joint_progress = {}
        for joint in set(list(b_scores.keys()) + list(c_scores.keys())):
            joint_progress[joint] = {"baseline_deviation": b_scores.get(joint, 0),
                                     "current_score": c_scores.get(joint, 0)}
        week_scores = []
        for w in weekly_data:
            days = w.get("days", [])
            avgs = [d.get("average_score", 0) for d in days if "average_score" in d]
            week_scores.append(round(sum(avgs) / len(avgs), 1) if avgs else 0)
        overall_imp = round(week_scores[-1] - week_scores[0], 1) if len(week_scores) > 1 else 0
        attended = sum(len(w.get("days", [])) for w in weekly_data)
        return {
            "joint_progress": joint_progress, "weekly_scores": week_scores,
            "overall_improvement": overall_imp,
            "consistency": {"days_attended": attended, "total_days": 30},
            "current_avg": current_result.get("average_score", 0)
        }

    def generate_monthly_report(self, user_id, current_result, month_number=1):
        baseline = self._load_baseline(user_id)
        weekly_data = self._load_weekly_summaries(user_id)
        comparison = self._compare(baseline, current_result, weekly_data)
        prompt = (
            f"Baseline (Day 1): {json.dumps(baseline)}\n"
            f"Current (Day 30): {json.dumps(current_result)}\n"
            f"Comparison: {json.dumps(comparison)}\n"
            "Generate a monthly progress report as JSON: summary, joint_by_joint_improvement, "
            "overall_improvement_pct, consistency, highlights, concerns, next_month_plan. JSON only."
        )
        try:
            raw = self.llm_client.generate(prompt) if self.llm_client else None
            report = json.loads(raw) if raw else {"summary": f"Month {month_number} complete.",
                                                   **comparison}
        except Exception as e:
            logger.error(f"LLM monthly report error: {e}")
            report = {"summary": f"Month {month_number} complete.", **comparison}
        result = {
            "user_id": user_id, "month_number": month_number,
            "report_date": datetime.now().strftime("%Y-%m-%d"),
            "report": report, "status": "success"
        }
        safe_write_json(self.reports_path / f"{user_id}_month{month_number}_report_{timestamp()}.json", result)
        logger.info(f"Monthly report generated for {user_id} month {month_number}")
        return result