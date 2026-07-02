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

    if not username or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (username, email, password, company_id, role)
        VALUES (?, ?, ?, NULL, 'employee')
    """, (username, email, hashed_password))

    conn.commit()
    conn.close()

    return jsonify({"message": "User registered successfully"})
