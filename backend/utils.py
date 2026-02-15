import base64
from functools import wraps
from flask import request, jsonify
from os import environ


# ============================================================
# Authorization check
# ============================================================
def is_authorized() -> bool:

    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Basic "):
        return False

    try:
        encoded = auth_header.split(" ")[1]
        decoded = base64.b64decode(encoded).decode()
        username, password = decoded.split(":", 1)
    except Exception:
        return False

    return (
        username == environ["USERNAME"]
        and password == environ["PASSWORD"]
    )


# ============================================================
# Decorator
# ============================================================
def login_required(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):

        if not is_authorized():
            return jsonify({"error": "Unauthorized"}), 401

        return fn(*args, **kwargs)

    return wrapper
