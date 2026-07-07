from flask import Blueprint, render_template, request, jsonify
from modules.employees.service import EmployeeService

employees_bp = Blueprint("employees", __name__)

# ---------- UI ----------

@employees_bp.route("/employees")
def employees_page():
    return render_template("employees/index.html")


# ---------- API ----------

@employees_bp.route("/api/employees", methods=["GET"])
def list_employees():
    return jsonify(EmployeeService.all())


@employees_bp.route("/api/employees/<int:employee_id>", methods=["GET"])
def get_employee(employee_id):
    employee = EmployeeService.get(employee_id)
    if employee is None:
        return jsonify({"status": "error", "message": "Employee not found"}), 404
    return jsonify(employee)


@employees_bp.route("/api/employees", methods=["POST"])
def create_employee():
    data = request.get_json(force=True)
    employee_id = EmployeeService.create(data)
    from database.activity import log_activity
    log_activity("employees","create","Employee created")
    return jsonify({
        "status": "success",
        "employee_id": employee_id
    }), 201


@employees_bp.route("/api/employees/<int:employee_id>", methods=["PUT"])
def update_employee(employee_id):
    data = request.get_json(force=True)
    EmployeeService.update(employee_id, data)
    return jsonify({"status": "success"})


@employees_bp.route("/api/employees/<int:employee_id>", methods=["DELETE"])
def delete_employee(employee_id):
    EmployeeService.delete(employee_id)
    return jsonify({"status": "success"})


@employees_bp.route("/api/employees/search")
def search_employees():
    keyword = request.args.get("q", "")
    return jsonify(EmployeeService.search(keyword))


@employees_bp.route("/api/employees/stats")
def employee_stats():
    return jsonify(EmployeeService.stats())
