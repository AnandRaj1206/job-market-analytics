"""
Natural-language querying over job market data using Groq's free API
(Llama 3.3 models). Pulls a small relevant slice of aggregated stats
and lets the LLM reason over it, rather than dumping the whole DB
into the prompt.
"""
from groq import Groq
from app.config import settings
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import JobPosting

client = Groq(api_key=settings.groq_api_key)

def build_context(db: Session) -> str:
    top_categories = (
        db.query(JobPosting.category, func.count(JobPosting.id))
        .group_by(JobPosting.category)
        .order_by(func.count(JobPosting.id).desc())
        .limit(10)
        .all()
    )
    avg_salary_by_category = (
        db.query(JobPosting.category, func.avg((JobPosting.salary_min + JobPosting.salary_max) / 2))
        .group_by(JobPosting.category)
        .all()
    )
    lines = ["Top job categories by posting count:"]
    lines += [f"- {c}: {n} postings" for c, n in top_categories]
    lines.append("\nAverage salary by category:")
    lines += [f"- {c}: ${s:,.0f}" for c, s in avg_salary_by_category if s]
    return "\n".join(lines)

def answer_query(db: Session, user_message: str) -> str:
    context = build_context(db)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=500,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a job market analyst assistant. Answer using only "
                    "the aggregated statistics provided below. If the data "
                    "doesn't cover the question, say so.\n\n" + context
                ),
            },
            {"role": "user", "content": user_message},
        ],
    )
    return response.choices[0].message.content
