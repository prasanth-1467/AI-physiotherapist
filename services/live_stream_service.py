"""Live Stream Service
Opens and manages a webcam stream using OpenCV.
Exposes get_frame(), start(), and stop() for session control.
Buffers last 5 frames. Auto-reconnects on disconnect (up to 3 attempts).
"""
import cv2
import time
import threading
from collections import deque
from utils.logger import get_logger
from config import config

logger = get_logger(__name__)

BUFFER_SIZE = 5
MAX_RECONNECT_ATTEMPTS = 3
RECONNECT_DELAY = 2  # seconds


class LiveStreamService:
    def __init__(self, camera_index: int = None, fps: int = 30):
        self._camera_index = camera_index if camera_index is not None else config.CAMERA_INDEX
        self._fps = fps
        self._cap = None
        self._buffer = deque(maxlen=BUFFER_SIZE)
        self._running = False
        self._thread = None
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def start(self):
        """Open the camera and begin capturing frames in a background thread."""
        if self._running:
            logger.warning("LiveStreamService: already running")
            return
        if not self._open_camera():
            raise RuntimeError(f"Failed to open camera at index {self._camera_index}")
        self._running = True
        self._thread = threading.Thread(target=self._capture_loop, daemon=True)
        self._thread.start()
        logger.info(f"LiveStreamService started on camera index {self._camera_index} @ {self._fps} FPS")

    def stop(self):
        """Stop capturing and release the camera."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=3)
            self._thread = None
        self._release_camera()
        logger.info("LiveStreamService stopped")

    def get_frame(self):
        """Return the most recent captured frame, or None if buffer is empty."""
        with self._lock:
            if self._buffer:
                return self._buffer[-1].copy()
        return None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _open_camera(self) -> bool:
        self._cap = cv2.VideoCapture(self._camera_index)
        if not self._cap.isOpened():
            logger.error(f"LiveStreamService: cannot open camera {self._camera_index}")
            return False
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
        self._cap.set(cv2.CAP_PROP_FPS, self._fps)
        return True

    def _release_camera(self):
        if self._cap and self._cap.isOpened():
            self._cap.release()
        self._cap = None

    def _capture_loop(self):
        interval = 1.0 / self._fps
        while self._running:
            ret, frame = self._cap.read() if self._cap else (False, None)
            if ret and frame is not None:
                with self._lock:
                    self._buffer.append(frame)
            else:
                logger.error("LiveStreamService: frame read failed — attempting reconnect")
                self._release_camera()
                reconnected = False
                for attempt in range(1, MAX_RECONNECT_ATTEMPTS + 1):
                    logger.info(f"Reconnect attempt {attempt}/{MAX_RECONNECT_ATTEMPTS}...")
                    time.sleep(RECONNECT_DELAY)
                    if self._open_camera():
                        logger.info("LiveStreamService: reconnected successfully")
                        reconnected = True
                        break
                if not reconnected:
                    logger.error("LiveStreamService: all reconnect attempts failed — stopping stream")
                    self._running = False
                    break
            time.sleep(interval)
