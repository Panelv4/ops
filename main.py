from flask import Flask, render_template
from modules.crm.routes import crm_bp
from database.db import init_db
from routes.stats import stats_bp
from auth.login import login_bp
from auth.register import register_bp
from auth.rbac import role_required

app = Flask(__name__)
from modules.billing.routes import billing_bp
app.register_blueprint(billing_bp)
app.secret_key = "supersecretkey"

# ---------------- INIT DB ----------------
from database.init_extended import init_extended

init_extended()
# ---------------- BLUEPRINTS ----------------
app.register_blueprint(stats_bp)
app.register_blueprint(register_bp)
app.register_blueprint(login_bp)
app.register_blueprint(crm_bp)
# ---------------- UI ROUTES ----------------
@app.route("/crm")
def crm_page():
    return render_template("crm.html")

@app.route("/support")
def support_page():
    return render_template("support.html")

@app.route("/hr")
def hr_page():
    return render_template("hr.html")
@app.route("/")
def home():
    return render_template("auth/login.html")

@app.route("/register-page")
def register_page():
    return render_template("auth/register.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard/home.html")

@app.route("/users")
def users_page():
    return render_template("admin/users.html")

@app.route("/admin-page")
@role_required(["admin"])
def admin_page(user_id):
    return render_template("admin/panel.html")

@app.route("/logout")
def logout():
    return render_template("auth/login.html")

# ---------------- API TEST ----------------

@app.route("/admin")
@role_required(["admin"])
def admin_api(user_id):
    return {
        "status": "success",
        "message": "Admin access granted",
        "user_id": user_id
    }

# ---------------- START SERVER ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
