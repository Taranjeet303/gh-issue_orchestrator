
from pydantic import BaseModel

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