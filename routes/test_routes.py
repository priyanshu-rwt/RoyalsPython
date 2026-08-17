from flask import Blueprint, jsonify
from database.connection import get_db_connection

test_bp = Blueprint("test", __name__)

@test_bp.route("/api/test-db", methods=["GET"])
def test_db():
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()[0]
        return jsonify({"success": True, "message": "Database connected successfully", "result": result})
    except Exception as exc:
        print("DATABASE ERROR:", repr(exc))
        return jsonify({"success": False, "message": "Database connection failed"}), 500
    finally:
        if conn:
            conn.close()
