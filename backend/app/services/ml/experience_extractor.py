"""Estimates years of experience implied by a job posting's title/description."""
import re

SENIORITY_YEARS = {
    "intern": 0,
    "junior": 1,
    "entry": 1,
    "associate": 2,
    "mid": 3,
    "senior": 6,
    "lead": 8,
    "principal": 10,
    "staff": 10,
    "director": 12,
}

def estimate_years_experience(title: str, description: str = "") -> float:
    text = f"{title or ''} {description or ''}".lower()

    # Look for explicit patterns like "5+ years" or "3-5 years"
    match = re.search(r"(\d+)\s*\+?\s*(?:-\s*\d+\s*)?years?", text)
    if match:
        return float(match.group(1))

    # Fall back to seniority keyword in the title
    for keyword, years in SENIORITY_YEARS.items():
        if keyword in text:
            return float(years)

    return 3.0  # reasonable default for unspecified mid-level roles