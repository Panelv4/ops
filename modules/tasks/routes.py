from flask import Blueprint,render_template,jsonify

tasks_bp=Blueprint("tasks",__name__)

@tasks_bp.route("/tasks")
def tasks():
    return render_template("tasks/index.html")

@tasks_bp.route("/api/tasks")
def api_tasks():
    return jsonify([])
