import hmac
import hashlib
import os

def verify_github_signature(body,github_signature):
    secret = os.getenv("GITHUB_WEBHOOK_SECRET")
    if not secret:
        raise ValueError(
            "GITHUB_WEBHOOK_SECRET is not configured"
        )

    expected_signature= (
        "sha256=" +
        hmac.new(
            secret.encode(),
            body,
            hashlib.sha256
        ).hexdigest()
    )
    
    
    return hmac.compare_digest(github_signature,expected_signature)
  