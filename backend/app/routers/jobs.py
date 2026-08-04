from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter()

@router.get("/", response_model=list[schemas.JobPostingOut])
def list_jobs(
    db: Session = Depends(get_db),
    category: str | None = None,
    location: str | None = None,
    limit: int = Query(50, le=200),
):
    q = db.query(models.JobPosting)
    if category:
        q = q.filter(models.JobPosting.category == category)
    if location:
        q = q.filter(models.JobPosting.location.ilike(f"%{location}%"))
    return q.limit(limit).all()

@router.post("/predict-salary", response_model=schemas.SalaryPredictionResponse)
def predict_salary(req: schemas.SalaryPredictionRequest):
    from app.services.ml.predict import predict_salary as predict
    return predict(req.title, req.location, req.skills, req.years_experience)