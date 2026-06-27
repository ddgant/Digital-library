# ============================================================
#  TeamX Digital Library Platform — API Entry Point
#  Author: Rodrigo Garcia Martinez (2309091)
#  Role:   API Design
# ============================================================

from flask import Flask, jsonify
from flask_cors import CORS

# TODO (Rodrigo): Import and register all route blueprints
# from routes.books    import books_bp
# from routes.search   import search_bp
# from routes.sessions import sessions_bp
# from routes.saves    import saves_bp
# from routes.subjects import subjects_bp

app = Flask(__name__)
CORS(app)

# TODO: Register blueprints here

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "platform": "TeamX Digital Library"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
