from flask import Blueprint, request, jsonify
from database.db import get_connection

hr_bp = Blueprint("hr", __name__)

@hr_bp.route("/hr/employees", methods=["GET"])
def get_employees():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employees")
    employees = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return jsonify(employees)

@hr_bp.route("/hr/employees", methods=["POST"])
def add_employee():
    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO employees (name, role) VALUES (?, ?)",
        (data["name"], data["role"])
    )

    conn.commit()
    conn.close()

    return jsonify({"status": "employee added"})
