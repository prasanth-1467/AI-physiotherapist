"""Tracker Agent - Module 2
Core: Daily results → weekly log → Day 7 LLM analysis → suggest next week or repeat/alternative
"""
import json
from datetime import datetime
from utils.logger import get_logger
from utils.helpers import ensure_directory, safe_write_json
from config import config

logger = get_logger(__name__)

class TrackerAgent:
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        self.weekly_path = config.DATA_PATH / "sessions" / "weekly"
        ensure_directory(self.weekly_path)

    def _load_week(self, uid, wk):
        try:
            with open(self.weekly_path / f"{uid}_week{wk}.json") as f:
                return json.load(f)
        except:
            return {"user_id": uid, "week": wk, "days": []}

    def process_daily(self, result, week=1):
        uid = result.get("user_id", "unknown")
        log = self._load_week(uid, week)
        log["days"].append(result)
        safe_write_json(self.weekly_path / f"{uid}_week{week}.json", log)
        
        if len(log["days"]) >= 7:
            # Day 7: Analyze
            prompt = f"""Analyze 7 days: {json.dumps(log['days'])}
Did user improve, stay same, or regress? By what %? Return JSON:
{{"trend": "improving|stable|regressing", "improvement_percent": number, "weak_joints": [], "strong_joints": []}}"""
            
            try:
                analysis = json.loads(self.llm_client.generate(prompt)) if self.llm_client else {}
            except:
                scores = [d.get("average_score", 0) for d in log["days"]]
                delta = scores[-1] - scores[0] if len(scores) > 1 else 0
                analysis = {"trend": "improving" if delta > 5 else "stable", 
                           "improvement_percent": delta, "weak_joints": [], "strong_joints": []}
            
            # Send feedback to suggestion_agent
            imp = analysis.get("improvement_percent", 0)
            weak = analysis.get("weak_joints", [])
            feedback = f"User improved by {imp}%, weak on {weak}. " + (
                "Suggest next week exercises accordingly" if imp > 3 else 
                "Lesser improvement - repeat or suggest alternative exercises")
            analysis["feedback_to_suggester"] = feedback
            
            logger.info(f"Week {week} done: {analysis['trend']}, sending to suggestion_agent")
            return {"week_complete": True, "analysis": analysis, "week": week, "user_id": uid}
        
        logger.info(f"Day {len(log['days'])}/7 logged")
        return {"week_complete": False, "days_logged": len(log['days']), "week": week, "user_id": uid}
