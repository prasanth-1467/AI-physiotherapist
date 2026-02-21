"""Voice Feedback Agent - Module 2
Provides real-time audio feedback during exercises every 5 seconds.
"""
import threading, time
from utils.logger import get_logger
from utils.helpers import ensure_directory, timestamp
from config import config

logger = get_logger(__name__)
INTERVAL = 5

class VoiceFeedbackAgent:
    def __init__(self, voice_service=None, pose_estimation_service=None, angle_calculator_service=None):
        self.voice = voice_service
        self.pose = pose_estimation_service
        self.angle = angle_calculator_service
        self.feedback_path = config.OUTPUT_PATH / "feedback" / "voice_feedback"
        ensure_directory(self.feedback_path)
        self._running = False
        self._thread = None
        self._count = 0

    def _get_feedback(self, angle, mn, mx, joint):
        if angle is None:
            return f"Can't detect your {joint}, adjust your position"
        if mn <= angle <= mx:
            return "Perfect, keep it up!"
        if angle < mn:
            return f"Raise your {joint} a little more"
        if angle > mx:
            return f"Don't overextend your {joint}, bring it down slightly"

    def _loop(self, exercise, frame_getter):
        joint = exercise["target_joint"]
        mn, mx = exercise["ideal_angle_min"], exercise["ideal_angle_max"]
        while self._running:
            frame = frame_getter() if frame_getter else None
            kp = self.pose.estimate(frame) if self.pose and frame else None
            angle = self.angle.calculate(kp, joint) if self.angle and kp else None
            text = self._get_feedback(angle, mn, mx, joint)
            self._count += 1
            if self.voice:
                try:
                    audio = self.voice.text_to_speech(text)
                    self.voice.play(audio)
                    path = self.feedback_path / f"feedback_{self._count}_{timestamp()}.wav"
                    self.voice.save(audio, str(path))
                except Exception as e:
                    logger.error(f"Voice error: {e}")
            logger.info(f"Feedback #{self._count}: {text}")
            time.sleep(INTERVAL)

    def start(self, exercise, frame_getter=None):
        self._running = True
        self._thread = threading.Thread(target=self._loop, args=(exercise, frame_getter), daemon=True)
        self._thread.start()
        logger.info(f"Voice feedback started for {exercise['name']}")

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=INTERVAL + 1)
        logger.info(f"Voice feedback stopped after {self._count} feedbacks")

class VoiceFeedbackContext:
    def __init__(self, agent, exercise, frame_getter=None):
        self.agent = agent
        self.exercise = exercise
        self.frame_getter = frame_getter
    def __enter__(self):
        self.agent.start(self.exercise, self.frame_getter)
        return self.agent
    def __exit__(self, *args):
        self.agent.stop()