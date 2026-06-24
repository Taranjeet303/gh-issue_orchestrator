from fastapi import FastAPI
from app.database import Base, engine
from app.routes import webhooks,workflows

Base.metadata.create_all(bind=engine)
app= FastAPI(title="Issue Orchestrator")

app.include_router(webhooks.router, prefix="/webhooks",tags=["webhooks"])

@app.get("/")
def project_name():
    return {
        "project_name": "GitHub Issue Orchestrator",
        "version": "1.0.12"
    }
app.include_router(workflows.router,tags=["workflows"])