from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")
celery_app = Celery(
    "issue_orchestrator",
    broker=REDIS_URL,
    backend=REDIS_URL

   
)