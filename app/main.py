from fastapi import FastAPI
from app.database import Base, engine
from app.routes import webhooks

Base.metadata.create_all(bind=engine)
app= FastAPI(title="Issue Orchestrator")

app.include_router(webhooks.router, prefix="/webhooks")

@app.get("/")
def project_name():
    return {
        "project_name": "GitHub Issue Orchestrator",
        "version": "1.0.12"
    }