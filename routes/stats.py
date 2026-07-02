from flask import Blueprint, request, jsonify
from database.db import get_connection

stats_bp = Blueprint("stats", __name__)

@stats_bp.route("/stats")
def stats():
    company_id = request.args.get("company_id")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM leads WHERE company_id=?", (company_id,))
    leads = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tickets WHERE company_id=?", (company_id,))
    tickets = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM employees WHERE company_id=?", (company_id,))
    employees = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        "leads": leads,
        "tickets": tickets,
        "employees": employees
    })
