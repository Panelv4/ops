from flask import Blueprint, request, jsonify
from database.db import get_connection
from auth.jwt_handler import generate_token

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email=?", (data["email"],))
    user = cursor.fetchone()

    conn.close()

    if not user:
        return jsonify({"status": "failed", "message": "user not found"})

    if user["password"] != data["password"]:
        return jsonify({"status": "failed", "message": "wrong password"})

    token = generate_token(user)

    return jsonify({
        "status": "success",
        "token": token,
        "user": {
            "id": user["id"],
            "company_id": user["company_id"],
            "role": user["role"]
        }
    })
