"""Feedback Agent - Module 3
Core: Load reports → calc recovery rate → LLM predicts date + feedback → save → send to user
"""
import json
from datetime import datetime, timedelta
from utils.logger import get_logger
from utils.helpers import ensure_directory, safe_write_json
from config import config

logger = get_logger(__name__)

class FeedbackAgent:
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        self.predictions_path = config.OUTPUT_PATH / "predictions" / "recovery_predictions"
        self.feedback_path = config.OUTPUT_PATH / "feedback" / "progress_feedback"
        ensure_directory(self.predictions_path)
        ensure_directory(self.feedback_path)

    def generate_feedback(self, user_id, weekly_report, monthly_report=None):
        """Core: Load reports → calc progress rate → LLM predict + feedback → save"""
        # Calculate recovery progress rate
        report = weekly_report.get("report", {})
        imp_pct = 0
        if isinstance(report.get("Improvement"), str):
            imp_pct = float(report["Improvement"].replace("%", ""))
        else:
            imp_pct = report.get("improvement_percentage", 0)
        
        current_score = 70.0  # default estimate
        if monthly_report:
            current_score = monthly_report.get("report", {}).get("overall_improvement_pct", 70.0)
        
        gap = 100 - current_score
        weeks_left = max(1, round(gap / imp_pct)) if imp_pct > 0 else 12
        recovery_date = (datetime.now() + timedelta(weeks=weeks_left)).strftime("%Y-%m-%d")
        
        # LLM prompt
        prompt = f"""Weekly: {json.dumps(weekly_report)}
Monthly: {json.dumps(monthly_report if monthly_report else {{}})}
Progress: {imp_pct}% per week, {gap}% remaining, ETA {weeks_left} weeks

Based on this progress data, predict when user will fully recover.
Generate feedback:
- If progress good (>5%/week): motivating with appreciation + milestone highlights
- If progress slow (<5%/week): encouraging with tips

Return JSON: {{"predicted_recovery_date": "{recovery_date}", "feedback_message": "", 
"feedback_tone": "positive|corrective", "milestones": [], "tips": []}}"""
        
        try:
            feedback = json.loads(self.llm_client.generate(prompt)) if self.llm_client else {}
        except:
            tone = "positive" if imp_pct >= 5 else "corrective"
            if tone == "positive":
                msg = f"Great! {imp_pct}% improvement/week. Full recovery by {recovery_date}"
                miles = [f"Current: {current_score}%", "Strong consistency"]
                tips = []
            else:
                msg = f"Keep going! {gap}% to go. Attend all 7 days for faster results"
                miles = []
                tips = ["Increase consistency", "Focus on weak areas"]
            
            feedback = {
                "predicted_recovery_date": recovery_date,
                "feedback_message": msg,
                "feedback_tone": tone,
                "milestones": miles,
                "tips": tips
            }
        
        # Save prediction
        pred = {"user_id": user_id, "predicted_date": feedback.get("predicted_recovery_date"), 
                "weeks_remaining": weeks_left, "progress_rate": imp_pct}
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_write_json(self.predictions_path / f"{user_id}_pred_{ts}.json", pred)
        
        # Save feedback
        result = {"user_id": user_id, "feedback": feedback}
        safe_write_json(self.feedback_path / f"{user_id}_feedback_{ts}.json", result)
        
        logger.info(f"Feedback: {feedback['feedback_tone']} - ETA {feedback['predicted_recovery_date']}")
        return result
