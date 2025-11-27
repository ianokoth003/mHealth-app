from flask import Flask, jsonify
from flask_cors import CORS
from utils.db import init_db

# Import Blueprints
from routes.auth import auth_bp
from routes.patients import patients_bp

app = Flask(__name__)
app.url_map.strict_slashes = False
# Apply CORS explicitly for API routes to ensure Access-Control-Allow-Origin
# headers are returned for all /api/* responses and during redirects.
# Apply CORS globally so both API and non-API routes return CORS headers.
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Initialize MongoDB
init_db(app)

@app.route("/")
def home():
    return jsonify({"message": "Backend running"})

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(patients_bp, url_prefix="/api/patients")

if __name__ == "__main__":
    print("🚀 Starting Flask backend...")
    app.run(host="0.0.0.0", port=5000, debug=False)

