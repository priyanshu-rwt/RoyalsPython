from flask import Blueprint, request, jsonify, current_app
from database.connection import get_db_connection
from services.email_service import send_contact_emails
from utils.career_utils import valid_email

contact_bp = Blueprint("contact", __name__)

@contact_bp.route("/api/contact", methods=["POST"])
def contact():
    conn = None
    cursor = None
    try:
        data = request.get_json(silent=True) or {}
        required = ["name", "email", "phone", "service", "message", "sourcePage"]
        if any(not str(data.get(k, "")).strip() for k in required):
            return jsonify({"success": False, "message": "Please fill in all required fields."}), 400
        if not valid_email(str(data.get("email", "")).strip()):
            return jsonify({"success": False, "message": "Please enter a valid email address."}), 400

        name = str(data["name"]).strip()
        email = str(data["email"]).strip()
        phone = str(data["phone"]).strip()
        company = str(data.get("company", "")).strip()
        service = str(data["service"]).strip()
        message = str(data["message"]).strip()
        source_page = str(data["sourcePage"]).strip()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO enquiries (name, email, phone, company, service, message, source_page)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (name, email, phone, company, service, message, source_page)
        )
        conn.commit()

        send_contact_emails(
            current_app.extensions["mail"], name, email, phone,
            company, service, message, source_page
        )
        return jsonify({"success": True, "message": "Thank you! Your enquiry has been submitted successfully."}), 200

    except Exception as exc:
        print("CONTACT ERROR:", repr(exc))
        if conn:
            conn.rollback()
        return jsonify({"success": False, "message": "Unable to submit enquiry. Please try again later."}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
