from functools import wraps
from flask import request, jsonify
from auth.jwt_handler import verify_token
from database.db import get_connection

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            token = None
            if "Authorization" in request.headers:
                token = request.headers["Authorization"].split(" ")[1]

            if not token:
                return jsonify({"error": "Token missing"}), 401

            data = verify_token(token)
            if not data:
                return jsonify({"error": "Invalid token"}), 401

            user_id = data["user_id"]

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT role FROM users WHERE id=?", (user_id,))
            user = cursor.fetchone()
            conn.close()

            if not user or user["role"] not in allowed_roles:
                return jsonify({"error": "Forbidden"}), 403

            return f(user_id, *args, **kwargs)

        return wrapper
    return decorator
