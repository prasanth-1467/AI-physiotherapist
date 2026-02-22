"""
ALL MODELS COMPLETE - Copy these to individual files
Each model under 50 lines, fully functional
"""

# === exercise_model.py ===
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class MovementTarget(BaseModel):
    joint_or_region: str
    movement_type: str
    ideal_angle_min: float = Field(ge=0, le=180)
    ideal_angle_max: float = Field(ge=0, le=180)
    measurement_plane: str

class ExerciseModel(BaseModel):
    name: str
    reps: int = Field(10, ge=1)
    sets: int = Field(3, ge=1)
    difficulty_level: str = "easy"
    reason: Optional[str] = None
    movement_targets: List[MovementTarget] = []

# === result_model.py ===
class ROMResult(BaseModel):
    joint: str
    observed_min: float
    observed_max: float
    target_min: float
    target_max: float
    status: str

class RepResult(BaseModel):
    rep_number: int
    quality: str
    tempo: str

class StabilityResult(BaseModel):
    score: float = Field(ge=0, le=1)
    label: str

class ResultModel(BaseModel):
    session_id: str
    exercise_name: str
    timestamp: datetime
    rom: List[ROMResult] = []
    reps: List[RepResult] = []
    stability: StabilityResult
    overall_status: str
    overall_score: float = Field(ge=0, le=100)

# === suggestion_model.py ===
class SuggestionModel(BaseModel):
    user_id: str
    rehab_goal: str
    week_number: int = 1
    suggestions: List[dict] = []
    total_suggestions: int = 0

# === feedback_model.py ===
from datetime import date

class FeedbackModel(BaseModel):
    user_id: str
    predicted_recovery_date: date
    feedback_message: str
    feedback_tone: str
    milestones: List[str] = []
    tips: List[str] = []

# === progress_model.py ===
class ProgressModel(BaseModel):
    user_id: str
    days_completed: int
    completion_percentage: float
    overall_trend: str
    overall_improvement: float

# === tracker_model.py ===
class TrackerModel(BaseModel):
    user_id: str
    week_number: int
    week_completed: bool = False
    days_logged: int
    analysis: Optional[dict] = None

# === summary_model.py ===
class SummaryModel(BaseModel):
    patient_id: str
    problem: str
    affected_body_part: str
    severity: str
    confirmed: bool = False

# === report_model.py ===
class ReportModel(BaseModel):
    user_id: str
    report_type: str
    period: str
    summary: str
    improvement_percentage: float

# === user_model.py ===
class UserModel(BaseModel):
    user_id: str
    name: str
    age: Optional[int] = None
    injuries: List[str] = []
    rehab_goal: Optional[str] = None
