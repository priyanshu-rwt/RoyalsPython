import os
from flask import Blueprint, request, jsonify, current_app
from database.connection import get_db_connection
from services.email_service import send_career_emails
from services.storage_service import upload_resume, delete_file
from utils.career_utils import extract_detail, allowed_resume_file, secure_resume_filename, valid_email

career_bp = Blueprint("career", __name__)

@career_bp.route("/api/career/apply", methods=["POST"])
def career_apply():
    conn = None
    cursor = None
    storage_bucket = None
    storage_path = None
    try:
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip()
        phone = (request.form.get("phone") or "").strip()
        position = (request.form.get("position") or "").strip()
        application_type = (request.form.get("applicationType") or "").strip()
        experience = (request.form.get("experience") or "").strip()
        combined_message = request.form.get("message", "")
        resume = request.files.get("resume")

        location = extract_detail(combined_message, "Location:")
        college = extract_detail(combined_message, "College:")
        degree = extract_detail(combined_message, "Degree:")
        branch = extract_detail(combined_message, "Branch:")
        semester = extract_detail(combined_message, "Semester:")
        internship_skills = extract_detail(combined_message, "Skills:")
        linkedin = extract_detail(combined_message, "LinkedIn:")
        github = extract_detail(combined_message, "GitHub:")
        portfolio = extract_detail(combined_message, "Portfolio:")
        cover_message = extract_detail(combined_message, "Message:")

        if not all([application_type, name, email, phone, position]):
            return jsonify({"success": False, "message": "Please fill in all required personal details."}), 400
        if not valid_email(email):
            return jsonify({"success": False, "message": "Please enter a valid email address."}), 400
        if not resume or not resume.filename:
            return jsonify({"success": False, "message": "Please upload your resume."}), 400
        if not allowed_resume_file(resume.filename):
            return jsonify({"success": False, "message": "Only PDF, DOC or DOCX resumes are allowed."}), 400

        resume.seek(0, os.SEEK_END)
        file_size = resume.tell()
        resume.seek(0)
        if file_size > 5 * 1024 * 1024:
            return jsonify({"success": False, "message": "Resume must be smaller than 5 MB."}), 400

        filename = secure_resume_filename(resume.filename)
        resume_data = resume.read()
        storage_bucket, storage_path = upload_resume(filename, resume_data, resume.content_type)

        current_company = ""
        expected_ctc = ""
        notice_period = ""
        job_skills = ""

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO career_applications (
                application_type, full_name, email, phone, location, position,
                college, degree, branch, semester, internship_skills, experience,
                current_company, expected_ctc, notice_period, job_skills,
                resume_filename, resume_path, linkedin, github, portfolio, message
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """,
            (
                application_type, name, email, phone, location, position,
                college, degree, branch, semester, internship_skills, experience,
                current_company, expected_ctc, notice_period, job_skills,
                filename, storage_path, linkedin, github, portfolio, cover_message
            )
        )
        conn.commit()

        send_career_emails(
            current_app.extensions["mail"], name, email, phone, location, position,
            application_type, college, degree, branch, semester, internship_skills,
            experience, current_company, expected_ctc, notice_period, job_skills,
            linkedin, github, portfolio, cover_message, filename, resume_data,
            resume.content_type
        )
        return jsonify({"success": True, "message": "Your application has been submitted successfully."}), 200

    except Exception as exc:
        print("CAREER ERROR:", repr(exc))
        if conn:
            conn.rollback()
        if storage_bucket and storage_path:
            delete_file(storage_bucket, storage_path)
        return jsonify({"success": False, "message": "Unable to submit your application. Please try again later."}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
