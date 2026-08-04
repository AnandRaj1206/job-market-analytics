"""
Pulls real job postings from Adzuna across multiple countries and
role categories, extracts skills via keyword matching, and stores
them in the database. Run with: python fetch_real_data.py
"""
import time
from app.database import SessionLocal, Base, engine
from app.models import JobPosting
from app.services.data_collection.api_client import fetch_adzuna_jobs
from datetime import datetime

Base.metadata.create_all(bind=engine)

COUNTRIES = ["in", "us", "gb", "au"]

SEARCH_QUERIES = {
    "data scientist": "Data Science",
    "backend engineer": "Backend",
    "frontend developer": "Frontend",
    "devops engineer": "DevOps",
    "product manager": "Product",
}

SKILL_VOCAB = [
    "Python", "SQL", "Java", "JavaScript", "TypeScript", "React", "Angular",
    "Vue", "Node.js", "FastAPI", "Django", "Flask", "AWS", "Azure", "GCP",
    "Docker", "Kubernetes", "Terraform", "CI/CD", "Git", "PostgreSQL",
    "MySQL", "MongoDB", "Redis", "Machine Learning", "TensorFlow", "PyTorch",
    "Pandas", "NumPy", "Spark", "Airflow", "Agile", "Scrum", "Jira",
    "Roadmapping", "Analytics", "Linux", "REST API", "GraphQL", "CSS", "HTML",
]

def extract_skills(description: str) -> list[str]:
    if not description:
        return []
    found = [skill for skill in SKILL_VOCAB if skill.lower() in description.lower()]
    return found[:8]

def run():
    db = SessionLocal()
    total_inserted = 0
    try:
        for country in COUNTRIES:
            for query, category in SEARCH_QUERIES.items():
                print(f"Fetching [{country}]: {query}...")
                try:
                    jobs = fetch_adzuna_jobs(query=query, country=country, pages=1)
                except Exception as e:
                    print(f"  -> skipped ({e})")
                    continue

                for job_data in jobs:
                    skills = extract_skills(job_data.get("description", ""))
                    job = JobPosting(
                        title=job_data.get("title"),
                        company=job_data.get("company"),
                        location=job_data.get("location"),
                        description=job_data.get("description"),
                        salary_min=job_data.get("salary_min"),
                        salary_max=job_data.get("salary_max"),
                        category=category,
                        source=f"adzuna_api_{country}",
                        skills=", ".join(skills),
                        posted_date=datetime.now(),
                    )
                    db.add(job)
                    total_inserted += 1
                db.commit()
                print(f"  -> inserted {len(jobs)} postings")
                time.sleep(1)  # be polite to the API, avoid rate-limit issues
        print(f"Done. Total inserted: {total_inserted}")
    finally:
        db.close()

if __name__ == "__main__":
    run()