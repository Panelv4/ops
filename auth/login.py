from flask import Blueprint, request, jsonify
from database.db import get_connection
from auth.jwt_handler import generate_token

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data["email"]
    password = data["password"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cursor.fetchone()

    conn.close()

    if not user or user["password"] != password:
        return jsonify({"status": "failed", "message": "invalid credentials"})

    token = generate_token(user)

    return jsonify({
        "status": "success",
        "token": token,
        "user": {
            "id": user["id"],
            "company_id": user["company_id"],
            "role": user["role"],
            "email": user["email"]
        }
    })
