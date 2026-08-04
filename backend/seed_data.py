"""
Seeds realistic sample job postings with overlapping skills across
categories, so category classification is a genuine ML challenge
rather than a keyword lookup. Also generates a real, varying
years_experience value per posting.
"""
import random
from datetime import datetime, timedelta
from app.database import SessionLocal, Base, engine
from app.models import JobPosting

Base.metadata.create_all(bind=engine)

TITLES_BY_CATEGORY = {
    "Data Science": ["Data Scientist", "Machine Learning Engineer", "Data Analyst", "AI Researcher"],
    "Backend": ["Backend Engineer", "Python Developer", "API Developer", "Software Engineer"],
    "Frontend": ["Frontend Developer", "React Developer", "UI Engineer", "Web Developer"],
    "DevOps": ["DevOps Engineer", "Site Reliability Engineer", "Cloud Engineer", "Infrastructure Engineer"],
    "Product": ["Product Manager", "Technical Product Manager", "Product Owner"],
}

COMMON_SKILLS = ["Python", "SQL", "Git", "Communication", "Agile", "AWS", "Docker"]

LEANING_SKILLS = {
    "Data Science": ["Machine Learning", "Pandas", "TensorFlow", "Statistics"],
    "Backend": ["FastAPI", "PostgreSQL", "Redis", "Microservices"],
    "Frontend": ["React", "JavaScript", "CSS", "TypeScript"],
    "DevOps": ["Kubernetes", "Terraform", "CI/CD", "Linux"],
    "Product": ["Roadmapping", "Jira", "Analytics", "Stakeholder Management"],
}

DESCRIPTION_TEMPLATES = [
    "We're hiring someone to join our growing team. You'll work closely with cross-functional partners and take ownership of key initiatives. Experience with {skill1} and {skill2} is a strong plus.",
    "Looking for a {seniority} professional who thrives in a fast-paced environment. Day-to-day work involves {skill1}, with exposure to {skill2} and {skill3} over time.",
    "Join our team! We value curiosity and collaboration over pure years of experience, though comfort with {skill1} will help you ramp up quickly.",
    "Our team needs someone to help scale our product. Prior work involving {skill1} or {skill2} is preferred but not required if you're a fast learner.",
    "New opening on our team - you'll be responsible for delivering high-quality work end to end, using tools like {skill1} and {skill2} daily.",
]

SENIORITY_LEVELS = [
    ("Junior", 0.75, 0, 2),
    ("Mid-level", 1.0, 2, 5),
    ("Senior", 1.35, 5, 9),
    ("Lead", 1.65, 8, 15),
]

BASE_SALARY_BY_CATEGORY = {
    "Data Science": 110000,
    "Backend": 105000,
    "Frontend": 95000,
    "DevOps": 115000,
    "Product": 120000,
}

LOCATION_MULTIPLIER = {
    "Bengaluru": 1.1,
    "Remote": 1.05,
    "Hyderabad": 1.0,
    "Pune": 0.95,
    "Mumbai": 1.08,
    "Delhi NCR": 1.0,
}

COMPANIES = ["Nimbus Tech", "Datalynx", "Coreflow", "Stackwise", "BrightGrid", "Vector Labs"]

def pick_skills(category):
    skills = random.sample(COMMON_SKILLS, k=2)
    skills += random.sample(LEANING_SKILLS[category], k=2)
    if random.random() < 0.25:
        other_category = random.choice([c for c in LEANING_SKILLS if c != category])
        skills.append(random.choice(LEANING_SKILLS[other_category]))
    random.shuffle(skills)
    return skills[:4]

def seed(n=800):
    db = SessionLocal()
    try:
        for _ in range(n):
            category = random.choice(list(TITLES_BY_CATEGORY.keys()))
            base_title = random.choice(TITLES_BY_CATEGORY[category])
            seniority, seniority_mult, exp_lo, exp_hi = random.choice(SENIORITY_LEVELS)
            years_experience = random.randint(exp_lo, exp_hi)
            location = random.choice(list(LOCATION_MULTIPLIER.keys()))

            skills = pick_skills(category)
            title = base_title

            base = BASE_SALARY_BY_CATEGORY[category]
            noise = random.uniform(0.92, 1.08)
            salary_center = base * seniority_mult * LOCATION_MULTIPLIER[location] * noise
            salary_min = round(salary_center * 0.93, -3)
            salary_max = round(salary_center * 1.07, -3)

            template = random.choice(DESCRIPTION_TEMPLATES)
            description = template.format(
                seniority=seniority.lower(),
                skill1=skills[0],
                skill2=skills[1] if len(skills) > 1 else skills[0],
                skill3=skills[2] if len(skills) > 2 else skills[0],
            )

            job = JobPosting(
                title=title,
                company=random.choice(COMPANIES),
                location=location,
                description=description,
                salary_min=salary_min,
                salary_max=salary_max,
                category=category,
                source="seed_script_v4",
                skills=", ".join(skills),
                years_experience=years_experience,
                posted_date=datetime.now() - timedelta(days=random.randint(0, 60)),
            )
            db.add(job)
        db.commit()
        print(f"Seeded {n} realistic job postings with overlapping skills and years_experience.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()