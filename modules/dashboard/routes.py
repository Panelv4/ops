from flask import Blueprint, jsonify
from modules.dashboard.service import DashboardService

dashboard_summary_bp = Blueprint("dashboard_summary", __name__)

@dashboard_summary_bp.route("/api/dashboard/summary")
def dashboard_summary():
    return jsonify(DashboardService.summary())

@dashboard_summary_bp.route("/api/dashboard/activity")
def activity():
    return jsonify(DashboardService.activity())
