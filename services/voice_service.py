"""Voice Service
Converts feedback text to speech using pyttsx3 (offline TTS engine).
Plays audio immediately and simultaneously saves a WAV file to
output/feedback/voice_feedback/<timestamp>.wav.
Errors are logged and silently skipped — the session is never crashed.
"""
import io
import os
import time
import threading
from pathlib import Path
from utils.logger import get_logger
from config import config

logger = get_logger(__name__)


class VoiceService:
    def __init__(self):
        self._feedback_dir = config.OUTPUT_PATH / "feedback" / "voice_feedback"
        os.makedirs(self._feedback_dir, exist_ok=True)
        self._engine = None
        self._engine_lock = threading.Lock()
        self._init_engine()

    # ------------------------------------------------------------------
    # Public API expected by VoiceFeedbackAgent
    # ------------------------------------------------------------------

    def text_to_speech(self, text: str):
        """Convert text to speech audio.

        Returns:
            str  path to the saved WAV file, or None on failure.
        """
        try:
            return self._synthesise(text)
        except Exception as e:
            logger.error(f"VoiceService.text_to_speech error: {e}")
            return None

    def play(self, audio_path: str):
        """Play audio from the given file path.
        No-op if audio_path is None or the file does not exist.
        """
        if not audio_path or not os.path.isfile(audio_path):
            return
        try:
            self._play_file(audio_path)
        except Exception as e:
            logger.error(f"VoiceService.play error: {e}")

    def save(self, audio_path: str, dest_path: str):
        """Copy/move audio to a custom destination path.
        Since _synthesise already writes to the feedback folder,
        this renames/copies to dest_path if it differs.
        """
        if not audio_path or audio_path == dest_path:
            return
        try:
            import shutil
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(audio_path, dest_path)
            logger.debug(f"VoiceService: saved audio to {dest_path}")
        except Exception as e:
            logger.error(f"VoiceService.save error: {e}")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _init_engine(self):
        """Initialise the pyttsx3 TTS engine."""
        try:
            import pyttsx3
            self._engine = pyttsx3.init()
            self._engine.setProperty("rate", 160)   # words per minute
            self._engine.setProperty("volume", 1.0)
            logger.info("VoiceService: pyttsx3 TTS engine initialised")
        except Exception as e:
            logger.error(f"VoiceService: failed to initialise TTS engine — {e}")
            self._engine = None

    def _synthesise(self, text: str) -> str | None:
        """Synthesise speech, save to a timestamped WAV, and return the path."""
        if self._engine is None:
            logger.error("VoiceService: TTS engine not available, skipping feedback")
            return None

        ts = time.strftime("%Y%m%d_%H%M%S")
        filename = f"voice_feedback_{ts}.wav"
        out_path = str(self._feedback_dir / filename)

        with self._engine_lock:
            try:
                self._engine.save_to_file(text, out_path)
                self._engine.runAndWait()
                logger.debug(f"VoiceService: synthesised → {out_path}")
                return out_path
            except Exception as e:
                logger.error(f"VoiceService: synthesis failed — {e}")
                return None

    def _play_file(self, path: str):
        """Play a WAV file using pyttsx3 proxy or a fallback (playsound)."""
        try:
            from playsound import playsound
            playsound(path, block=False)
            logger.debug(f"VoiceService: playing {path} via playsound")
        except ImportError:
            # Fallback: use pyttsx3 to re-read from file is not ideal;
            # instead use winsound on Windows or subprocess on Unix
            try:
                import platform
                if platform.system() == "Windows":
                    import winsound
                    winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                    logger.debug(f"VoiceService: playing {path} via winsound")
                else:
                    import subprocess
                    subprocess.Popen(["aplay", path])
                    logger.debug(f"VoiceService: playing {path} via aplay")
            except Exception as e:
                logger.error(f"VoiceService: playback failed — {e}")
        except Exception as e:
            logger.error(f"VoiceService: playback failed — {e}")
