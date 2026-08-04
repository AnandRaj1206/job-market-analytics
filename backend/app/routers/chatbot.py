from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.llm.chatbot_service import answer_query
from app.services.llm.report_service import generate_career_report
from app import schemas

router = APIRouter()

@router.post("/", response_model=schemas.ChatResponse)
def chat(req: schemas.ChatRequest, db: Session = Depends(get_db)):
    reply = answer_query(db, req.message)
    return {"reply": reply}

@router.post("/report", response_model=schemas.ReportResponse)
def career_report(req: schemas.ReportRequest, db: Session = Depends(get_db)):
    report = generate_career_report(db, req.category)
    return {"report_markdown": report}

@router.get("/report/download")
def download_career_report(category: str, db: Session = Depends(get_db)):
    report = generate_career_report(db, category)
    filename = f"{category.replace(' ', '_').lower()}_career_report.md"
    return Response(
        content=report,
        media_type="text/markdown",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )