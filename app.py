import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, jsonify
from flask_cors import CORS
from flask_mail import Mail
from config.config import configure_app
from routes.contact_routes import contact_bp
from routes.career_routes import career_bp
from routes.test_routes import test_bp

app = Flask(__name__)
configure_app(app)

origins = [x.strip() for x in os.getenv("ALLOWED_ORIGINS", "").split(",") if x.strip()]
if not origins:
    raise RuntimeError("ALLOWED_ORIGINS is required in production.")

CORS(app, resources={r"/api/*": {"origins": origins}}, supports_credentials=False)

mail = Mail(app)
app.extensions["mail"] = mail

app.register_blueprint(contact_bp)
app.register_blueprint(career_bp)
app.register_blueprint(test_bp)

@app.route("/")
def home():
    return jsonify({"success": True, "service": "Royals Webtech Backend", "status": "running"})

@app.route("/health")
def health():
    return jsonify({"success": True, "status": "healthy"})

@app.errorhandler(413)
def request_too_large(_error):
    return jsonify({"success": False, "message": "Uploaded file is too large. Maximum size is 5 MB."}), 413

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
