from app.database import SessionLocal
from app.models import JobPosting

db = SessionLocal()
db.query(JobPosting).delete()
db.commit()
db.close()
print("Cleared job_postings table.")