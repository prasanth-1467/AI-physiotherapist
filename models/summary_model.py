from pydantic import BaseModel, Field

class SummaryModel(BaseModel):
    session_id: str = Field(..., description="Session identifier")
    total_time: float = Field(0.0, description="Total exercise time in seconds")
    reps_completed: int = Field(0, description="Total repetitions completed")
