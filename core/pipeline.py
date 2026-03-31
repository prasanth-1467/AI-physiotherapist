from utils.logger import get_logger
from utils.helpers import safe_write_json, timestamp
from services import LiveStreamService, PoseEstimationService, AngleCalculatorService
from config import config

logger = get_logger(__name__)

class Pipeline:
    def __init__(self, stream=None, pose=None, angle=None):
        self.stream = stream or LiveStreamService(
            camera_index=config.CAMERA_INDEX,
            fps=30,
            width=config.FRAME_WIDTH,
            height=config.FRAME_HEIGHT,
        )
        self.pose = pose or PoseEstimationService()
        self.angle = angle or AngleCalculatorService()
        self.output_path = config.OUTPUT_PATH / "predictions" / "recovery_predictions"
        logger.info("Pipeline initialized")

    def capture(self):
        """
        Stage 1: Capture frame from source.
        """
        logger.debug("Executing stage: capture")
        return self.stream.get_frame()

    def analyze(self, frame):
        """
        Stage 2: Use pose logic to analyze landmarks.
        """
        logger.debug("Executing stage: analyze")
        return self.pose.estimate(frame)

    def evaluate(self, landmarks):
        """
        Stage 3: Evaluate pose against exercise standards.
        """
        logger.debug("Executing stage: evaluate")
        joints = ["shoulder", "elbow", "knee", "hip", "ankle", "wrist"]
        angles = {}
        for joint in joints:
            angle = self.angle.calculate(landmarks, joint)
            if angle is not None:
                angles[joint] = round(float(angle), 2)
        return {"angles": angles, "status": "success"}

    def store(self, results):
        """
        Stage 4: Store session data and results.
        """
        logger.debug("Executing stage: store")
        payload = {
            "timestamp": timestamp(),
            "results": results,
        }
        safe_write_json(self.output_path / f"prediction_{payload['timestamp']}.json", payload)
        return payload
