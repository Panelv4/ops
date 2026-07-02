from flask import Blueprint, request, jsonify
from database.db import get_connection
import bcrypt
from auth.jwt_handler import generate_token

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

    # JOIN users + companies
    cursor.execute("""
        SELECT 
            users.id,
            users.username,
            users.email,
            users.password,
            users.company_id,
            companies.name as company_name
        FROM users
        LEFT JOIN companies
        ON users.company_id = companies.id
        WHERE users.email = ?
    """, (email,))

    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode(), user["password"].encode()):
        token = generate_token(user["id"])

        return jsonify({
            "status": "success",
            "token": token,
            "user": {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
                "company": {
                    "id": user["company_id"],
                    "name": user["company_name"]
                }
            }
        })

    return jsonify({
        "status": "failed",
        "message": "Invalid email or password"
    }), 401
