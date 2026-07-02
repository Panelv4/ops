from flask import Blueprint, request, jsonify
from database.db import get_connection

support_bp = Blueprint("support", __name__)

@support_bp.route("/support/tickets", methods=["GET"])
def get_tickets():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets")
    tickets = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return jsonify(tickets)

@support_bp.route("/support/tickets", methods=["POST"])
def create_ticket():
    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    priority = "high" if "error" in data["issue"].lower() else "normal"

    cursor.execute(
        "INSERT INTO tickets (issue, status) VALUES (?, ?)",
        (data["issue"], "open")
    )

    conn.commit()
    conn.close()

    return jsonify({"status": "created", "priority": priority})
