from flask import Flask, jsonify, request
import json
from Crypto.Cipher import AES

app = Flask(__name__)

def parse_request():
    """Function to handle JSON and raw text request body parsing."""
    try:
        if request.is_json:
            return request.get_json()
        else:
            raw_text = request.data.decode("utf-8").strip()
            return json.loads(raw_text)
    except json.JSONDecodeError:
        return None

# Generate-HASH value
@app.route("/generate-hash", methods = ["POST"])
def generateHash():
    arguments = parse_request()
    if arguments is None:
        return jsonify({"error": "Invalid JSON format"}), 400
    
    data = arguments.get("data")
    algorithm = arguments.get("algorithm")

    return jsonify({
        "data" : data,
        "algorithm" : algorithm
    }), 200
    
# Verify-HASH value
@app.route("/verify-hash", methods = ["POST"])
def verifyHash():
    arguments = parse_request()
    if arguments is None:
        return jsonify({"error": "Invalid JSON format"}), 400

    data = arguments.get("data")
    hash_value = arguments.get("hash_value")
    algorithm = arguments.get("algorithm")

    return jsonify({
        "data" : data,
        "hash_value" : hash_value,
        "algorithm" : algorithm
    }), 200

# Handle unsupported HTTP methods
@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method Not Allowed", "message": "Use a valid HTTP method"}), 405

# Handle unknown routes
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found", "message": "Invalid API endpoint"}), 404
    

if __name__ == "__main__" :
    app.run(debug=True)
