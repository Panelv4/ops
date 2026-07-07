from flask import Blueprint, request, jsonify
from database.db import get_connection

finance_bp = Blueprint("finance", __name__)

@finance_bp.route("/api/finance", methods=["GET"])
def list_transactions():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM finance ORDER BY id DESC")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify(rows)

@finance_bp.route("/api/finance", methods=["POST"])
def add_transaction():
    data = request.get_json()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO finance
        (type, category, description, amount, company_id)
        VALUES (?,?,?,?,?)
    """, (
        data["type"],
        data.get("category",""),
        data.get("description",""),
        data["amount"],
        data.get("company_id",1)
    ))

    conn.commit()
    tid = cur.lastrowid
    conn.close()

    return jsonify({"status":"success","id":tid})
