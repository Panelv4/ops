from flask import Blueprint, request, jsonify
from database.db import get_connection

crm_bp = Blueprint("crm", __name__)

@crm_bp.route("/crm/leads", methods=["GET"])
def get_leads():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM leads")
    leads = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return jsonify(leads)

@crm_bp.route("/crm/leads", methods=["POST"])
def add_lead():
    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    score = len(data["name"]) * 10  # simple scoring logic

    cursor.execute(
        "INSERT INTO leads (name, score) VALUES (?, ?)",
        (data["name"], score)
    )

    conn.commit()
    conn.close()

    return jsonify({"status": "lead created", "score": score})
