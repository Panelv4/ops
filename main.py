from flask import Flask, render_template, jsonify

from database.init_saas import init_saas
from auth.login import login_bp
from auth.register import register_bp
from modules.billing.routes import billing_bp
from modules.employees.database import init_employees
from modules.employees.routes import employees_bp
from routes.stats import stats_bp
from routes.admin_stats import admin_stats_bp
from routes.dashboard_api import dashboard_api_bp
from routes.activity import activity_bp
from routes.search import search_bp
from routes.dashboard import dashboard_bp
from routes.placeholders import placeholder_bp
app = Flask(__name__)
from modules.attendance.routes import attendance_bp
# Initialize databases
init_saas()
init_employees()
# Register blueprints
@app.route("/")
def home():
    return render_template("home/index.html")
@app.route("/register-page")
def register_page():
    return render_template("auth/register.html")
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard/home.html", title="Dashboard")
@app.route("/admin-page")
def admin_page():
    return render_template("admin/panel.html")
from modules.tasks.database import init_tasks
from modules.tasks.routes import tasks_bp
from modules.crm.database import init_crm
from modules.crm.routes import crm_bp
from modules.inventory.database import init_inventory
from modules.inventory.routes import inventory_bp
from modules.inventory.page import inventory_page_bp
from modules.finance.database import init_finance
from modules.finance.routes import finance_bp
from modules.dashboard.routes import dashboard_summary_bp
from modules.core.hub import hub_bp
init_tasks()
init_crm()
init_inventory()
init_finance()
# =========================
# FINAL CLEAN REGISTRY
app.register_blueprint(register_bp)
app.register_blueprint(login_bp)
app.register_blueprint(billing_bp)
app.register_blueprint(stats_bp)
app.register_blueprint(admin_stats_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(dashboard_api_bp)
app.register_blueprint(dashboard_summary_bp)
app.register_blueprint(activity_bp)
app.register_blueprint(search_bp)
from routes.activity import activity_bp
from routes.search import search_bp
app.register_blueprint(employees_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(tasks_bp)
app.register_blueprint(crm_bp)
app.register_blueprint(inventory_bp)
app.register_blueprint(inventory_page_bp)
app.register_blueprint(finance_bp)
# START SERVER
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
