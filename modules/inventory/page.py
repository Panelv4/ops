from flask import Blueprint, render_template

inventory_page_bp = Blueprint("inventory_page", __name__)

@inventory_page_bp.route("/inventory")
def inventory_page():
    return render_template("inventory/index.html")
