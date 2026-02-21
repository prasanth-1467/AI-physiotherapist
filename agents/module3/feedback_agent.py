"""Feedback Agent - Module 3
Predicts recovery timeline and generates motivational/corrective feedback.
"""
import json
from datetime import datetime, timedelta
from utils.logger import get_logger
from utils.helpers import ensure_directory, safe_write_json, timestamp
from config import config

logger = get_logger(__name__)

class FeedbackAgent:
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        self.predictions_path = config.OUTPUT_PATH / "predictions" / "recovery_predictions"
        self.feedback_path = config.OUTPUT_PATH / "feedback" / "progress_feedback"
        ensure_directory(self.predictions_path)
        ensure_directory(self.feedback_path)

    def _calc_recovery_estimate(self, weekly_report, monthly_report=None):
        report = weekly_report.get("report", {})
        imp = report.get("improvement_percentage", 0)
        avg = float(report.get("consistency", {}).get("days_attended", 7)) / 7
        weekly_rate = imp * avg if imp > 0 else 1.0
        current_score = 0
        for ex in report.get("exercise_breakdown", []):
            current_score = max(current_score, ex.get("avg_score", 0))
        if monthly_report:
            mr = monthly_report.get("report", {})
            current_score = max(current_score, mr.get("current_avg", current_score))
        gap = 100 - current_score
        weeks_left = max(1, round(gap / weekly_rate)) if weekly_rate > 0 else 12
        est_date = datetime.now() + timedelta(weeks=weeks_left)
        tone = "positive" if imp >= 5 else "corrective"
        return {"current_score": current_score, "weekly_rate": round(weekly_rate, 1),
                "gap_to_full": round(gap, 1), "weeks_remaining": weeks_left,
                "predicted_recovery_date": est_date.strftime("%Y-%m-%d"), "tone": tone}

    def generate_feedback(self, user_id, weekly_report, monthly_report=None):
        estimate = self._calc_recovery_estimate(weekly_report, monthly_report)
        prompt = (
            f"Recovery estimate: {json.dumps(estimate)}\n"
            f"Weekly report: {json.dumps(weekly_report.get('report', {}))}\n"
            f"Tone: {estimate['tone']}\n"
            "Return JSON: predicted_recovery_date, feedback_message, feedback_tone, "
            "milestones (list), tips (list). If positive: appreciation + milestone highlights. "
            "If corrective: improvement tips + encouragement. JSON only."
        )
        try:
            raw = self.llm_client.generate(prompt) if self.llm_client else None
            feedback = json.loads(raw) if raw else self._fallback(estimate)
        except Exception as e:
            logger.error(f"LLM feedback error: {e}")
            feedback = self._fallback(estimate)
        safe_write_json(self.predictions_path / f"{user_id}_prediction_{timestamp()}.json",
                        {"user_id": user_id, **estimate})
        result = {"user_id": user_id, "feedback": feedback, "estimate": estimate, "status": "success"}
        safe_write_json(self.feedback_path / f"{user_id}_feedback_{timestamp()}.json", result)
        logger.info(f"Feedback for {user_id}: {feedback.get('feedback_tone')} - ETA {estimate['predicted_recovery_date']}")
        return result

    def _fallback(self, est):
        if est["tone"] == "positive":
            msg = f"Great progress! You're improving {est['weekly_rate']}% per week. Estimated full recovery by {est['predicted_recovery_date']}."
        else:
            msg = f"Keep going! You have {est['gap_to_full']}% to go. Try to attend all 7 days next week for faster results."
        return {"predicted_recovery_date": est["predicted_recovery_date"], "feedback_message": msg,
                "feedback_tone": est["tone"],
                "milestones": [f"Current score: {est['current_score']}%"] if est["tone"] == "positive" else [],
                "tips": ["Increase session consistency", "Focus on weak joints"] if est["tone"] == "corrective" else []}