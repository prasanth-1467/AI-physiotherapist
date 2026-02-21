from pydantic import BaseModel, Field

class ResultModel(BaseModel):
    session_id: str = Field(..., description="Session identifier")
    score: float = Field(0.0, description="Exercise performance score")
    accuracy: float = Field(0.0, description="Movement accuracy")
