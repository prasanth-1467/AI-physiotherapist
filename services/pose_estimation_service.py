"""Pose Estimation Service
Receives a single BGR frame, runs MediaPipe PoseLandmarker (IMAGE mode),
extracts 33 body landmark coordinates, filters by visibility threshold,
and returns a dict of landmark_name -> {x, y, z, visibility}.
Returns None if no person is detected.
"""
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from utils.logger import get_logger

logger = get_logger(__name__)

# MediaPipe canonical landmark names (index → name)
LANDMARK_NAMES = [
    "nose", "left_eye_inner", "left_eye", "left_eye_outer",
    "right_eye_inner", "right_eye", "right_eye_outer",
    "left_ear", "right_ear",
    "mouth_left", "mouth_right",
    "left_shoulder", "right_shoulder",
    "left_elbow", "right_elbow",
    "left_wrist", "right_wrist",
    "left_pinky", "right_pinky",
    "left_index", "right_index",
    "left_thumb", "right_thumb",
    "left_hip", "right_hip",
    "left_knee", "right_knee",
    "left_ankle", "right_ankle",
    "left_heel", "right_heel",
    "left_foot_index", "right_foot_index",
]

DEFAULT_MODEL_PATH = "pose_landmarker_lite.task"
DEFAULT_VISIBILITY_THRESHOLD = 0.5


class PoseEstimationService:
    def __init__(self, model_path: str = DEFAULT_MODEL_PATH,
                 visibility_threshold: float = DEFAULT_VISIBILITY_THRESHOLD):
        self._visibility_threshold = visibility_threshold
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            min_pose_detection_confidence=0.5,
            min_pose_presence_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self._landmarker = vision.PoseLandmarker.create_from_options(options)
        logger.info(f"PoseEstimationService initialised (model: {model_path})")

    def estimate(self, frame):
        """Run pose estimation on a single BGR frame.

        Returns:
            dict  landmark_name -> {x, y, z, visibility}  (only visible landmarks)
            None  if no person detected or frame is None
        """
        if frame is None:
            logger.warning("PoseEstimationService: received None frame")
            return None

        # Convert BGR (OpenCV) to RGB for MediaPipe
        frame_rgb = frame[:, :, ::-1].copy()
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        results = self._landmarker.detect(mp_image)

        if not results.pose_landmarks:
            logger.warning("PoseEstimationService: no person detected in frame")
            return None

        landmarks_raw = results.pose_landmarks[0]
        landmarks = {}
        for idx, lm in enumerate(landmarks_raw):
            name = LANDMARK_NAMES[idx] if idx < len(LANDMARK_NAMES) else str(idx)
            visibility = getattr(lm, "visibility", 1.0)
            if visibility < self._visibility_threshold:
                continue  # skip unreliable detections
            landmarks[name] = {
                "x": lm.x,
                "y": lm.y,
                "z": lm.z,
                "visibility": visibility,
            }

        if not landmarks:
            logger.warning("PoseEstimationService: all landmarks below visibility threshold")
            return None

        return landmarks
