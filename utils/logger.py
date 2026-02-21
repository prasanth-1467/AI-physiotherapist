import os
import logging
import sys
from logging.handlers import RotatingFileHandler
from config import config

def get_logger(name: str):
    """
    Returns a reusable logger with console and file logging.
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.DEBUG if config.DEBUG else logging.INFO)
        
        # Ensure logs directory exists
        os.makedirs(config.LOGS_PATH, exist_ok=True)
        
        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # File Handler
        log_file = config.LOGS_PATH / "app.log"
        file_handler = RotatingFileHandler(
            log_file, maxBytes=10*1024*1024, backupCount=5
        )
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
    return logger
