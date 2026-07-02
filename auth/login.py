from flask import Blueprint, request, jsonify
from database.db import get_connection
import bcrypt

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    )

    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(
        password.encode(),
        user["password"].encode()
    ):
        return jsonify({
            "status": "success",
            "user": {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
                "company": user["company"]
            }
        })

    return jsonify({
        "status": "failed",
        "message": "Invalid email or password"
    }), 401
