from Crypto.PublicKey import RSA as PyCryptoRSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA3_256
from .utils import hash_data

class RSA:
    def __init__(self, key_size=2048):
        self.key = PyCryptoRSA.generate(key_size)
        self.private_key = self.key
        self.public_key = self.key.publickey()
    
    def sign(self, data: bytes) -> bytes:
        h = SHA3_256.new(data)
        signature = pkcs1_15.new(self.private_key).sign(h)
        return signature
    
    def verify(self, data: bytes, signature: bytes) -> bool:
        h = SHA3_256.new(data)
        try:
            pkcs1_15.new(self.public_key).verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False