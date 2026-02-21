from pydantic import BaseModel, Field
from datetime import datetime

class ReportModel(BaseModel):
    report_id: str = Field(..., description="Unique report identifier")
    user_id: str = Field(..., description="User identifier")
    session_id: str = Field(..., description="Session identifier")
    summary: str = Field(..., description="Textual summary of the report")
    timestamp: datetime = Field(default_factory=datetime.now)
