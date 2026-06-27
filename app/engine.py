from sqlalchemy.orm import Session
from app import models


def find_matching_workflow(
    db: Session,
    event_type: str,
    label: str
):
    # NOTE:
    # If multiple workflows match the same trigger,
    # this currently returns only the first one found.
    # Supporting multiple matching workflows can be
    # added in a future version.

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