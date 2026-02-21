"""Suggestion Agent - Module 2
Input: Module 1 confirmed summary + user rehab goal. Output: 3 exercise suggestions.
"""
import json
from datetime import datetime
from utils.logger import get_logger
from utils.helpers import ensure_directory, safe_write_json, get_week_number
from config import config

logger = get_logger(__name__)

class SuggestionAgent:
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        self.history_path = config.DATA_PATH / "user_profiles" / "rehab_history"
        self.output_path = config.OUTPUT_PATH / "suggestions" / "exercise_suggestions"
        ensure_directory(self.output_path)
        logger.info("SuggestionAgent initialized")

    def _load_rehab_history(self, user_id):
        path = self.history_path / f"{user_id}_history.json"
        try:
            with open(path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"No rehab history for {user_id}")
            return {}

    def _weakest_joint(self, summary):
        joints = summary.get("affected_joints", [])
        if not joints:
            return summary.get("affected_body_part", "shoulder")
        return max(joints, key=lambda j: j.get("deviation", 0)).get("joint", "shoulder")

    def _build_prompt(self, summary, rehab_goal):
        return (
            f"Module 1 summary: {json.dumps(summary)}\n"
            f"User rehab goal: {rehab_goal}\n"
            f"Weakest joint: {self._weakest_joint(summary)}\n"
            f"""Create a rehabilitation exercise plan to achieve the specified rehab goal. While generating the plan, consider the patient’s condition as described in the summary to ensure the exercises are safe, appropriate, and progressive.

Suggest exactly 3 exercises that best support achieving the rehab goal given the patient’s current limitations.

For each exercise, return JSON with the following fields:
name, target_joint, reps, sets, ideal_angle_min, ideal_angle_max, difficulty_level, reason.

Ensure the exercises are clinically relevant to the goal and tailored to the patient’s condition.

Return a JSON array only."""

        )

    def _validate(self, suggestions):
        safe = []
        for s in suggestions:
            mn, mx = s.get("ideal_angle_min", 0), s.get("ideal_angle_max", 180)
            if 0 <= mn < mx <= 180:
                safe.append(s)
            else:
                logger.warning(f"Filtered unsafe: {s.get('name')} angles {mn}-{mx}")
        return safe

    def process_summary(self, summary, user_id, rehab_goal="restore full mobility"):
        logger.info(f"Input: patient={summary.get('patient_id')}, goal={rehab_goal}")
        history = self._load_rehab_history(user_id)
        prompt = self._build_prompt(summary, rehab_goal)
        try:
            raw = self.llm_client.generate(prompt) if self.llm_client else None
            suggestions = json.loads(raw) if raw else self._fallback(summary)
        except Exception as e:
            logger.error(f"LLM error: {e}")
            suggestions = self._fallback(summary)
        suggestions = self._validate(suggestions)
        if not suggestions:
            suggestions = self._fallback(summary)
        week = get_week_number(summary.get("rehab_start_date", datetime.now().isoformat()), datetime.now().isoformat())
        weakest = self._weakest_joint(summary)
        result = {
            "user_id": user_id, "patient_id": summary.get("patient_id", user_id),
            "rehab_goal": rehab_goal, "weakest_joint": weakest,
            "injuries": summary.get("specific_injuries", []),
            "week_number": week, "suggestions": suggestions,
            "total_suggestions": len(suggestions), "status": "success"
        }
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_write_json(self.output_path / f"{user_id}_week{week}_{ts}.json", result)
        logger.info(f"Output: {len(suggestions)} exercises for {user_id} (goal: {rehab_goal})")
        return result

    def _fallback(self, summary):
        w = self._weakest_joint(summary)
        return [
            {"name": f"{w.title()} Raise", "target_joint": w, "reps": 10, "sets": 3,
             "ideal_angle_min": 60, "ideal_angle_max": 180, "difficulty_level": "easy",
             "reason": f"Improves {w} range of motion"},
            {"name": f"{w.title()} Stretch", "target_joint": w, "reps": 8, "sets": 2,
             "ideal_angle_min": 45, "ideal_angle_max": 160, "difficulty_level": "easy",
             "reason": f"Reduces {w} stiffness"},
            {"name": f"{w.title()} Rotation", "target_joint": w, "reps": 12, "sets": 2,
             "ideal_angle_min": 30, "ideal_angle_max": 150, "difficulty_level": "moderate",
             "reason": f"Strengthens {w} stabilizers"}
        ]
