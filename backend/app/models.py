from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime
from app.database import Base

class JobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String, index=True)
    location = Column(String, index=True)
    description = Column(Text)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    category = Column(String, index=True)
    source = Column(String)
    skills = Column(String)
    years_experience = Column(Float, nullable=True)
    posted_date = Column(DateTime, default=datetime.utcnow)
    scraped_at = Column(DateTime, default=datetime.utcnow)
