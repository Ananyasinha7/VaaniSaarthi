from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from datetime import datetime

class Grievance(Base):
    __tablename__ = "grievances"

    id = Column(Integer, primary_key=True, index=True)
    transcript = Column(String, nullable=False)
    audio_url = Column(String, default="")
    category = Column(String)
    severity_level = Column(String)
    urgency_level = Column(String)
    escalation_level = Column(Integer)
    status = Column(String)
    location = Column(String, default="Unknown")
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    keywords = Column(String)




