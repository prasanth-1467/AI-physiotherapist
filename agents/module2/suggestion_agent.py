"""Suggestion Agent - Module 2
Core: Receives summary + rehab goal → LLM generates 3 exercises → validates angles → saves
"""
import json
from datetime import datetime
from utils.logger import get_logger
from utils.helpers import ensure_directory, safe_write_json
from config import config

logger = get_logger(__name__)

class SuggestionAgent:
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        self.output_path = config.OUTPUT_PATH / "suggestions" / "exercise_suggestions"
        ensure_directory(self.output_path)

    def get_rehab_goal(self):
        """Get rehab goal from user (placeholder for interactive input)"""
        return "restore full mobility"

    def process_summary(self, summary, user_id, rehab_goal=None):
        """Main: summary + goal → LLM → 3 exercises → validate → save"""
        if not rehab_goal:
            rehab_goal = self.get_rehab_goal()
        
        # Build LLM prompt
        prompt = f"""
Summary: {json.dumps(summary)}
Rehab Goal: {rehab_goal}

Create a rehabilitation exercise plan to achieve the specified rehab goal. While generating the plan, consider the patient's condition as described in the summary to ensure the exercises are safe, appropriate, and progressively challenging.

Suggest exactly 3 exercises that best support achieving the rehab goal given the patient's current limitations.

Each exercise may involve different joints, anatomical regions, or measurement angles. Therefore, include a flexible structure that captures exercise-specific biomechanical targets.

Return JSON array:
[{{
  "name": "string",
  "reps": number,
  "sets": number,
  "difficulty_level": "easy | moderate | hard",
  "reason": "string",
  "movement_targets": [{{
    "joint_or_region": "string",
    "movement_type": "string",
    "ideal_angle_min": number,
    "ideal_angle_max": number,
    "measurement_plane": "sagittal | frontal | transverse | functional"
  }}]
}}]]
"""
        
        # Get LLM response
        try:
            raw = self.llm_client.generate(prompt) if self.llm_client else None
            suggestions = json.loads(raw) if raw else []
        except:
            suggestions = []
        
        # Validate angles (0 <= min < max <= 180)
        validated = []
        for ex in suggestions:
            valid = all(0 <= t["ideal_angle_min"] < t["ideal_angle_max"] <= 180 
                       for t in ex.get("movement_targets", []))
            if valid:
                validated.append(ex)
        
        # Save to output/suggestions/exercise_suggestions
        result = {"user_id": user_id, "rehab_goal": rehab_goal, "suggestions": validated}
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_write_json(self.output_path / f"{user_id}_{ts}.json", result)
        logger.info(f"Generated {len(validated)} exercises for {user_id}")
        
        return result
