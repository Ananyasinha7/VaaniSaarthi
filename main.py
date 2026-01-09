from fastapi import FastAPI
from database import engine
import models
from grievance_api import router as grievance_router

app = FastAPI(title="Backend Intelligence API")

models.Base.metadata.create_all(bind=engine)

app.include_router(grievance_router)

@app.get("/")
def health_check():
    return {"status": "Backend Intelligence running"}
