import hmac
import hashlib

secret = "mysecretkey30"

body = b'{\r\n  "action": "labeled",\r\n  "repository": {\r\n    "full_name": "test/repo"\r\n  },\r\n  "issue": {\r\n    "number": 42,\r\n    "title": "Critical Bug",\r\n    "body": "Fix me",\r\n    "labels": [\r\n      {\r\n        "name": "critical"\r\n      }\r\n    ]\r\n  }\r\n}'

signature = (
    "sha256="
    + hmac.new(
        secret.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
)

print(signature)