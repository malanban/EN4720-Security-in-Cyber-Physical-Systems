from flask import Blueprint, Flask, jsonify, request
import json
from Crypto.Cipher import AES
from api_database import APIDatabase
from cryptographic_functions import AES_Util, RSA_Util

crypto_api = Blueprint('crypto_api' ,__name__)

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
@crypto_api.route("/generate-key", methods = ["POST"])
def generateKey():
    arguments = parse_request()
    if arguments is None:
        return jsonify({"error": "Invalid request format. Expected JSON input."}), 400
    
    key_type = arguments.get("key_type")
    key_size = arguments.get("key_size")

    if not isinstance(key_type, str):
        return jsonify({"error": "Invalid key type. Expected a string value."}), 400
    elif key_type.upper() not in {"AES", "RSA"}:
        return jsonify({"error": "Unsupported key type. Choose either 'AES' or 'RSA'."}), 400
    else:
        key_type = key_type.upper()

    if (key_type == "AES") and (key_size in {128, 192, 256}):
        key_value_1 = AES_Util.generate_key(key_size)
        return jsonify(APIDatabase.insert_key(key_type, key_size, key_value_1)), 200
    
    elif (key_type == "RSA") and (key_size in {1024, 2048, 4096}):
        private_key, public_key = RSA_Util.generate_key_pair(key_size)
        return jsonify(APIDatabase.insert_key(key_type, key_size, public_key, private_key)), 200

    else:
        return jsonify({"error": "Invalid key size for the selected type. AES supports 128, 192, or 256 bits. RSA supports 1024, 2048, or 4096 bits."}), 400
   



# Encrypt-Message
@crypto_api.route("/encrypt", methods = ["POST"])
def encrypt():
    arguments = parse_request()
    if arguments is None:
        return jsonify({"error": "Invalid request format. Expected JSON input."}), 400

    key_id = arguments.get("key_id") 
    plaintext = arguments.get("plaintext")
    algorithm = arguments.get("algorithm")

    if (key_id is None) or (plaintext is None) or (algorithm is None):
        return jsonify({"error": "Missing required fields. Ensure 'key_id', 'plaintext', and 'algorithm' are provided."}), 400

    query_response = APIDatabase.get_key_by_id(key_id)

    if query_response.get("error") is not None:
        return jsonify(query_response), 400

    query_key_type = query_response["key_type"]
    query_key_size = query_response["key_size"]
    query_key_value_1 = query_response["key_value_1"]
    query_key_value_2 = query_response["key_value_2"]

    if query_key_type != algorithm.upper():
        return jsonify({"error": f"KeyID_Type-{query_key_type} and Algorithm-{algorithm} Mismatch"}), 400

    if query_key_type == "AES":
        return jsonify({"ciphertext": AES_Util.encrypt_text(plaintext, query_key_value_1)}), 200
    elif query_key_type == "RSA":
        return jsonify({"ciphertext": RSA_Util.encrypt_text(plaintext, query_key_value_1)}), 200



# Decrypt-Message
@crypto_api.route("/decrypt", methods = ["POST"])
def decrypt():
    arguments = parse_request()
    if arguments is None:
        return jsonify({"error": "Invalid request format. Expected JSON input."}), 400
    
    key_id = arguments.get("key_id")
    ciphertext = arguments.get("ciphertext")
    algorithm = arguments.get("algorithm")

    if (key_id is None) or (ciphertext is None) or (algorithm is None):
        return jsonify({"error": "Missing required fields. Ensure 'key_id', 'ciphertext' and 'algorithm' are provided."}), 400

    query_response = APIDatabase.get_key_by_id(key_id)

    if query_response.get("error") is not None:
        return jsonify(query_response), 400

    query_key_type = query_response["key_type"]
    query_key_size = query_response["key_size"]
    query_key_value_1 = query_response["key_value_1"]
    query_key_value_2 = query_response["key_value_2"]

    if query_key_type != algorithm.upper():
        return jsonify({"error": f"KeyID_Type-{query_key_type} and Algorithm-{algorithm} Mismatch"}), 400
    
    if query_key_type == "AES":
        plaintext, error = AES_Util.decrypt_text(ciphertext, query_key_value_1)
    elif query_key_type == "RSA":
        plaintext, error = RSA_Util.decrypt_text(ciphertext, query_key_value_2)
    
    if plaintext is not None:
        return jsonify({"plaintext": plaintext}), 200
    else:
        return jsonify({"error": error}), 400

