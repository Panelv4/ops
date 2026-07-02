from auth.register import register_bp
from flask import Flask
from database.db import init_db

app = Flask(__name__)
app.register_blueprint(register_bp)
init_db()

@app.route("/")
def home():
    return {
        "status": "success",
        "message": "OpsPilotAI Backend Running",
        "version": "0.1.0"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
