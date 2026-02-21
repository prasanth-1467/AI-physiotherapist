from pydantic import BaseModel, Field
from datetime import datetime

class FeedbackModel(BaseModel):
    feedback_id: str = Field(..., description="Unique identifier for feedback")
    session_id: str = Field(..., description="Linked session identifier")
    message: str = Field(..., description="Feedback message for the user")
    timestamp: datetime = Field(default_factory=datetime.now)
