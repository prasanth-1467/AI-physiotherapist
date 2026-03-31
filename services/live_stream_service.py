import cv2
import time
from utils.logger import get_logger

logger = get_logger(__name__)


class LiveStreamService:
    """
    Live camera stream using OpenCV.
    """

    def __init__(self, camera_index=0, fps=30, width=640, height=480):
        self.camera_index = camera_index
        self.fps = fps
        self.width = width
        self.height = height
        self._cap = None
        self._running = False
        self._frame_id = 0
        logger.info("LiveStreamService initialized")

    def start(self):
        if self._running:
            return
        self._cap = cv2.VideoCapture(self.camera_index)
        if not self._cap.isOpened():
            raise RuntimeError("Cannot open webcam. Check camera permissions or index.")
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self._running = True
        logger.info("LiveStreamService: webcam stream started")

    def stop(self):
        self._running = False
        if self._cap:
            self._cap.release()
            self._cap = None
        logger.info("LiveStreamService: webcam stream stopped")

    def get_frame(self):
        if not self._running:
            self.start()
        ret, frame = self._cap.read()
        if not ret:
            raise RuntimeError("Failed to read frame from webcam.")
        self._frame_id += 1
        time.sleep(1 / self.fps)
        return {"frame_id": self._frame_id, "ts": time.time(), "frame": frame}
