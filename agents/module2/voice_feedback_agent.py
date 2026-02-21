"""Voice Feedback Agent - Module 2
Core: Parallel thread → every 5s read frame → pose → angle → feedback → TTS → save audio
"""
import threading
import time
from utils.logger import get_logger
from utils.helpers import ensure_directory
from config import config

logger = get_logger(__name__)

class VoiceFeedbackAgent:
    def __init__(self, live_stream_service=None, pose_estimation_service=None, 
                 angle_calculator_service=None, voice_service=None):
        self.stream = live_stream_service
        self.pose = pose_estimation_service
        self.angle = angle_calculator_service
        self.voice = voice_service
        self.feedback_path = config.OUTPUT_PATH / "feedback" / "voice_feedback"
        ensure_directory(self.feedback_path)
        self.running = False
        self.thread = None

    def _decide_feedback(self, angle, mn, mx, joint):
        if angle is None:
            return f"Can't detect {joint}, adjust position"
        if mn <= angle <= mx:
            return "Perfect, keep it up!"
        if angle < mn:
            return f"Raise your {joint} a little more"
        return f"Don't overextend {joint}, bring it down slightly"

    def _loop(self, exercise, get_frame):
        targets = exercise.get("movement_targets", [])
        if not targets:
            return
        t = targets[0]
        joint = t["joint_or_region"]
        mn, mx = t["ideal_angle_min"], t["ideal_angle_max"]
        count = 0
        
        while self.running:
            frame = get_frame() if get_frame else (self.stream.get_frame() if self.stream else None)
            kp = self.pose.estimate(frame) if self.pose and frame else None
            angle = self.angle.calculate(kp, joint) if self.angle and kp else None
            text = self._decide_feedback(angle, mn, mx, joint)
            count += 1
            
            if self.voice:
                try:
                    audio = self.voice.text_to_speech(text)
                    self.voice.play(audio)
                    ts = time.strftime("%Y%m%d_%H%M%S")
                    self.voice.save(audio, str(self.feedback_path / f"fb_{count}_{ts}.wav"))
                except Exception as e:
                    logger.error(f"Voice error: {e}")
            
            logger.info(f"Feedback #{count}: {text}")
            time.sleep(5)

    def start(self, exercise, frame_getter=None):
        self.running = True
        self.thread = threading.Thread(target=self._loop, args=(exercise, frame_getter), daemon=True)
        self.thread.start()
        logger.info(f"Voice feedback started: {exercise.get('name','')}")

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=6)
        logger.info("Voice feedback stopped")
