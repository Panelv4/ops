from flask import Blueprint, request, jsonify
from database.db import get_connection

crm_bp = Blueprint("crm", __name__)

@crm_bp.route("/crm/leads", methods=["GET"])
def get_leads():
    company_id = request.args.get("company_id")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM leads WHERE company_id=?", (company_id,))
    return jsonify([dict(x) for x in cursor.fetchall()])

@crm_bp.route("/crm/leads", methods=["POST"])
def add_lead():
    data = request.get_json()
    company_id = data["company_id"]

    score = len(data["name"]) * 10

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO leads (name, score, status, company_id) VALUES (?, ?, ?, ?)",
        (data["name"], score, "new", company_id)
    )

    conn.commit()
    conn.close()

    return jsonify({"status": "created", "score": score})
