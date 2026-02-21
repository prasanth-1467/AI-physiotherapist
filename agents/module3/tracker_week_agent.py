"""Tracker Week Agent - Module 3
Core: Loads 7 days → LLM generates report → formats → saves → sends to feedback_agent
"""
import json
from datetime import datetime
from utils.logger import get_logger
from utils.helpers import ensure_directory, safe_write_json
from config import config

logger = get_logger(__name__)

class TrackerWeekAgent:
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        self.weekly_path = config.DATA_PATH / "sessions" / "weekly"
        self.reports_path = config.OUTPUT_PATH / "reports" / "weekly_reports"
        ensure_directory(self.reports_path)

    def generate_weekly_report(self, user_id, week, analysis):
        """Core: Load 7 days → LLM report → format → save"""
        # Load all 7 days
        try:
            with open(self.weekly_path / f"{user_id}_week{week}.json") as f:
                sessions = json.load(f)
        except:
            sessions = {"days": []}
        
        # LLM prompt
        prompt = f"""Sessions: {json.dumps(sessions['days'])}
Analysis: {json.dumps(analysis)}

Generate structured weekly progress report covering:
- exercises completed
- average performance score
- improvement percentage
- consistency (days attended)
- key problem areas

Return JSON: {{"summary": "", "exercise_breakdown": [], "improvement_percentage": 0, 
"consistency": {{"days_attended": 0}}, "problem_areas": [], "areas_to_work_on": []}}"""
        
        # Get LLM response
        try:
            report = json.loads(self.llm_client.generate(prompt)) if self.llm_client else {}
        except:
            days = sessions.get("days", [])
            scores = [d.get("average_score", 0) for d in days]
            avg = round(sum(scores)/len(scores), 1) if scores else 0
            report = {
                "summary": f"Week {week}: {len(days)}/7 days, avg {avg}%",
                "exercise_breakdown": [],
                "improvement_percentage": round(scores[-1]-scores[0], 1) if len(scores)>1 else 0,
                "consistency": {"days_attended": len(days)},
                "problem_areas": analysis.get("weak_joints", []),
                "areas_to_work_on": analysis.get("weak_joints", [])
            }
        
        # Format with sections
        formatted = {
            "Summary": report.get("summary", ""),
            "Exercise Breakdown": report.get("exercise_breakdown", []),
            "Improvement": f"{report.get('improvement_percentage', 0)}%",
            "Areas to Work On": report.get("areas_to_work_on", [])
        }
        
        # Save to output/reports/weekly_reports
        result = {"user_id": user_id, "week": week, "report": formatted}
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_write_json(self.reports_path / f"week{week}_report_{ts}.json", result)
        logger.info(f"Weekly report saved: week{week}")
        
        return result
