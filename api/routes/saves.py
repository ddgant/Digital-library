# ============================================================
#  Route: /api/saves
#  Author: Rodrigo Garcia Martinez (2309091)
#
#  Supports: Rodrigo's question — browsing depth vs. save probability
# ============================================================

from flask import Blueprint, jsonify, request

saves_bp = Blueprint("saves", __name__)

# TODO (Rodrigo): Implement the following endpoints

@saves_bp.route("/", methods=["POST"])
def save_book():
    # TODO: Save a book for a student, log browsing_depth at moment of save
    pass

@saves_bp.route("/", methods=["GET"])
def get_saved_books():
    # TODO: Return all saved books for a student
    pass
