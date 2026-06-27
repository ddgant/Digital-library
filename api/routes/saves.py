# ============================================================
#  Route: /api/saves
#  Author: Rodrigo Garcia Martinez (2309091)
#  Supports: Rodri — browsing depth vs. save probability
# ============================================================

from flask import Blueprint, jsonify, request
from controllers.base import get_db_connection

saves_bp = Blueprint("saves", __name__)


@saves_bp.route("/", methods=["GET"])
def get_saves():
    student_id = request.args.get("student_id", type=int)
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB connection failed"}), 500
    cur = conn.cursor()
    if student_id:
        cur.execute(
            "SELECT sb.*, b.title FROM saved_books sb "
            "JOIN books b ON sb.book_id = b.book_id "
            "WHERE sb.student_id = %s ORDER BY sb.saved_at DESC;", (student_id,)
        )
    else:
        cur.execute(
            "SELECT sb.*, b.title FROM saved_books sb "
            "JOIN books b ON sb.book_id = b.book_id ORDER BY sb.saved_at DESC LIMIT 100;"
        )
    rows = cur.fetchall()
    cur.close(); conn.close()
    return jsonify(rows), 200


@saves_bp.route("/", methods=["POST"])
def save_book():
    data = request.get_json() or {}
    required = ["student_id", "book_id", "browsing_depth_at_save"]
    if not all(k in data for k in required):
        return jsonify({"error": f"Required: {required}"}), 400
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB connection failed"}), 500
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO saved_books (student_id, book_id, browsing_depth_at_save, saved_at) "
        "VALUES (%s, %s, %s, NOW()) "
        "ON CONFLICT (student_id, book_id) DO NOTHING RETURNING save_id;",
        (data["student_id"], data["book_id"], data["browsing_depth_at_save"])
    )
    row = cur.fetchone()
    conn.commit(); cur.close(); conn.close()
    return jsonify({"message": "Book saved", "save_id": row["save_id"] if row else None}), 201
