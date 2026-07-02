from flask import Blueprint, jsonify
from database.db import get_connection

stats_bp = Blueprint("stats", __name__)

@stats_bp.route("/stats")
def stats():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM leads")
    leads = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tickets")
    tickets = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM employees")
    employees = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        "leads": leads,
        "tickets": tickets,
        "employees": employees
    })
