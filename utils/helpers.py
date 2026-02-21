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

def get_week_number(start_date: str, current_date: str) -> int:
    """
    Calculate which rehab week number based on start date.
    
    Args:
        start_date: Rehab start date (ISO format)
        current_date: Current date (ISO format)
        
    Returns:
        Week number (1-based)
    """
    try:
        start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        current = datetime.fromisoformat(current_date.replace('Z', '+00:00'))
        delta_days = (current - start).days
        return max(1, (delta_days // 7) + 1)
    except Exception as e:
        print(f"Error calculating week number: {e}")
        return 1

def get_month_number(start_date: str, current_date: str) -> int:
    """
    Calculate which rehab month number based on start date.
    
    Args:
        start_date: Rehab start date (ISO format)
        current_date: Current date (ISO format)
        
    Returns:
        Month number (1-based)
    """
    try:
        start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        current = datetime.fromisoformat(current_date.replace('Z', '+00:00'))
        delta_days = (current - start).days
        return max(1, (delta_days // 30) + 1)
    except Exception as e:
        print(f"Error calculating month number: {e}")
        return 1

def format_date(date_obj) -> str:
    """
    Format date as YYYY-MM-DD string.
    
    Args:
        date_obj: datetime object or ISO string
        
    Returns:
        Formatted date string
    """
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.fromisoformat(date_obj.replace('Z', '+00:00'))
        except:
            return date_obj
    return date_obj.strftime("%Y-%m-%d")

def normalize_score(score: float, min_val: float, max_val: float) -> float:
    """
    Convert raw score to 0-100 scale.
    
    Args:
        score: Raw score
        min_val: Minimum possible value
        max_val: Maximum possible value
        
    Returns:
        Normalized score (0-100)
    """
    if max_val == min_val:
        return 50.0
    return ((score - min_val) / (max_val - min_val)) * 100

def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """
    Calculate percentage change between two values.
    
    Args:
        old_value: Original value
        new_value: New value
        
    Returns:
        Percentage change (positive for improvement, negative for regression)
    """
    if old_value == 0:
        return 0.0 if new_value == 0 else 100.0
    return ((new_value - old_value) / old_value) * 100

def generate_session_id(user_id: str, date: str) -> str:
    """
    Generate unique session ID.
    
    Args:
        user_id: User identifier
        date: Date string
        
    Returns:
        Unique session ID
    """
    timestamp_str = datetime.now().strftime("%H%M%S")
    return f"{user_id}_{date}_{timestamp_str}"
