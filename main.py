import sys
from config import config
from utils.logger import get_logger
from core.orchestrator import Orchestrator

# Initialize logger
logger = get_logger("PhysioAI")

def main():
    logger.info("Starting PhysioAI Foundational Environment...")
    
    try:
        # Initialize Orchestrator
        orchestrator = Orchestrator()
        
        # Prepare environment (directories, config)
        orchestrator.initialize()
        
        # Run pipeline stages
        orchestrator.run()
        
        logger.info("PhysioAI initialized and ran successfully.")
        
    except Exception as e:
        logger.critical(f"Application failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
