from flask import Blueprint, jsonify
from database.db import get_connection

admin_stats_bp = Blueprint("admin_stats", __name__)

@admin_stats_bp.route("/admin/stats")
def stats():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM companies")
    companies = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        "users": users,
        "companies": companies
    })
