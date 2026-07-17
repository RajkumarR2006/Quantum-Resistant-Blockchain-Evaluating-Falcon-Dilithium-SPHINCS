from Crypto.PublicKey import ECC as CryptoECC
from Crypto.Signature import eddsa
from .utils import hash_data

class ECC:
    def __init__(self):
        self.key = CryptoECC.generate(curve='ed25519')
        self.private_key = self.key
        self.public_key = self.key.public_key()
    
    def sign(self, data: bytes) -> bytes:
        h = hash_data(data)
        signer = eddsa.new(self.private_key, 'rfc8032')
        return signer.sign(h)
    
    def verify(self, data: bytes, signature: bytes) -> bool:
        h = hash_data(data)
        verifier = eddsa.new(self.public_key, 'rfc8032')
        try:
            verifier.verify(h, signature)
            return True
        except ValueError:
            return False