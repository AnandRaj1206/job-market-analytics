from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import jobs, analytics, chatbot

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Market Analytics Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jobs.router, prefix="/api/jobs", tags=["jobs"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(chatbot.router, prefix="/api/chat", tags=["chatbot"])

@app.get("/")
def root():
    return {"status": "ok"}
