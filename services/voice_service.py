from pathlib import Path
from utils.logger import get_logger
from utils.helpers import ensure_directory

logger = get_logger(__name__)


class VoiceService:
    """
    Minimal text-to-speech stub.
    It logs feedback and can optionally persist a tiny placeholder audio file.
    """

    def __init__(self, output_dir=None):
        self.output_dir = Path(output_dir) if output_dir else None
        if self.output_dir:
            ensure_directory(self.output_dir)
        logger.info("VoiceService initialized (stub)")

    def text_to_speech(self, text):
        # Return bytes so the caller can save to disk.
        return (text or "").encode("utf-8")

    def play(self, audio_bytes):
        # No-op; we only log for demo mode.
        if audio_bytes:
            logger.info("VoiceService: audio playback simulated")

    def save(self, audio_bytes, path):
        try:
            if not audio_bytes:
                return
            path = Path(path)
            ensure_directory(path.parent)
            path.write_bytes(audio_bytes)
            logger.info(f"VoiceService: saved feedback to {path}")
        except Exception as exc:
            logger.error(f"VoiceService save error: {exc}")
