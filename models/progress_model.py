from pydantic import BaseModel, Field
from typing import List

class ProgressModel(BaseModel):
    user_id: str = Field(..., description="User identifier")
    completion_percentage: float = Field(0.0, description="Overall completion percentage")
    sessions_completed: int = Field(0, description="Total sessions completed")
