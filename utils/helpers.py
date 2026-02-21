import os
import json
from datetime import datetime
from pathlib import Path

def ensure_directory(path: Path):
    """
    Creates missing directories if they don't exist.
    """
    os.makedirs(path, exist_ok=True)

def timestamp():
    """
    Returns current timestamp in a consistent format.
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def safe_write_json(path: Path, data: dict):
    """
    Safely writes data to a JSON file.
    """
    try:
        ensure_directory(path.parent)
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error writing JSON to {path}: {e}")
