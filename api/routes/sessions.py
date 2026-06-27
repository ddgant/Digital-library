# ============================================================
#  Route: /api/sessions
#  Author: Rodrigo Garcia Martinez (2309091)
#  Supports: Mau (duration vs subjects), Rodri (depth vs save)
# ============================================================

from flask import Blueprint, jsonify, request
from controllers.base import get_db_connection

sessions_bp = Blueprint("sessions", __name__)


@sessions_bp.route("/", methods=["POST"])
def start_session():
    data = request.get_json() or {}
    if "student_id" not in data:
        return jsonify({"error": "student_id is required"}), 400
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB connection failed"}), 500
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO sessions (student_id, started_at, ended_at, duration_minutes) "
        "VALUES (%s, NOW(), NOW(), 0) RETURNING session_id;",
        (data["student_id"],)
    )
    sid = cur.fetchone()["session_id"]
    conn.commit(); cur.close(); conn.close()
    return jsonify({"message": "Session started", "session_id": sid}), 201


@sessions_bp.route("/<int:session_id>/end", methods=["PUT"])
def end_session(session_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB connection failed"}), 500
    cur = conn.cursor()
    cur.execute(
        "UPDATE sessions SET ended_at = NOW(), "
        "duration_minutes = EXTRACT(EPOCH FROM (NOW() - started_at))/60 "
        "WHERE session_id = %s;", (session_id,)
    )
    conn.commit(); cur.close(); conn.close()
    return jsonify({"message": "Session ended"}), 200


@sessions_bp.route("/<int:session_id>/subjects", methods=["POST"])
def log_subject(session_id):
    data = request.get_json() or {}
    if "subject_id" not in data:
        return jsonify({"error": "subject_id is required"}), 400
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB connection failed"}), 500
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO session_subjects (session_id, subject_id) VALUES (%s, %s) "
        "ON CONFLICT DO NOTHING;", (session_id, data["subject_id"])
    )
    conn.commit(); cur.close(); conn.close()
    return jsonify({"message": "Subject logged"}), 200


@sessions_bp.route("/<int:session_id>/browse", methods=["POST"])
def increment_browse(session_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB connection failed"}), 500
    cur = conn.cursor()
    cur.execute(
        "UPDATE sessions SET books_browsed = books_browsed + 1 WHERE session_id = %s;",
        (session_id,)
    )
    conn.commit(); cur.close(); conn.close()
    return jsonify({"message": "Browse counter incremented"}), 200
