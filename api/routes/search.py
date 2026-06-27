# ============================================================
#  Route: /api/search
#  Author: Rodrigo Garcia Martinez (2309091)
#  Supports: Arturo — filter usage vs. search-to-click conversion
# ============================================================

from flask import Blueprint, jsonify, request
from controllers.base import get_db_connection

search_bp = Blueprint("search", __name__)


@search_bp.route("/", methods=["GET"])
def search_books():
    """Search books by title. Logs the search event with filter usage."""
    query = request.args.get("q", "")
    filter_used = request.args.get("filter_used", "false").lower() == "true"
    student_id = request.args.get("student_id", type=int)

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB connection failed"}), 500
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM books WHERE title ILIKE %s ORDER BY book_id LIMIT 50;",
        (f"%{query}%",)
    )
    results = cur.fetchall()

    # Log the search event (clicked defaults false; updated by /click)
    if student_id:
        cur.execute(
            "INSERT INTO search_events (student_id, query, filter_used, clicked, searched_at) "
            "VALUES (%s, %s, %s, FALSE, NOW()) RETURNING event_id;",
            (student_id, query, filter_used)
        )
        event_id = cur.fetchone()["event_id"]
        conn.commit()
    else:
        event_id = None

    cur.close(); conn.close()
    return jsonify({"event_id": event_id, "count": len(results), "results": results}), 200


@search_bp.route("/click", methods=["POST"])
def register_click():
    """Mark a search event as converted (clicked)."""
    data = request.get_json()
    if not data or "event_id" not in data:
        return jsonify({"error": "event_id is required"}), 400
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB connection failed"}), 500
    cur = conn.cursor()
    cur.execute("UPDATE search_events SET clicked = TRUE WHERE event_id = %s;",
                (data["event_id"],))
    conn.commit(); cur.close(); conn.close()
    return jsonify({"message": "Click registered"}), 200
