"""Pulls job postings from the Adzuna public API (free tier)."""
import requests
from app.config import settings

def fetch_adzuna_jobs(query: str, country: str = "us", pages: int = 1):
    results = []
    for page in range(1, pages + 1):
        url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/{page}"
        params = {
            "app_id": settings.adzuna_app_id,
            "app_key": settings.adzuna_app_key,
            "what": query,
            "content-type": "application/json",
        }
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        for job in data.get("results", []):
            results.append({
                "title": job.get("title"),
                "company": job.get("company", {}).get("display_name"),
                "location": job.get("location", {}).get("display_name"),
                "description": job.get("description"),
                "salary_min": job.get("salary_min"),
                "salary_max": job.get("salary_max"),
                "source": "adzuna_api",
            })
    return results
