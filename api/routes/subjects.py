# ============================================================
#  Route: /api/subjects
#  Author: Rodrigo Garcia Martinez (2309091)
#  Supports: Diego — subject traffic by career program
# ============================================================

from flask import Blueprint, jsonify, request
from controllers.base import get_db_connection

subjects_bp = Blueprint("subjects", __name__)


@subjects_bp.route("/", methods=["GET"])
def get_subjects():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB connection failed"}), 500
    cur = conn.cursor()
    cur.execute("SELECT * FROM subjects ORDER BY subject_id;")
    rows = cur.fetchall()
    cur.close(); conn.close()
    return jsonify(rows), 200


@subjects_bp.route("/<int:subject_id>/stats", methods=["GET"])
def subject_stats(subject_id):
    """Return view counts for this subject broken down by career."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB connection failed"}), 500
    cur = conn.cursor()
    cur.execute(
        "SELECT bv.career, COUNT(*) AS views "
        "FROM book_views bv "
        "JOIN book_subjects bs ON bv.book_id = bs.book_id "
        "WHERE bs.subject_id = %s "
        "GROUP BY bv.career ORDER BY views DESC;", (subject_id,)
    )
    rows = cur.fetchall()
    cur.close(); conn.close()
    return jsonify({"subject_id": subject_id, "by_career": rows}), 200
