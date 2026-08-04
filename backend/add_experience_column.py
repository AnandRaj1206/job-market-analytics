from sqlalchemy import text
from app.database import engine

with engine.connect() as conn:
    conn.execute(text(
        "ALTER TABLE job_postings ADD COLUMN IF NOT EXISTS years_experience FLOAT"
    ))
    conn.commit()
print("Added years_experience column.")