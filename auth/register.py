from flask import Blueprint, request, jsonify
from database.db import get_connection
import bcrypt

register_bp = Blueprint("register", __name__)

@register_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    company = data.get("company")

    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    hashed_password = bcrypt.hashpw(
    password.encode(),
    bcrypt.gensalt()
).decode()

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (username, email, password, company)
            VALUES (?, ?, ?, ?)
            """,
            (username, email, hashed_password, company),
        )
        conn.commit()
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 400

    conn.close()

    return jsonify({"message": "User registered successfully"})
