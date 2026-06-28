from fastapi import APIRouter, Depends,Request, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.security import verify_github_signature
from app.utils import  build_response
from app.engine import find_matching_workflow,execute_workflow
router = APIRouter()
@router.post("/github")
async def receive_github_webhook(
    request: Request,
    db: Session = Depends(get_db)
):

    body = await request.body()
     # Check event type before signature verification.
# This endpoint only processes GitHub issue events.
# Non-issue events are ignored immediately to avoid
# unnecessary HMAC verification work.

    github_event = request.headers.get(
       "X-GitHub-Event"
    )
    if github_event != "issues":
       return build_response(
        status="ignored",
        message="Event type not supported",
        data=None
    )
    

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
        return build_response( status= "ignored",
             message= "Event not critical or not labeled action",
             data= None   )
   
    
        
    critical_found = False

    for label in payload.issue.labels:
     if label.name == "critical":
        critical_found = True
        break

    if not critical_found:
     return build_response( status= "ignored",
             message= "Event not critical or not labeled action",
             data= None   )
   

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

   
    workflow = find_matching_workflow(
     db,
     event.event_type,
     event.label
)

    if workflow is None:
      return build_response(
        status="ignored",
        message="No matching workflow found",
        data=None
    )

    execution = execute_workflow(
     db,
     workflow,
     event
)

    return build_response(
    status="success",
    message="Workflow executed successfully",
    data={
        "execution_id": execution.id,
        "workflow_id": workflow.id,
        "execution_status": execution.status
    }
)
