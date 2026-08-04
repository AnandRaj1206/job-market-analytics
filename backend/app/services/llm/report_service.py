"""
Generates a structured, multi-section career report for a given job
category — inspired by a multi-agent research pattern, implemented
as three sequential Groq calls against our own database (no external
web search, so this stays fully within the free Groq tier with no
extra API dependency):

  1. Data summarizer  -> turns raw DB aggregates into a clean summary
  2. Market analyst    -> reasons over the summary, extracts insights
  3. Report writer      -> writes the final structured markdown report
"""
from groq import Groq
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.config import settings
from app.models import JobPosting

client = Groq(api_key=settings.groq_api_key)
MODEL = "llama-3.3-70b-versatile"

def _get_db_stats(db: Session, category: str) -> str:
    postings = db.query(JobPosting).filter(JobPosting.category == category).all()
    if not postings:
        return f"No data available for category '{category}'."

    salaries = [(p.salary_min + p.salary_max) / 2 for p in postings if p.salary_min and p.salary_max]
    avg_salary = sum(salaries) / len(salaries) if salaries else None

    skill_counts: dict[str, int] = {}
    for p in postings:
        if p.skills:
            for s in [x.strip() for x in p.skills.split(",") if x.strip()]:
                skill_counts[s] = skill_counts.get(s, 0) + 1
    top_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:8]

    loc_counts: dict[str, int] = {}
    for p in postings:
        if p.location:
            loc_counts[p.location] = loc_counts.get(p.location, 0) + 1
    top_locations = sorted(loc_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    lines = [
        f"Category: {category}",
        f"Total postings analyzed: {len(postings)}",
        f"Average salary: ${avg_salary:,.0f}" if avg_salary else "Average salary: not available",
        "Top skills: " + ", ".join(f"{s} ({c})" for s, c in top_skills),
        "Top locations: " + ", ".join(f"{l} ({c})" for l, c in top_locations),
    ]
    return "\n".join(lines)

def _call_groq(system_prompt: str, user_prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=700,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content

def generate_career_report(db: Session, category: str) -> str:
    raw_stats = _get_db_stats(db, category)

    # Step 1: summarize raw stats into clean bullet points
    summary = _call_groq(
        system_prompt="You summarize raw job market statistics into 4-6 clean, factual bullet points. No commentary, just facts.",
        user_prompt=raw_stats,
    )

    # Step 2: analyze the summary for insights
    analysis = _call_groq(
        system_prompt=(
            "You are a job market analyst. Given a factual summary of postings "
            "data, identify 3-4 concrete insights: what's in demand, what pays "
            "well, and what a candidate should focus on. Be specific and concise."
        ),
        user_prompt=summary,
    )

    # Step 3: write the final structured report
    report = _call_groq(
        system_prompt=(
            "You are a career report writer. Using the analyst's insights below, "
            "write a structured markdown report with these exact sections: "
            "## Executive Summary, ## Top In-Demand Skills, ## Salary Outlook, "
            "## Top Hiring Locations, ## Action Plan. Keep it concise and "
            "practical for a job seeker. Base everything only on the provided data."
        ),
        user_prompt=f"Category: {category}\n\nAnalyst insights:\n{analysis}",
    )

    return report