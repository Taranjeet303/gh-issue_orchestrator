
from pydantic import BaseModel
from datetime import datetime
from pydantic import ConfigDict
from typing import Any
class Label(BaseModel):
    name: str

class Issue(BaseModel):
    number: int
    title: str
    body: str
    labels: list[Label]

class Repository(BaseModel):
    full_name: str

class GitHubEvent(BaseModel):
    action: str
    issue: Issue
    repository: Repository

class StepCreate(BaseModel):
    step_order: int
    action_type: str
    config: dict[str, Any]
    retry_limit: int = 3

class StepResponse(BaseModel):
    id: int
    workflow_id: int
    step_order: int
    action_type: str
    config: dict[str, Any]
    retry_limit: int
    created_at: datetime
    model_config = ConfigDict(
        from_attributes=True
    )

class WorkflowCreate(BaseModel):
    name:str
    trigger_event: str
    trigger_label: str
    

class WorkflowResponse(BaseModel):
    id:int
    name: str
    trigger_event: str
    trigger_label: str
    is_active: bool
    created_at: datetime
    steps: list[StepResponse] = []
    model_config = ConfigDict(
        from_attributes=True
    )

