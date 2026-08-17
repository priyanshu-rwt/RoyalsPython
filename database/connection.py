import os
import psycopg2
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

def _prepare_database_url(url: str) -> str:
    """Prepare a Supabase/Postgres URL for psycopg2.

    Render is IPv4-oriented, so use Supabase's Session Pooler connection
    string (port 5432) for the DATABASE_URL. We also explicitly disable
    prepared statements if a transaction-pooler URL is supplied.
    """
    parts = urlparse(url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    if parts.port == 6543:
        # Supavisor transaction mode does not support prepared statements.
        query.setdefault("prepare_threshold", "0")
    return urlunparse(parts._replace(query=urlencode(query)))

def get_db_connection():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not configured.")

    return psycopg2.connect(
        _prepare_database_url(database_url),
        sslmode=os.getenv("DB_SSLMODE", "require"),
        connect_timeout=10,
        application_name="royals-webtech-backend",
    )
