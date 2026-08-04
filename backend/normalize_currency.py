"""
Converts salary fields for non-US Adzuna postings into USD, using
fixed approximate exchange rates, so the salary model trains on a
single consistent currency. Run once: python normalize_currency.py
"""
from app.database import SessionLocal
from app.models import JobPosting

# Approximate rates to USD (fixed for simplicity — a real app would
# pull these from a live FX API).
RATES_TO_USD = {
    "adzuna_api_in": 0.012,   # INR -> USD
    "adzuna_api_gb": 1.27,    # GBP -> USD
    "adzuna_api_au": 0.66,    # AUD -> USD
    "adzuna_api_us": 1.0,     # already USD
}

def run():
    db = SessionLocal()
    try:
        updated = 0
        for source, rate in RATES_TO_USD.items():
            if rate == 1.0:
                continue
            jobs = db.query(JobPosting).filter(JobPosting.source == source).all()
            for job in jobs:
                if job.salary_min is not None:
                    job.salary_min = round(job.salary_min * rate, 2)
                if job.salary_max is not None:
                    job.salary_max = round(job.salary_max * rate, 2)
                updated += 1
        db.commit()
        print(f"Normalized currency for {updated} postings.")
    finally:
        db.close()

if __name__ == "__main__":
    run()