"""Tracker Agent - Module 2
Accumulates daily results into weekly logs and analyzes progress trends.
"""
import json
from datetime import datetime
from utils.logger import get_logger
from utils.helpers import ensure_directory, safe_write_json, timestamp
from config import config

logger = get_logger(__name__)
DAYS_PER_WEEK = 7

class TrackerAgent:
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        self.weekly_path = config.DATA_PATH / "sessions" / "weekly"
        self.summary_path = config.OUTPUT_PATH / "tracker"
        ensure_directory(self.weekly_path)
        ensure_directory(self.summary_path)

    def _load_weekly_log(self, user_id, week):
        path = self.weekly_path / f"{user_id}_week{week}.json"
        try:
            with open(path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"user_id": user_id, "week_number": week, "days": []}

    def _save_weekly_log(self, user_id, week, log):
        safe_write_json(self.weekly_path / f"{user_id}_week{week}.json", log)

    def _analyze_with_llm(self, log):
        prompt = (f"Analyze this 7-day rehab performance data:\n{json.dumps(log['days'])}\n"
                  "Return JSON: trend (improving/stable/regressing), improvement_delta, "
                  "weak_joints, strong_joints, recommendations (list of strings), overall_assessment.")
        if self.llm_client:
            try:
                return json.loads(self.llm_client.generate(prompt))
            except Exception as e:
                logger.error(f"LLM analysis error: {e}")
        return self._analyze_fallback(log)

    def _analyze_fallback(self, log):
        scores = [d["average_score"] for d in log["days"] if "average_score" in d]
        avg = sum(scores) / len(scores) if scores else 0
        delta = scores[-1] - scores[0] if len(scores) > 1 else 0
        trend = "improving" if delta > 5 else "regressing" if delta < -5 else "stable"
        joints = {}
        for d in log["days"]:
            for r in d.get("results", []):
                j = r.get("target_joint", "unknown")
                joints.setdefault(j, []).append(r.get("performance_score", 0))
        joint_avgs = {j: sum(s) / len(s) for j, s in joints.items()}
        weak = [j for j, a in joint_avgs.items() if a < 70]
        strong = [j for j, a in joint_avgs.items() if a >= 80]
        return {"trend": trend, "improvement_delta": round(delta, 1), "weak_joints": weak,
                "strong_joints": strong, "daily_scores": scores, "overall_week_score": round(avg, 1),
                "recommendations": [f"Focus on {j}" for j in weak] or ["Maintain current routine"],
                "overall_assessment": f"Week completed with {trend} trend."}

    def process_daily_result(self, daily_result, week_number=1):
        user_id = daily_result["user_id"]
        log = self._load_weekly_log(user_id, week_number)
        log["days"].append(daily_result)
        self._save_weekly_log(user_id, week_number, log)
        completed = len(log["days"]) >= DAYS_PER_WEEK
        analysis = self._analyze_with_llm(log) if completed else None
        result = {"user_id": user_id, "week_number": week_number,
                  "week_completed": completed, "days_logged": len(log["days"]),
                  "analysis": analysis, "status": "success"}
        if completed:
            safe_write_json(self.summary_path / f"{user_id}_week{week_number}_summary_{timestamp()}.json", result)
            logger.info(f"Week {week_number} complete for {user_id}: {analysis.get('trend')}")
        else:
            logger.info(f"Day {len(log['days'])}/{DAYS_PER_WEEK} logged for {user_id} week {week_number}")
        return result