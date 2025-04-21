import os
import time
import random
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class Entity:
    def __init__(self, id_name, key):
        self.id = id_name
        self.key = key
        self.session_keys = {}
        self.timestamps = {}
        self.nonces = {}

    def encrypt(self, key, data):
        iv = os.urandom(16)  # Initialization vector for AES
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # Pad data using PKCS#7
        padded_data = pad(data, AES.block_size)
        ciphertext = cipher.encrypt(padded_data)

        return base64.b64encode(iv + ciphertext)

    def decrypt(self, key, encrypted_data):
        encrypted_data = base64.b64decode(encrypted_data)
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]

        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_plaintext = cipher.decrypt(ciphertext)

        # Remove padding
        try:
            return unpad(padded_plaintext, AES.block_size)
        except ValueError:
            # If unpadding fails, return stripped data (for handling potential padding issues)
            return padded_plaintext.rstrip(b' \t\r\n\0')

    def generate_nonce(self):
        return random.randint(1000000, 9999999)

    def get_timestamp(self):
        return int(time.time())
