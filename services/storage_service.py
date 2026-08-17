import os
import uuid
from supabase import create_client

def _client():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are required.")
    return create_client(url, key)

def upload_resume(filename, data, content_type):
    bucket = os.getenv("SUPABASE_BUCKET", "resumes")
    storage_path = f"{uuid.uuid4().hex}_{filename}"
    _client().storage.from_(bucket).upload(
        storage_path, data,
        {"content-type": content_type or "application/octet-stream", "upsert": "false"}
    )
    return bucket, storage_path

def delete_file(bucket, storage_path):
    try:
        _client().storage.from_(bucket).remove([storage_path])
    except Exception as exc:
        print("Storage cleanup failed:", repr(exc))
