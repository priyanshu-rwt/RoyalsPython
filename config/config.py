import os

def configure_app(app):
    app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", "587"))
    app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    if not app.config["MAIL_USERNAME"] or not app.config["MAIL_PASSWORD"]:
        raise RuntimeError("MAIL_USERNAME and MAIL_PASSWORD are required.")
    if not os.getenv("HR_EMAIL"):
        raise RuntimeError("HR_EMAIL is required.")
