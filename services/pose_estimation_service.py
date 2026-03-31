import cv2
import mediapipe as mp
from utils.logger import get_logger

logger = get_logger(__name__)


class PoseEstimationService:
    """
    Real-time pose estimation using MediaPipe.
    Returns pose landmarks as a list of (x, y) coordinates in image space.
    """

    def __init__(self, min_detection_conf=0.5, min_tracking_conf=0.5):
        self._mp_pose = mp.solutions.pose
        self._pose = self._mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            enable_segmentation=False,
            min_detection_confidence=min_detection_conf,
            min_tracking_confidence=min_tracking_conf,
        )
        logger.info("PoseEstimationService initialized")

    def estimate(self, frame_packet):
        if not frame_packet or "frame" not in frame_packet:
            return None
        frame = frame_packet["frame"]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self._pose.process(rgb)
        if not result.pose_landmarks:
            return None
        h, w, _ = frame.shape
        landmarks = []
        for lm in result.pose_landmarks.landmark:
            landmarks.append((lm.x * w, lm.y * h))
        return {"landmarks": landmarks, "frame_id": frame_packet.get("frame_id")}
