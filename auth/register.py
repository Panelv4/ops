from flask import Blueprint, request, jsonify
from database.db import get_connection

register_bp = Blueprint("register", __name__)

@register_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data["username"]
    email = data["email"]
    password = data["password"]
    company_name = data["company"]

    conn = get_connection()
    cursor = conn.cursor()

    # create company
    cursor.execute("INSERT INTO companies (name) VALUES (?)", (company_name,))
    company_id = cursor.lastrowid

    # create user linked to company
    cursor.execute("""
        INSERT INTO users (username, email, password, role, company_id)
        VALUES (?, ?, ?, ?, ?)
    """, (username, email, password, "admin", company_id))

    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "SaaS workspace created",
        "company_id": company_id
    })
