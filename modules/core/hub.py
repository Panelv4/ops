from flask import Blueprint, jsonify

hub_bp = Blueprint("hub", __name__)

@hub_bp.route("/api/system/health", methods=["GET"])
def system_health():
    return jsonify({
        "status": "running",
        "modules": [
            "employees",
            "attendance",
            "dashboard"
        ]
    })
