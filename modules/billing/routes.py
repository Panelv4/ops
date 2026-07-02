from flask import Blueprint, request, jsonify

billing_bp = Blueprint("billing", __name__)

@billing_bp.route("/billing/subscribe", methods=["POST"])
def subscribe():
    data = request.get_json()

    plan = data.get("plan", "free")

    return jsonify({
        "status": "success",
        "message": "Subscription created (mock)",
        "plan": plan
    })
