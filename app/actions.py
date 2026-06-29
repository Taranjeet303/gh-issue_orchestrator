from typing import Any
import os

import requests
from dotenv import load_dotenv

from app import models,engine


load_dotenv()


def send_slack_message(
    config: dict[str, Any],
    github_event: models.GitHubEvent
):
    
    slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    if not slack_webhook_url:
        raise ValueError("SLACK_WEBHOOK_URL is not configured")

    
    message_template = config.get("message")

    if not message_template:
        raise ValueError("Message template not found in config")

    
    message = message_template.format(
        title=github_event.issue_title,
        issue_number=github_event.issue_number,
        repo=github_event.repo_name
    )

    
    response = requests.post(
        slack_webhook_url,
        json={
            "text": message
        }
    )

   
    if response.text != "ok":
        raise Exception(
            f"Slack API Error: {response.text}"
        )


ACTION_HANDLERS = {
    "slack": send_slack_message
}

from typing import Any

def execute_action(
    action_type: str,
    config: dict[str, Any],
    github_event: models.GitHubEvent
):
    handler = ACTION_HANDLERS.get(action_type)

    if handler is None:
        raise ValueError(
            f"Unknown action type: {action_type}"
        )

    return handler(
        config,
        github_event
    )