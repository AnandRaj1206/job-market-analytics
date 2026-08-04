from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class JobPostingOut(BaseModel):
    id: int
    title: str
    company: str
    location: str
    salary_min: Optional[float]
    salary_max: Optional[float]
    category: Optional[str]
    skills: Optional[str]
    posted_date: datetime

    class Config:
        from_attributes = True

class SalaryPredictionRequest(BaseModel):
    title: str
    location: str
    skills: List[str]
    years_experience: int

class SalaryPredictionResponse(BaseModel):
    predicted_salary: float
    confidence_range: List[float]

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

class SkillsGapRequest(BaseModel):
    category: str
    known_skills: List[str]

class SkillsGapResponse(BaseModel):
    matching_skills: List[str]
    missing_skills: List[str]
    top_skills_for_category: List[str]

class ReportRequest(BaseModel):
    category: str

class ReportResponse(BaseModel):
    report_markdown: str