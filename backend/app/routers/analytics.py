from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app import models, schemas

router = APIRouter()

@router.get("/top-skills")
def top_skills(db: Session = Depends(get_db), limit: int = 15):
    rows = db.query(models.JobPosting.skills).filter(models.JobPosting.skills.isnot(None)).all()
    counts: dict[str, int] = {}
    for (skills_str,) in rows:
        for s in [s.strip() for s in skills_str.split(",") if s.strip()]:
            counts[s] = counts.get(s, 0) + 1
    top = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:limit]
    return [{"skill": k, "count": v} for k, v in top]

@router.get("/salary-trends")
def salary_trends(db: Session = Depends(get_db)):
    rows = (
        db.query(
            models.JobPosting.category,
            func.avg((models.JobPosting.salary_min + models.JobPosting.salary_max) / 2).label("avg_salary"),
            func.count(models.JobPosting.id).label("count"),
        )
        .group_by(models.JobPosting.category)
        .all()
    )
    return [{"category": c, "avg_salary": round(a, 2) if a else None, "count": n} for c, a, n in rows]

@router.get("/top-locations")
def top_locations(db: Session = Depends(get_db), limit: int = 10):
    rows = (
        db.query(
            models.JobPosting.location,
            func.count(models.JobPosting.id).label("count"),
            func.avg((models.JobPosting.salary_min + models.JobPosting.salary_max) / 2).label("avg_salary"),
        )
        .filter(models.JobPosting.location.isnot(None))
        .group_by(models.JobPosting.location)
        .order_by(func.count(models.JobPosting.id).desc())
        .limit(limit)
        .all()
    )
    return [
        {"location": loc, "count": n, "avg_salary": round(a, 2) if a else None}
        for loc, n, a in rows
    ]

@router.post("/skills-gap", response_model=schemas.SkillsGapResponse)
def skills_gap(req: schemas.SkillsGapRequest, db: Session = Depends(get_db)):
    rows = (
        db.query(models.JobPosting.skills)
        .filter(models.JobPosting.category == req.category, models.JobPosting.skills.isnot(None))
        .all()
    )
    counts: dict[str, int] = {}
    for (skills_str,) in rows:
        for s in [s.strip() for s in skills_str.split(",") if s.strip()]:
            counts[s] = counts.get(s, 0) + 1

    top_skills_for_category = [s for s, _ in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]]
    known_lower = {s.lower() for s in req.known_skills}

    matching = [s for s in top_skills_for_category if s.lower() in known_lower]
    missing = [s for s in top_skills_for_category if s.lower() not in known_lower]

    return {
        "matching_skills": matching,
        "missing_skills": missing,
        "top_skills_for_category": top_skills_for_category,
    }