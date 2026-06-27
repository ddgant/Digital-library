# ============================================================
#  TeamX Digital Library Platform — API Entry Point
#  Author: Rodrigo Garcia Martinez (2309091)
#  Role:   API Design
# ============================================================

from flask import Flask, jsonify
from flask_cors import CORS
import os

from routes.books    import books_bp
from routes.search   import search_bp
from routes.sessions import sessions_bp
from routes.saves    import saves_bp
from routes.subjects import subjects_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(books_bp,    url_prefix="/api/books")
app.register_blueprint(search_bp,   url_prefix="/api/search")
app.register_blueprint(sessions_bp, url_prefix="/api/sessions")
app.register_blueprint(saves_bp,    url_prefix="/api/saves")
app.register_blueprint(subjects_bp, url_prefix="/api/subjects")


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "platform": "TeamX Digital Library"}), 200


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV", "development") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)
