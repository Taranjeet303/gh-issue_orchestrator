from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter()


@router.post("/workflows", response_model=schemas.WorkflowResponse)
def create_workflow(
    workflow: schemas.WorkflowCreate,
    db: Session = Depends(get_db)
):
    new_workflow = models.Workflow(
        name=workflow.name,
        trigger_event=workflow.trigger_event,
        trigger_label=workflow.trigger_label,
        
    )

    db.add(new_workflow)
    db.commit()
    db.refresh(new_workflow)

    return new_workflow


@router.get("/workflows", response_model=list[schemas.WorkflowResponse])
def get_workflows(db: Session = Depends(get_db)):
    workflows = db.query(models.Workflow).all()
    return workflows


@router.get("/workflows/{workflow_id}", response_model=schemas.WorkflowResponse)
def get_workflow(
    workflow_id: int,
    db: Session = Depends(get_db)
):
    workflow = (
        db.query(models.Workflow)
        .filter(models.Workflow.id == workflow_id)
        .first()
    )

    if not workflow:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found"
        )

    return workflow


@router.post("/workflows/{workflow_id}/steps", response_model=schemas.StepResponse)
def add_step_to_workflow(
    workflow_id: int,
    step: schemas.StepCreate,
    db: Session = Depends(get_db)
):
    workflow = (
        db.query(models.Workflow)
        .filter(models.Workflow.id == workflow_id)
        .first()
    )

    if not workflow:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found"
        )

    new_step = models.WorkflowStep(
        workflow_id=workflow_id,
        step_order=step.step_order,
        action_type=step.action_type,
        config=step.config,
        retry_limit=step.retry_limit
    )

    db.add(new_step)
    db.commit()
    db.refresh(new_step)

    return new_step