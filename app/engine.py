from sqlalchemy.orm import Session
from app import models
from datetime import datetime

def find_matching_workflow(
    db: Session,
    event_type: str,
    label: str
):
# NOTE:
# Currently, this function returns only the first matching workflow.
# Supporting multiple matching workflows can be added in a future version.
    workflow = (
        db.query(models.Workflow)
        .filter(models.Workflow.is_active == True)
        .filter(models.Workflow.trigger_event == event_type)
        .filter(models.Workflow.trigger_label == label)
        .first()
    )

    if workflow is None:
        return None

    return workflow




def execute_workflow(
    db: Session,
    workflow: models.Workflow,
    github_event: models.GitHubEvent
):
    execution = models.Execution(
        workflow_id=workflow.id,
        github_event_id=github_event.id,
        status="running",
        current_step=0
    )

    db.add(execution)
    db.commit()
    db.refresh(execution)

    try:
        steps = (
            db.query(models.WorkflowStep)
            .filter(models.WorkflowStep.workflow_id == workflow.id)
            .order_by(models.WorkflowStep.step_order)
            .all()
        )

        for step in steps:
            print(f"Executing step {step.step_order}: {step.action_type}")
            

            execution.current_step = step.step_order

            # TODO:
            # Execute the real action here (Slack, Email, Discord, etc.)
            # For now, we simply simulate success.

            db.commit()

        execution.status = "success"
        execution.completed_at = datetime.utcnow()

        db.commit()
        db.refresh(execution)

    except Exception as e:
        execution.status = "failed"
        execution.error_message = str(e)
        execution.completed_at = datetime.utcnow()

        db.commit()
        db.refresh(execution)

    return execution