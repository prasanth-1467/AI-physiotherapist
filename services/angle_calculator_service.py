import math
from utils.logger import get_logger

logger = get_logger(__name__)


class AngleCalculatorService:
    """
    Angle calculator using MediaPipe pose landmarks.
    """

    JOINT_MAP = {
        "shoulder": (13, 11, 23),  # elbow, shoulder, hip
        "elbow": (15, 13, 11),     # wrist, elbow, shoulder
        "knee": (27, 25, 23),      # ankle, knee, hip
        "hip": (25, 23, 11),       # knee, hip, shoulder
        "wrist": (19, 15, 13),     # index, wrist, elbow
        "ankle": (31, 27, 25),     # foot index, ankle, knee
        "neck": (7, 11, 23),       # ear, shoulder, hip
        "back": (23, 11, 7),       # hip, shoulder, ear
    }

    def calculate(self, pose_output, joint):
        if not pose_output or "landmarks" not in pose_output:
            return None
        landmarks = pose_output["landmarks"]
        if joint not in self.JOINT_MAP:
            return None
        a_idx, b_idx, c_idx = self.JOINT_MAP[joint]
        try:
            a, b, c = landmarks[a_idx], landmarks[b_idx], landmarks[c_idx]
            return self._angle_from_points(a, b, c)
        except Exception as exc:
            logger.error(f"Angle calculation error: {exc}")
            return None

    def _angle_from_points(self, a, b, c):
        ba = (a[0] - b[0], a[1] - b[1])
        bc = (c[0] - b[0], c[1] - b[1])
        dot = ba[0] * bc[0] + ba[1] * bc[1]
        mag_ba = math.hypot(*ba)
        mag_bc = math.hypot(*bc)
        if mag_ba == 0 or mag_bc == 0:
            return None
        cos_angle = max(-1.0, min(1.0, dot / (mag_ba * mag_bc)))
        return round(math.degrees(math.acos(cos_angle)), 2)

    def calculate_deviation(self, angle, min_angle, max_angle):
        if angle is None:
            return None
        if min_angle <= angle <= max_angle:
            return 0.0
        if angle < min_angle:
            return round(min_angle - angle, 2)
        return round(angle - max_angle, 2)
