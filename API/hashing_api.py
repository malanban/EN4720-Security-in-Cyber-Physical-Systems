from flask import Flask, jsonify, request
from Crypto.Cipher import AES

app = Flask(__name__)

# Generate-HASH value
@app.route("/generate-hash", methods = ["POST"])
def generateHash():
    arguments = request.get_json()
    
    data = arguments.get("data")
    algorithm = arguments.get("algorithm")

    return jsonify({
        "data" : data,
        "algorithm" : algorithm
    }), 200
    
# Verify-HASH value
@app.route("/verify-hash", methods = ["POST"])
def verifyHash():
    arguments = request.get_json()

    data = arguments.get("data")
    hash_value = arguments.get("hash_value")
    algorithm = arguments.get("algorithm")

    return jsonify({
        "data" : data,
        "hash_value" : hash_value,
        "algorithm" : algorithm
    }), 200
    

if __name__ == "__main__" :
    app.run(debug=True)
