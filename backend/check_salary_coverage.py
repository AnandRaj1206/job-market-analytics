from app.database import SessionLocal
from app.models import JobPosting

db = SessionLocal()
total = db.query(JobPosting).filter(JobPosting.source == "adzuna_api").count()
with_salary = db.query(JobPosting).filter(
    JobPosting.source == "adzuna_api",
    JobPosting.salary_min.isnot(None)
).count()
print(f"Adzuna postings: {total}, with salary data: {with_salary}")
db.close()