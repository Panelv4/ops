from flask import Blueprint, request, jsonify
from database.db import get_connection

company_bp = Blueprint("company", __name__)

@company_bp.route("/company", methods=["POST"])
def create_company():
    data = request.get_json()
    name = data.get("name")
    owner_id = data.get("owner_id")

    if not name or not owner_id:
        return jsonify({"error": "Missing fields"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO companies (name, owner_id) VALUES (?, ?)",
            (name, owner_id)
        )
        company_id = cursor.lastrowid

        # link user to company
        cursor.execute(
            "UPDATE users SET company_id=? WHERE id=?",
            (company_id, owner_id)
        )

        conn.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

    return jsonify({
        "status": "success",
        "company_id": company_id
    })
