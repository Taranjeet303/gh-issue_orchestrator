import hmac
import hashlib

secret = "mysecretkey30"

body = b'''
{
  "action": "labeled",
  "repository": {
    "full_name": "test/repo"
  },
  "issue": {
    "number": 42,
    "title": "Critical Bug",
    "body": "Fix me",
    "labels": [
      {
        "name": "critical"
      }
    ]
  }
}
'''

signature = (
    "sha256="
    + hmac.new(
        secret.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
)

print(signature)