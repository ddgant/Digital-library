# ============================================================
#  Route: /api/search
#  Author: Rodrigo Garcia Martinez (2309091)
#
#  Supports: Arturo's question — filter usage vs. conversion rate
# ============================================================

from flask import Blueprint, jsonify, request

search_bp = Blueprint("search", __name__)

# TODO (Rodrigo): Implement the following endpoints

@search_bp.route("/", methods=["GET"])
def search_books():
    # TODO: Full-text search across books
    # Log event to search_events: query, filter_used (bool), student_id
    # Needed for: Arturo's conversion rate analysis
    pass

@search_bp.route("/click", methods=["POST"])
def register_click():
    # TODO: Mark a search result as clicked (conversion event)
    pass
