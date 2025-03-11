from flask import Blueprint, Flask, jsonify, request
import json
from Crypto.Cipher import AES
from hashing_functions import HashingUtil

hashing_api = Blueprint('hashing_api' ,__name__)

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
@hashing_api.route("/generate-hash", methods = ["POST"])
def generateHash():
    arguments = parse_request()
    if arguments is None:
        return jsonify({"error": "Invalid JSON format"}), 400
    
    data = arguments.get("data")
    algorithm = arguments.get("algorithm")

    if (data is None) or (algorithm is None):
        return jsonify({"error": "Invalid Input Request"}), 400
    
    algorithm = algorithm.upper()

    return jsonify(HashingUtil.generate_hash(data, algorithm)), 200
    
# Verify-HASH value
@hashing_api.route("/verify-hash", methods = ["POST"])
def verifyHash():
    arguments = parse_request()
    if arguments is None:
        return jsonify({"error": "Invalid JSON format"}), 400

    data = arguments.get("data")
    hash_value = arguments.get("hash_value")
    algorithm = arguments.get("algorithm")

    if (data is None) or (hash_value is None) or (algorithm is None):
        return jsonify({"error": "Invalid Inuput Request"}), 400
    
    algorithm = algorithm.upper()

    return jsonify(HashingUtil.verify_hash(data, hash_value, algorithm)), 200
