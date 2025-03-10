import os
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


class AES_Util:
    @staticmethod
    def generate_key(key_size: int) -> str:
        """
        Generates a random AES key of the given size and returns it as a Base64-encoded string..
        """
        if key_size not in {128, 192, 256}:
            return ("Key size must be 128, 192, or 256 bits.")
        
        key_bytes = key_size // 8  # Convert bits to bytes
        key = os.urandom(key_bytes)  # Generate a random key
        return base64.b64encode(key).decode('utf-8')
    
    @staticmethod
    def encrypt_text(plain_text: str, base64_key: str) -> str:
        """
        Encrypts plaintext using AES encryption.
        """
        key = base64.b64decode(base64_key)
        cipher = AES.new(key, AES.MODE_ECB)  # Using ECB mode (consider using CBC for better security)
        padded_text = pad(plain_text.encode(), AES.block_size)
        encrypted_bytes = cipher.encrypt(padded_text)
        return base64.b64encode(encrypted_bytes).decode('utf-8')
    
    @staticmethod
    def decrypt_text(encrypted_text: str, base64_key: str) -> str:
        """
        Decrypts AES-encrypted text.
        """
        key = base64.b64decode(base64_key)
        cipher = AES.new(key, AES.MODE_ECB)
        encrypted_bytes = base64.b64decode(encrypted_text)
        decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
        return decrypted_bytes.decode('utf-8')


class RSA_Util:
    @staticmethod
    def generate_key_pair(key_size: int = 2048) -> tuple[str, str]:
        """
        Generates an RSA key pair and returns Base64-encoded private and public keys.
        """
        key = RSA.generate(key_size)
        private_key = base64.b64encode(key.export_key()).decode('utf-8')
        public_key = base64.b64encode(key.publickey().export_key()).decode('utf-8')
        return private_key, public_key
    
    @staticmethod
    def encrypt_text(plain_text: str, base64_public_key: str) -> str:
        """
        Encrypts plaintext using RSA encryption.
        """
        public_key = RSA.import_key(base64.b64decode(base64_public_key))
        cipher = PKCS1_OAEP.new(public_key)
        encrypted_bytes = cipher.encrypt(plain_text.encode())
        return base64.b64encode(encrypted_bytes).decode('utf-8')
    
    @staticmethod
    def decrypt_text(encrypted_text: str, base64_private_key: str) -> str:
        """
        Decrypts RSA-encrypted text.
        """
        private_key = RSA.import_key(base64.b64decode(base64_private_key))
        cipher = PKCS1_OAEP.new(private_key)
        encrypted_bytes = base64.b64decode(encrypted_text)
        decrypted_bytes = cipher.decrypt(encrypted_bytes)
        return decrypted_bytes.decode('utf-8')
