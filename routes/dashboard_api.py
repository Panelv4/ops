from flask import Blueprint, jsonify
from database.db import get_connection

dashboard_api_bp = Blueprint("dashboard_api", __name__)

@dashboard_api_bp.route("/api/dashboard")
def dashboard():

    conn = get_connection()
    cur = conn.cursor()

    stats = {}

    tables = {
        "employees":"employees",
        "customers":"customers",
        "orders":"orders",
        "products":"products",
        "users":"users"
    }

    for key, table in tables.items():
        try:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            stats[key] = cur.fetchone()[0]
        except:
            stats[key] = 0

    try:
        cur.execute("SELECT IFNULL(SUM(amount),0) FROM payments")
        stats["revenue"] = cur.fetchone()[0]
    except:
        stats["revenue"] = 0

    conn.close()

    return jsonify(stats)
