import re
from werkzeug.utils import secure_filename

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def extract_detail(message, label):
    if not message:
        return ""
    for line in message.splitlines():
        if line.startswith(label):
            return line[len(label):].strip()
    return ""

def allowed_resume_file(filename):
    allowed_extensions = {"pdf", "doc", "docx"}
    if not filename or "." not in filename:
        return False
    return filename.rsplit(".", 1)[-1].lower() in allowed_extensions

def secure_resume_filename(filename):
    return secure_filename(filename)

def valid_email(email):
    return bool(EMAIL_RE.match(email or ""))