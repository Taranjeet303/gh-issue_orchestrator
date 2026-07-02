from app.celery_app import celery_app
from app import models
from app.engine import execute_workflow
from app.database import SessionLocal


@celery_app.task
def process_github_event_task(
    github_event_id:int ,
    workflow_id:int
    ):
    db = SessionLocal()
    
    try:
        github_event=(
           db.query(models.GitHubEvent)
           .filter(models.GitHubEvent.id==github_event_id)
           .first()
        )
        if github_event is None:
            raise ValueError("Github event not found")

        workflow=(
            db.query(models.Workflow)
            .filter(models.Workflow.id==workflow_id)
            .first()
        )
        if workflow is None:
            raise ValueError("Workflow not found")
        
        execute_workflow(
            db,
            workflow,
            github_event
)
        
    finally:
        db.close()


  

