from config import config
from utils.logger import get_logger
from utils.helpers import ensure_directory
from core.pipeline import Pipeline

logger = get_logger(__name__)

class Orchestrator:
    def __init__(self):
        self.pipeline = Pipeline()
        logger.info("Orchestrator initialized")

    def initialize(self):
        """
        Prepare folders and validate environment.
        """
        logger.info("Initializing project structure...")
        
        # Create required directories
        directories = [
            config.RAW_DATA_PATH,
            config.PROCESSED_DATA_PATH,
            config.SESSIONS_PATH,
            config.REPORTS_PATH,
            config.FEEDBACK_PATH,
            config.LOGS_PATH
        ]
        
        for directory in directories:
            ensure_directory(directory)
            logger.debug(f"Ensured directory exists: {directory}")
            
        logger.info("Project structure ready.")

    def run(self):
        """
        Main entry pipeline placeholder.
        """
        logger.info("Orchestrator starting run loop...")
        
        # Skeleton loop execution
        try:
            frame = self.pipeline.capture()
            landmarks = self.pipeline.analyze(frame)
            results = self.pipeline.evaluate(landmarks)
            self.pipeline.store(results)
            
            logger.info("Orchestrator run completed successfully.")
        except Exception as e:
            logger.error(f"Error during orchestrator run: {e}")
            raise
