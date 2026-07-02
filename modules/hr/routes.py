from flask import Blueprint, request, jsonify
from database.db import get_connection

hr_bp = Blueprint("hr", __name__)

@hr_bp.route("/hr/employees", methods=["GET"])
def get_employees():
    company_id = request.args.get("company_id")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employees WHERE company_id=?", (company_id,))
    return jsonify([dict(x) for x in cursor.fetchall()])

@hr_bp.route("/hr/employees", methods=["POST"])
def add_employee():
    data = request.get_json()
    company_id = data["company_id"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO employees (name, role, company_id) VALUES (?, ?, ?)",
        (data["name"], data["role"], company_id)
    )

    conn.commit()
    conn.close()

    return jsonify({"status": "created"})
