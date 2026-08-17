import os
import psycopg2


def get_db_connection():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL is not configured.")

    return psycopg2.connect(
        database_url,
        sslmode="require",
        connect_timeout=15,
        application_name="royals-webtech-backend"
    )