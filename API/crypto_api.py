from flask import Flask, jsonify, request
from Crypto.Cipher import AES

app = Flask(__name__)

# Generate-Key
@app.route("/generate-key", methods = ["POST"])
def generateKey():
    data = request.get_json()

    key_type = data.get("key_type")
    key_size = data.get("key_size")

    return jsonify({
        "key_type" : key_type,
        "key_size" : key_size
    }), 200

# Encrypt-Message
@app.route("/encrypt", methods = ["POST"])
def encrypt():
    data = request.get_json()

    key_id = data.get("key_id") 
    plaintext = data.get("plaintext")
    algorithm = data.get("algorithm")


    return jsonify({
        "key_id" : key_id,
        "plaintext" : plaintext,
        "algorithm" : algorithm
    }), 200

# Decrypt-Message
@app.route("/decrypt", methods = ["POST"])
def decrypt():
    data = request.get_json()
    
    key_id = data.get("key_id")
    ciphertext = data.get("ciphertext")
    algorithm = data.get("algorithm")
    
    return jsonify({
        "key_id" : key_id,
        "ciphertext" : ciphertext,
        "algorithm" : algorithm
    }), 200

if __name__ == "__main__":
    app.run(debug=True)
