# ============================================================
#  Route: /api/subjects
#  Author: Rodrigo Garcia Martinez (2309091)
#
#  Supports: Diego's question — subject traffic by career program
# ============================================================

from flask import Blueprint, jsonify, request

subjects_bp = Blueprint("subjects", __name__)

# TODO (Rodrigo): Implement the following endpoints

@subjects_bp.route("/", methods=["GET"])
def get_subjects():
    # TODO: Return all subjects with view counts broken down by career
    # Needed for: Diego's traffic distribution analysis
    pass

@subjects_bp.route("/<int:subject_id>/stats", methods=["GET"])
def get_subject_stats(subject_id):
    # TODO: Return view proportion per career for a specific subject
    pass
