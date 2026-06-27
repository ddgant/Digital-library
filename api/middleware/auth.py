# ============================================================
#  Middleware: API key validation
#  Author: Rodrigo Garcia Martinez (2309091)
# ============================================================

from functools import wraps
from flask import request, jsonify
import os

API_KEY = os.getenv("API_KEY", "teamx-dev-key")


def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get("X-API-Key")
        if not key or key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated
