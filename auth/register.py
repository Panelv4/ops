from flask import Blueprint, request, jsonify
from database.db import get_connection

register_bp = Blueprint("register", __name__)

@register_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json(force=True)

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        company_name = data.get("company")

        if not all([username, email, password, company_name]):
            return jsonify({
                "status": "error",
                "message": "missing fields"
            }), 400

        conn = get_connection()
        cursor = conn.cursor()

        # create company
        cursor.execute(
            "INSERT INTO companies (name) VALUES (?)",
            (company_name,)
        )
        company_id = cursor.lastrowid

        # create user
        cursor.execute("""
            INSERT INTO users (username, email, password, role, company_id)
            VALUES (?, ?, ?, ?, ?)
        """, (username, email, password, "admin", company_id))

        conn.commit()

        return jsonify({
            "status": "success",
            "user": email,
            "company_id": company_id
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
