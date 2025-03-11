import hashlib
import base64
from typing import Tuple, Optional

class HashingUtil:
    # Supported hashing algorithms
    SUPPORTED_ALGORITHMS = {
        'SHA-256': hashlib.sha256,
        'SHA-512': hashlib.sha512
    }

    @staticmethod
    def generate_hash(data: str, algorithm: str) -> Tuple[Optional[str], str]:
        """
        Generate a hash for the given data using specified algorithm
        Returns: (base64_encoded_hash or None, message/algorithm_used)
        """
        try:
            # Validate algorithm
            if algorithm not in HashingUtil.SUPPORTED_ALGORITHMS:
                return {"hash_value": None, "error": f"Unsupported algorithm. Supported: {list(HashingUtil.SUPPORTED_ALGORITHMS.keys())}"}

            # Convert string data to bytes
            data_bytes = data.encode('utf-8')
            
            # Create hash object and generate hash
            hash_obj = HashingUtil.SUPPORTED_ALGORITHMS[algorithm](data_bytes)
            hash_bytes = hash_obj.digest()
            
            # Encode hash to base64
            hash_base64 = base64.b64encode(hash_bytes).decode('utf-8')
            
            return {"hash_value": hash_base64, "algorithm": algorithm}
            
        except Exception as e:
            return {"hash_value": None, "error": f"Hash generation failed: {str(e)}"}

    @staticmethod
    def verify_hash(data: str, hash_value: str, algorithm: str) -> Tuple[bool, str]:
        """
        Verify if the given hash matches the data
        Returns: (is_valid, message)
        """
        try:
            # Validate algorithm
            if algorithm not in HashingUtil.SUPPORTED_ALGORITHMS:
                return {"is_valid": None, "error": f"Unsupported algorithm. Supported: {list(HashingUtil.SUPPORTED_ALGORITHMS.keys())}"}

            # Generate new hash from input data
            new_hash = HashingUtil.generate_hash(data, algorithm).get("hash_value")
            result = HashingUtil.generate_hash(data, algorithm).get("error")
            
            # Check if hash generation failed
            if new_hash is None:
                return {"is_valid": False, "error": result}
            
            # Compare hashes
            is_valid = (new_hash == hash_value)
            print(is_valid)
            message = "Hash matches the data." if is_valid else "Hash does not match the data."
            return { "is_valid": is_valid, "message": message }
            
        except Exception as e:
            return {"is_valid": None, "error": f"Hash verification failed: {str(e)}"}