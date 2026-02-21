from pydantic import BaseModel, Field
from typing import Optional

class UserModel(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user")
    name: str = Field(..., description="Full name of the user")
    age: Optional[int] = Field(None, description="Age of the user")
    height: Optional[float] = Field(None, description="Height in cm")
    weight: Optional[float] = Field(None, description="Weight in kg")
