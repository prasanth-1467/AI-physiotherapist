"""Results Agent - Module 2
Tracks real-time exercise performance by monitoring pose and angles.
"""
import time, json
from datetime import datetime
from utils.logger import get_logger
from utils.helpers import ensure_directory, safe_write_json, timestamp
from config import config

logger = get_logger(__name__)
RATINGS = [(90, "Excellent"), (75, "Good"), (60, "Fair"), (40, "Needs Improvement"), (0, "Poor")]

class ResultsAgent:
    def __init__(self, live_stream_service=None, pose_estimation_service=None, angle_calculator_service=None):
        self.stream = live_stream_service
        self.pose = pose_estimation_service
        self.angle = angle_calculator_service
        self.angle_path = config.DATA_PATH / "processed" / "angle_data"
        self.results_path = config.OUTPUT_PATH / "results"
        ensure_directory(self.angle_path)
        ensure_directory(self.results_path)

    def _get_rating(self, score):
        return next(label for thresh, label in RATINGS if score >= thresh)

    def _track_exercise(self, ex, fps=30, duration=30):
        joint = ex["target_joint"]
        mn, mx = ex["ideal_angle_min"], ex["ideal_angle_max"]
        correct, total, errors, err_start = 0, 0, [], None
        for _ in range(fps * duration):
            frame = self.stream.get_frame() if self.stream else None
            kp = self.pose.estimate(frame) if self.pose and frame else None
            angle = self.angle.calculate(kp, joint) if self.angle and kp else None
            if angle is None:
                continue
            total += 1
            if mn <= angle <= mx:
                correct += 1
                if err_start is not None:
                    errors.append({"joint": joint, "avg_deviation": abs(angle - (mn + mx) / 2),
                                   "duration": (total - err_start) / fps, "frame_start": err_start, "frame_end": total})
                    err_start = None
            else:
                if err_start is None:
                    err_start = total
        score = (correct / total * 100) if total else 0
        return {"exercise_name": ex["name"], "target_joint": joint, "ideal_angle_min": mn,
                "ideal_angle_max": mx, "total_frames": total, "correct_frames": correct,
                "performance_score": round(score, 1), "performance_rating": self._get_rating(score), "errors": errors}

    def process_suggestions(self, suggestions):
        user_id = suggestions["user_id"]
        results = [self._track_exercise(ex) for ex in suggestions["suggestions"]]
        avg = round(sum(r["performance_score"] for r in results) / len(results), 1) if results else 0
        date_str = datetime.now().strftime("%Y-%m-%d")
        ts = timestamp()
        result = {"user_id": user_id, "session_date": date_str, "total_exercises": len(results),
                  "average_score": avg, "results": results, "status": "success"}
        safe_write_json(self.results_path / f"{user_id}_{date_str}_{ts}_results.json", result)
        safe_write_json(self.angle_path / f"{user_id}_{date_str}_{ts}_results.json", result)
        logger.info(f"Tracked {len(results)} exercises for {user_id}, avg score: {avg}")
        return result