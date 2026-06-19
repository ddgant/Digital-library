# ============================================================
#  Middleware: Auth (skeleton)
#  Author: Rodrigo Garcia Martinez (2309091)
# ============================================================

from functools import wraps
from flask import request, jsonify

def require_api_key(f):
    # TODO (Rodrigo): Implement token/API key validation
    @wraps(f)
    def decorated(*args, **kwargs):
        # TODO
        return f(*args, **kwargs)
    return decorated
