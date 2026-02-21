"""Tracker Month Agent - Module 3
Core: Day 30 trigger → load Day 1 baseline → ask user benchmark → compare → LLM report → save
"""
import json
from datetime import datetime
from utils.logger import get_logger
from utils.helpers import ensure_directory, safe_write_json
from config import config

logger = get_logger(__name__)

class TrackerMonthAgent:
    def __init__(self, llm_client=None, live_stream=None, pose_service=None, angle_service=None):
        self.llm_client = llm_client
        self.stream = live_stream
        self.pose = pose_service
        self.angle = angle_service
        self.history_path = config.DATA_PATH / "user_profiles" / "rehab_history"
        self.reports_path = config.OUTPUT_PATH / "reports" / "monthly_reports"
        ensure_directory(self.reports_path)

    def generate_monthly_report(self, user_id, month=1):
        """Core: Load Day 1 baseline → user performs benchmark → compare → LLM report"""
        # Load Day 1 baseline
        try:
            with open(self.history_path / f"{user_id}_history.json") as f:
                baseline = json.load(f)
        except:
            baseline = {}
        
        # Ask user to perform same benchmark (simulated - would be interactive)
        logger.info("User performing Day 30 benchmark exercises...")
        # In real implementation: record via live_stream + pose + angle services
        # For now, simulate current performance
        current = {"average_score": 75.0, "results": []}
        
        # Compare Day 1 vs Day 30
        b_score = baseline.get("baseline_score", 50.0)
        c_score = current.get("average_score", 75.0)
        improvement = round(c_score - b_score, 1)
        
        # Calculate joint-by-joint
        joints = {}
        for j in baseline.get("affected_joints", []):
            jname = j.get("joint", "unknown")
            joints[jname] = {"day1_deviation": j.get("deviation", 0), "day30_score": 75.0}
        
        # Consistency across 4 weeks
        attended = 0
        for w in range(1, 5):
            try:
                with open(config.DATA_PATH / "sessions" / "weekly" / f"{user_id}_week{w}.json") as f:
                    wk = json.load(f)
                    attended += len(wk.get("days", []))
            except:
                pass
        
        # LLM prompt
        prompt = f"""Day 1 baseline: {json.dumps(baseline)}
Day 30 current: {json.dumps(current)}
Improvement: {improvement}%
Joint progress: {json.dumps(joints)}
Consistency: {attended}/30 days

Generate comprehensive monthly progress report comparing Day 1 vs Day 30 performance.
Return JSON: {{"summary": "", "joint_by_joint_improvement": {{}}, "overall_improvement_pct": 0, 
"consistency": {{}}, "highlights": [], "concerns": []}}"""
        
        try:
            report = json.loads(self.llm_client.generate(prompt)) if self.llm_client else {}
        except:
            report = {
                "summary": f"Month {month}: {improvement}% improvement, {attended}/30 days",
                "joint_by_joint_improvement": joints,
                "overall_improvement_pct": improvement,
                "consistency": {"days_attended": attended, "total_days": 30}
            }
        
        # Save to output/reports/monthly_reports
        result = {"user_id": user_id, "month": month, "report": report}
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_write_json(self.reports_path / f"month{month}_report_{ts}.json", result)
        logger.info(f"Monthly report saved: month{month}")
        
        return result
