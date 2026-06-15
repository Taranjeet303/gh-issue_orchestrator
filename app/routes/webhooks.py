from fastapi import APIRouter, Depends,Request, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.security import verify_github_signature
router = APIRouter()
@router.post("/github")
async def receive_github_webhook(
    request: Request,
    db: Session = Depends(get_db)
):

    body = await request.body()

    github_signature = request.headers.get(
        "X-Hub-Signature-256"
    )

    if not github_signature:
        raise HTTPException(
            status_code=401,
            detail="Missing signature"
        )

    if not verify_github_signature(
        body,
        github_signature
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid signature"
        )

    payload_dict = await request.json()

    payload = schemas.GitHubEvent(
        **payload_dict
    )


    
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
    db.refresh(event)

    return {"status": "received"}