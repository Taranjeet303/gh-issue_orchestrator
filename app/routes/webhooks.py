from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter()

@router.post("/github")
def receive_github_webhook(
    payload : schemas.GitHubEvent,
    db: Session= Depends(get_db)

):
    
    if payload.action != "labeled":
        return {
            "status": "ignored"
        }
    
        
    critical_found = False

    for label in payload.issue.labels:
     if label.name == "critical":
        critical_found = True
        break

    if not critical_found:
     return {"status": "ignored"}
   

    event = models.GitHubEvent(
    event_type=payload.action,
    repo_name=payload.repository.full_name,
    issue_number=payload.issue.number,
    issue_title=payload.issue.title,
    issue_body=payload.issue.body,
    label="critical"
)

    db.add(event)
    db.commit()

    return {"status": "received"}