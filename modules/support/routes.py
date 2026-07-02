from flask import Blueprint, request, jsonify
from database.db import get_connection

support_bp = Blueprint("support", __name__)

@support_bp.route("/support/tickets", methods=["GET"])
def get_tickets():
    company_id = request.args.get("company_id")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets WHERE company_id=?", (company_id,))
    return jsonify([dict(x) for x in cursor.fetchall()])

@support_bp.route("/support/tickets", methods=["POST"])
def create_ticket():
    data = request.get_json()
    company_id = data["company_id"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tickets (issue, status, company_id) VALUES (?, ?, ?)",
        (data["issue"], "open", company_id)
    )

    conn.commit()
    conn.close()

    return jsonify({"status": "created"})
