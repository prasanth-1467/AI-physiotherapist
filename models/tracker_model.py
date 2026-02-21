from pydantic import BaseModel, Field
from typing import Dict, Any

class TrackerModel(BaseModel):
    session_id: str = Field(..., description="Session identifier")
    tracking_data: Dict[str, Any] = Field(default_factory=dict, description="Raw tracking data points")
