from pydantic import BaseModel, Field
from typing import List

class ExerciseModel(BaseModel):
    exercise_id: str = Field(..., description="Unique identifier for the exercise")
    name: str = Field(..., description="Name of the exercise")
    description: str = Field(..., description="Detailed description of the exercise")
    target_angles: List[float] = Field(default_factory=list, description="Target joint angles for the exercise")
