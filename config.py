import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

class Config(BaseModel):
    # Environment
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Camera Settings
    CAMERA_INDEX: int = int(os.getenv("CAMERA_INDEX", 0))
    FRAME_WIDTH: int = int(os.getenv("FRAME_WIDTH", 640))
    FRAME_HEIGHT: int = int(os.getenv("FRAME_HEIGHT", 480))
    
    # Path Settings
    BASE_DIR: Path = Path(__file__).parent.absolute()
    DATA_PATH: Path = BASE_DIR / os.getenv("DATA_PATH", "storage/")
    OUTPUT_PATH: Path = BASE_DIR / os.getenv("OUTPUT_PATH", "output/")
    
    # Subdirectories
    RAW_DATA_PATH: Path = DATA_PATH / "raw"
    PROCESSED_DATA_PATH: Path = DATA_PATH / "processed"
    SESSIONS_PATH: Path = DATA_PATH / "sessions"
    
    REPORTS_PATH: Path = OUTPUT_PATH / "reports"
    FEEDBACK_PATH: Path = OUTPUT_PATH / "feedback"
    LOGS_PATH: Path = OUTPUT_PATH / "logs"

    class Config:
        arbitrary_types_allowed = True

# Global config instance
config = Config()
