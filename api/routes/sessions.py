# ============================================================
#  Route: /api/sessions
#  Author: Rodrigo Garcia Martinez (2309091)
#
#  Supports:
#  [Mau]   Session duration vs. distinct subjects visited
#  [Rodri] Browsing depth vs. save probability
# ============================================================

from flask import Blueprint, jsonify, request

sessions_bp = Blueprint("sessions", __name__)

# TODO (Rodrigo): Implement the following endpoints

@sessions_bp.route("/", methods=["POST"])
def start_session():
    # TODO: Create a new session record for a student
    pass

@sessions_bp.route("/<int:session_id>/end", methods=["PUT"])
def end_session(session_id):
    # TODO: Record session end time, calculate duration
    pass

@sessions_bp.route("/<int:session_id>/subjects", methods=["POST"])
def log_subject_visit(session_id):
    # TODO: Log a subject visited during the session
    # Needed for: Mau's subject count per session
    pass

@sessions_bp.route("/<int:session_id>/browse", methods=["POST"])
def log_book_browse(session_id):
    # TODO: Increment browsing depth counter for this session
    # Needed for: Rodri's browsing depth vs. save probability
    pass
