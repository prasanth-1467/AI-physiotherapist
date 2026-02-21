from pydantic import BaseModel, Field
from typing import List

class SuggestionModel(BaseModel):
    suggestion_id: str = Field(..., description="Suggestion identifier")
    exercise_id: str = Field(..., description="Exercise identifier")
    recommendations: List[str] = Field(default_factory=list, description="Recommended improvements")
