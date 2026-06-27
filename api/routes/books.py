# ============================================================
#  Route: /api/books
#  Author: Rodrigo Garcia Martinez (2309091)
# ============================================================

from flask import Blueprint, jsonify, request

books_bp = Blueprint("books", __name__)

# TODO (Rodrigo): Implement the following endpoints

@books_bp.route("/", methods=["GET"])
def get_books():
    # TODO: Return paginated book catalog
    # Support filter by subject, career, tag count
    pass

@books_bp.route("/<int:book_id>", methods=["GET"])
def get_book(book_id):
    # TODO: Return book detail + log a view event in book_views
    pass

@books_bp.route("/", methods=["POST"])
def create_book():
    # TODO: Create a new book record
    pass
