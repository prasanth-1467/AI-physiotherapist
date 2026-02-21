"""Angle Calculator Service
Receives landmark coordinates from PoseEstimationService.
For a given joint name, selects the 3 relevant body points and computes
the angle using vector math.

calculate(landmarks, joint_name)
    -> float  (degrees) or None   — used by ResultsAgent / VoiceFeedbackAgent

calculate_full(landmarks, joint_name, ideal_min, ideal_max)
    -> dict   with joint_name, calculated_angle, ideal_min, ideal_max,
               in_range (bool), deviation (0 if in range)
    -> None   if landmarks missing / joint unknown
"""
import math
import numpy as np
from utils.logger import get_logger

logger = get_logger(__name__)

# Maps each joint name to the three landmark names used to compute its angle:
# (proximal, vertex/joint, distal)
JOINT_TRIPLETS = {
    "left_shoulder":  ("left_elbow",  "left_shoulder",  "left_hip"),
    "right_shoulder": ("right_elbow", "right_shoulder", "right_hip"),
    "left_elbow":     ("left_shoulder", "left_elbow",   "left_wrist"),
    "right_elbow":    ("right_shoulder", "right_elbow", "right_wrist"),
    "left_hip":       ("left_shoulder", "left_hip",     "left_knee"),
    "right_hip":      ("right_shoulder", "right_hip",   "right_knee"),
    "left_knee":      ("left_hip",  "left_knee",  "left_ankle"),
    "right_knee":     ("right_hip", "right_knee", "right_ankle"),
    "left_wrist":     ("left_elbow",  "left_wrist",  "left_index"),
    "right_wrist":    ("right_elbow", "right_wrist", "right_index"),
    "left_ankle":     ("left_knee",  "left_ankle",  "left_foot_index"),
    "right_ankle":    ("right_knee", "right_ankle", "right_foot_index"),
}


def _angle_between(a, b, c) -> float:
    """Compute the angle at vertex b formed by points a-b-c (in degrees)."""
    a, b, c = np.array(a, dtype=float), np.array(b, dtype=float), np.array(c, dtype=float)
    ba = a - b
    bc = c - b
    cos_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-9)
    cos_angle = np.clip(cos_angle, -1.0, 1.0)
    return float(math.degrees(math.acos(cos_angle)))


class AngleCalculatorService:
    # ------------------------------------------------------------------
    # Primary method — returns a plain float (used by agents)
    # ------------------------------------------------------------------

    def calculate(self, landmarks: dict, joint_name: str):
        """Compute the joint angle in degrees.

        Returns:
            float  — angle in degrees
            None   — if landmarks is None or required points are missing
        """
        if landmarks is None:
            logger.warning(f"AngleCalculatorService: landmarks is None for joint '{joint_name}'")
            return None

        triplet = JOINT_TRIPLETS.get(joint_name)
        if triplet is None:
            logger.warning(f"AngleCalculatorService: unknown joint '{joint_name}'")
            return None

        name_a, name_b, name_c = triplet
        missing = [n for n in (name_a, name_b, name_c) if n not in landmarks]
        if missing:
            logger.warning(f"AngleCalculatorService: missing landmarks {missing} for joint '{joint_name}'")
            return None

        def coords(name):
            lm = landmarks[name]
            return (lm["x"], lm["y"])  # normalised 2-D coords

        return round(_angle_between(coords(name_a), coords(name_b), coords(name_c)), 2)

    # ------------------------------------------------------------------
    # Extended method — returns full range-comparison dict
    # ------------------------------------------------------------------

    def calculate_full(self, landmarks: dict, joint_name: str,
                       ideal_min: float, ideal_max: float) -> dict:
        """Compute the joint angle and compare against ideal range.

        Returns:
            dict: {joint_name, calculated_angle, ideal_min, ideal_max,
                   in_range (bool), deviation (float)}
            None: if landmarks is None or required points are missing
        """
        angle = self.calculate(landmarks, joint_name)
        if angle is None:
            return None

        in_range = True
        deviation = 0.0
        if angle < ideal_min:
            deviation = ideal_min - angle
            in_range = False
        elif angle > ideal_max:
            deviation = angle - ideal_max
            in_range = False

        return {
            "joint_name": joint_name,
            "calculated_angle": angle,
            "ideal_min": ideal_min,
            "ideal_max": ideal_max,
            "in_range": in_range,
            "deviation": round(deviation, 2),
        }
