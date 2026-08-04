from app.database import SessionLocal
from app.models import JobPosting
from app.services.ml.experience_extractor import estimate_years_experience

db = SessionLocal()
try:
    jobs = db.query(JobPosting).filter(JobPosting.years_experience.is_(None)).all()
    for job in jobs:
        job.years_experience = estimate_years_experience(job.title, job.description)
    db.commit()
    print(f"Backfilled years_experience for {len(jobs)} postings.")
finally:
    db.close()