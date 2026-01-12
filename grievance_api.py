
from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Grievance
from pydantic import BaseModel

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class GrievanceCreate(BaseModel):
    transcript: str
    audio_url: str = ""
    latitude: float
    longitude: float


CATEGORY_RULES = {
    "Water": ["water", "tap", "pipeline"],
    "Electricity": ["power", "electricity", "light"],
    "Road": ["road", "pothole"],
    "Health": ["hospital", "doctor", "medicine"]
}

HIGH_SEVERITY_WORDS = ["no water", "danger", "emergency", "accident", "for days"]
MEDIUM_SEVERITY_WORDS = ["delay", "not working", "problem"]


def classify_category(text: str):
    text = text.lower()
    for category, keywords in CATEGORY_RULES.items():
        if any(word in text for word in keywords):
            return category
    return "Other"

def extract_keywords(text: str):
    words = text.lower().split()
    return ",".join(list(set(words[:5])))

def detect_severity(text: str):
    text = text.lower()
    if any(word in text for word in HIGH_SEVERITY_WORDS):
        return "HIGH"
    if any(word in text for word in MEDIUM_SEVERITY_WORDS):
        return "MEDIUM"
    return "LOW"


@router.post("/grievance/create")
def create_grievances(
    grievances: List[GrievanceCreate],  # Accept list of grievances
    db: Session = Depends(get_db)
):
    saved_grievances = []

    for g in grievances:
        category = classify_category(g.transcript)
        severity = detect_severity(g.transcript)

        if severity == "HIGH":
            status = "ESCALATED"
            escalation_level = 1
        else:
            status = "NEW"
            escalation_level = 0

        grievance = Grievance(
            transcript=g.transcript,
            audio_url=g.audio_url,
            category=category,
            severity_level=severity,
            urgency_level=severity,
            escalation_level=escalation_level,
            status=status,
            location="Unknown",
            latitude=g.latitude,
            longitude=g.longitude,
            keywords=extract_keywords(g.transcript)
        )

        db.add(grievance)
        db.commit()
        db.refresh(grievance)
        saved_grievances.append({
            "id": grievance.id,
            "category": grievance.category,
            "severity": grievance.severity_level,
            "status": grievance.status,
            "escalation_level": grievance.escalation_level
        })

    return saved_grievances







 
