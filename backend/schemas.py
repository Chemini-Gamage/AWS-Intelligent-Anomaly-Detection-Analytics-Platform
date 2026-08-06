# Create Pydantic Schemas
from pydantic import BaseModel
from datetime import datetime


class EventResponse(BaseModel):

    id: int

    timestamp: datetime

    temperature: float

    pressure: float

    status: str

    class Config:
        from_attributes = True