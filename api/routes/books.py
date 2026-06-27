# ============================================================
#  Route: /api/books
#  Author: Rodrigo Garcia Martinez (2309091)
# ============================================================

from flask import Blueprint, jsonify, request
from controllers.base import get_db_connection

books_bp = Blueprint("books", __name__)


@books_bp.route("/", methods=["GET"])
def get_books():
    """List books, optionally filtered by subject."""
    subject = request.args.get("subject")
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB connection failed"}), 500
    cur = conn.cursor()
    if subject:
        cur.execute(
            "SELECT b.* FROM books b "
            "JOIN book_subjects bs ON b.book_id = bs.book_id "
            "JOIN subjects s ON bs.subject_id = s.subject_id "
            "WHERE s.name = %s ORDER BY b.book_id;", (subject,)
        )
    else:
        cur.execute("SELECT * FROM books ORDER BY book_id LIMIT 100;")
    rows = cur.fetchall()
    cur.close(); conn.close()
    return jsonify(rows), 200


@books_bp.route("/<int:book_id>", methods=["GET"])
def get_book(book_id):
    """Get book detail and log a view event."""
    student_id = request.args.get("student_id", type=int)
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB connection failed"}), 500
    cur = conn.cursor()
    cur.execute("SELECT * FROM books WHERE book_id = %s;", (book_id,))
    book = cur.fetchone()
    if not book:
        cur.close(); conn.close()
        return jsonify({"error": "Book not found"}), 404

    # Log the view (needed for Diego's & Rous's questions)
    if student_id:
        cur.execute("SELECT career FROM students WHERE student_id = %s;", (student_id,))
        stu = cur.fetchone()
        if stu:
            cur.execute(
                "INSERT INTO book_views (book_id, student_id, career, viewed_at) "
                "VALUES (%s, %s, %s, NOW());",
                (book_id, student_id, stu["career"])
            )
            conn.commit()
    cur.close(); conn.close()
    return jsonify(book), 200


@books_bp.route("/", methods=["POST"])
def create_book():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "title is required"}), 400
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB connection failed"}), 500
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO books (title, author, year, description) "
        "VALUES (%s, %s, %s, %s) RETURNING book_id;",
        (data["title"], data.get("author"), data.get("year"), data.get("description"))
    )
    new_id = cur.fetchone()["book_id"]
    conn.commit(); cur.close(); conn.close()
    return jsonify({"message": "Book created", "book_id": new_id}), 201
