"""Suggestion Agent - Module 2
Generates personalized exercise suggestions from confirmed injury summary.
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

    def _build_prompt(self, summary, history):
        return (f"Given this injury: {json.dumps(summary)}\nRehab history: {json.dumps(history)}\n"
                "Suggest 2-3 rehab exercises. For each return JSON with: name, target_joint, reps, "
                "sets, ideal_angle_min, ideal_angle_max, difficulty_level, reason. Return a JSON array only.")

    def _validate(self, suggestions):
        safe = []
        for s in suggestions:
            mn, mx = s.get("ideal_angle_min", 0), s.get("ideal_angle_max", 180)
            if 0 <= mn < mx <= 180:
                safe.append(s)
            else:
                logger.warning(f"Filtered unsafe suggestion: {s.get('name')} angles {mn}-{mx}")
        return safe

    def process_summary(self, summary, user_id):
        history = self._load_rehab_history(user_id)
        prompt = self._build_prompt(summary, history)
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
        result = {"user_id": user_id, "week_number": week, "suggestions": suggestions,
                  "total_suggestions": len(suggestions), "status": "success"}
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_write_json(self.output_path / f"{user_id}_week{week}_{ts}.json", result)
        logger.info(f"Generated {len(suggestions)} suggestions for {user_id}")
        return result

    def _fallback(self, summary):
        part = summary.get("affected_body_part", "shoulder")
        return [{"name": f"{part.title()} Raise", "target_joint": part, "reps": 10, "sets": 3,
                 "ideal_angle_min": 60, "ideal_angle_max": 180, "difficulty_level": "easy",
                 "reason": f"Improves {part} mobility"}]