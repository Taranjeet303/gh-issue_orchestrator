from sqlalchemy import Column,String,Text,DateTime,Integer
from datetime import datetime, UTC
from app.database import Base
class GitHubEvent(Base):
    __tablename__ = "github_events"


    id = Column(Integer, primary_key=True, autoincrement=True)
    event_type =Column(String)
    repo_name  = Column(String) 
    issue_number= Column(Integer)
    issue_title  =Column(String)
    issue_body =   Column(Text)
    label =   Column(String)
    status  =      Column(String, default="pending")
    received_at  = Column(DateTime, default=lambda: datetime.now(UTC) )