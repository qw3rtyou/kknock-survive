import os
from flask import Flask, render_template, session, g
from config import Config
from models import init_db

from upload import file_bp
from auth import auth_bp, login_required
from audit import audit_bp
from gpt import gpt_bp

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.environ.get("SECRET_KEY", "default_secret_key")

@app.before_request
def load_user():
    g.user_id = session.get("username", "Guest")

@app.context_processor
def inject_user():
    return {"user_id": g.get("user_id", "Guest")}

@app.route("/", methods=["GET"])
@login_required
def index():
    return render_template("index.html")

app.register_blueprint(file_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(audit_bp, url_prefix='/audit')
app.register_blueprint(gpt_bp, url_prefix='/gpt')

if __name__ == "__main__":
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        init_db(app)
    app.run(host="0.0.0.0", port=8080, debug=True)
