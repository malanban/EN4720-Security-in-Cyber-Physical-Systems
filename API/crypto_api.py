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

# Generate-Key
@app.route("/generate-key", methods = ["POST"])
def generateKey():
    arguments = parse_request()
    if arguments is None:
        return jsonify({"error": "Invalid JSON format"}), 400
    
    key_type = arguments.get("key_type")
    key_size = arguments.get("key_size")

    return jsonify({
        "key_type" : key_type,
        "key_size" : key_size
    }), 200

# Encrypt-Message
@app.route("/encrypt", methods = ["POST"])
def encrypt():
    arguments = parse_request()
    if arguments is None:
        return jsonify({"error": "Invalid JSON format"}), 400

    key_id = arguments.get("key_id") 
    plaintext = arguments.get("plaintext")
    algorithm = arguments.get("algorithm")


    return jsonify({
        "key_id" : key_id,
        "plaintext" : plaintext,
        "algorithm" : algorithm
    }), 200

# Decrypt-Message
@app.route("/decrypt", methods = ["POST"])
def decrypt():
    arguments = parse_request()
    if arguments is None:
        return jsonify({"error": "Invalid JSON format"}), 400
    
    key_id = arguments.get("key_id")
    ciphertext = arguments.get("ciphertext")
    algorithm = arguments.get("algorithm")
    
    return jsonify({
        "key_id" : key_id,
        "ciphertext" : ciphertext,
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

if __name__ == "__main__":
    app.run(debug=True)
