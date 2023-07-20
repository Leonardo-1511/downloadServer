from . import app
import json
from flask import request

accepted_paths = ("/", "/auth", "/test")

@app.before_request
def before_request():
    replitUserId = request.headers.get("X-Replit-User-Id")
    try:
        if int(replitUserId) == 7215759:
            return
    except Exception:
        pass
    if request.path in accepted_paths:
        return
    return json.dumps({"error": "Unauthorized to view these contents. Go to <a href='/'>root</a> or <a href='/auth'>/auth</a>"}), 401