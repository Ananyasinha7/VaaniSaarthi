from pydantic import BaseModel
from typing import Optional

class GrievanceCreate(BaseModel):
    transcript: str
    audio_url: Optional[str] = ""
    latitude: float
    longitude: float

