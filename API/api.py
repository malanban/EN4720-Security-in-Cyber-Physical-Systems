from flask import Flask, jsonify
from crypto_api import crypto_api
from hashing_api import hashing_api

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(crypto_api)
app.register_blueprint(hashing_api)

# Handle unknown routes (404)
@app.errorhandler(404)
def handle_404(error):
    return jsonify({"error": "Not Found", "message": "The requested endpoint does not exist.", "status": 404}), 404

# Handle unsupported HTTP methods
@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method Not Allowed", "message": "Use a valid HTTP method"}), 405

if __name__ == "__main__":
    app.run(debug=True)
