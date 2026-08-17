import os
import base64
import requests


RESEND_API_URL = "https://api.resend.com/emails"

# Resend testing mode recipient
TEST_EMAIL = "priyanshukumar.royalswebtech@gmail.com"


def send_resend_email(payload):
    api_key = os.getenv("RESEND_API_KEY")

    if not api_key:
        raise RuntimeError("RESEND_API_KEY is not configured.")

    response = requests.post(
        RESEND_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=20,
    )

    if not response.ok:
        raise RuntimeError(
            f"Resend email failed: {response.status_code} {response.text}"
        )

    return response.json()


def get_sender():
    return os.getenv("MAIL_FROM", "onboarding@resend.dev")


def send_contact_emails(
    mail,
    name,
    email,
    phone,
    company,
    service,
    message,
    source_page
):
    sender = get_sender()

    hr_payload = {
        "from": sender,
        "to": [TEST_EMAIL],
        "subject": f"New Website Enquiry - {service}",
        "text": f"""A new enquiry has been submitted from the Royals Webtech website.

Name: {name}
Email: {email}
Phone: {phone}
Company: {company}
Service: {service}

Requirement:
{message}

Source: {source_page}

NOTE:
This email is being sent to the Resend testing account.
The applicant email is {email}.
Applicant confirmation email will be enabled after domain verification.
""",
    }

    send_resend_email(hr_payload)


def send_career_emails(
    mail,
    name,
    email,
    phone,
    location,
    position,
    application_type,
    college,
    degree,
    branch,
    semester,
    internship_skills,
    experience,
    current_company,
    expected_ctc,
    notice_period,
    job_skills,
    linkedin,
    github,
    portfolio,
    cover_message,
    filename,
    resume_data,
    resume_content_type
):
    sender = get_sender()

    attachments = []

    if resume_data and filename:
        attachments.append({
            "filename": filename,
            "content": base64.b64encode(resume_data).decode("utf-8"),
        })

    hr_payload = {
        "from": sender,
        "to": [TEST_EMAIL],
        "subject": f"New Career Application - {position}",
        "text": f"""A new career application has been submitted from the Royals Webtech website.

APPLICANT DETAILS

Name: {name}
Email: {email}
Phone: {phone}
Location: {location}
Position: {position}
Application Type: {application_type}


ACADEMIC INFORMATION

College: {college}
Degree: {degree}
Branch: {branch}
Semester: {semester}
Skills: {internship_skills}


PROFESSIONAL INFORMATION

Experience: {experience}
Current Company: {current_company}
Expected CTC: {expected_ctc}
Notice Period: {notice_period}
Job Skills: {job_skills}


ONLINE PROFILES

LinkedIn: {linkedin}
GitHub: {github}
Portfolio: {portfolio}


COVER MESSAGE

{cover_message}


RESUME

Filename: {filename}
Applicant Email: {email}

NOTE:
This email is being sent to the Resend testing account.
Applicant confirmation email will be enabled after domain verification.
""",
    }

    if attachments:
        hr_payload["attachments"] = attachments

    send_resend_email(hr_payload)