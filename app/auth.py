from functools import wraps
from flask import request, jsonify
from config import Config

API_KEY = Config.API_KEY

def require_api_key(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        key = request.headers.get("x-api-key")
        if not key:
            return jsonify({"error": "API key is missing."}), 401
        if key != API_KEY:
            return jsonify({"error": "Invalid API key."}), 403
        return func(*args, **kwargs)
    return decorated_function
