from sqlalchemy import Column,String,Text,DateTime,Integer,Boolean, ForeignKey,JSON
from datetime import datetime
from sqlalchemy.orm import relationship
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
    received_at = Column(DateTime, default=datetime.utcnow)

class Workflow(Base):
        __tablename__= "workflows"

        id= Column(Integer, primary_key=True)
        name= Column(String)
        trigger_event= Column(String)
        trigger_label= Column(String)
        is_active= Column(Boolean, default=True)
        created_at=Column(DateTime, default=datetime.utcnow)
        
        steps= relationship("WorkflowStep",back_populates="workflow", cascade="all, delete-orphan")

class WorkflowStep(Base):
        __tablename__="workflow_steps" 

        id=Column(Integer, primary_key=True)
        workflow_id=Column(Integer,ForeignKey("workflows.id", ondelete="CASCADE"))
        step_order=Column(Integer)
        action_type=Column(String)
        config=Column(JSON)
        retry_limit=Column(Integer, default=3)
        created_at=Column(DateTime, default=datetime.utcnow)     
        workflow= relationship("Workflow", back_populates="steps")

