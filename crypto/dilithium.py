import random
from .utils import hash_data, bytes_to_int

class Dilithium:
    def __init__(self, n=96, q=251):
        self.n = n  # Larger dimension for security
        self.q = q
        self.sk = [random.randint(0, q-1) for _ in range(n)]
        self.pk = [(x * 3) % q for x in self.sk]  # Public key
    
    def sign(self, data: bytes) -> bytes:
        h = bytes_to_int(hash_data(data)) % self.q
        c = [random.randint(0, self.q) for _ in range(self.n)]
        z = [(s * h + c_i) % self.q for s, c_i in zip(self.sk, c)]
        return bytes([x % 256 for x in z])
    
    def verify(self, data: bytes, signature: bytes) -> bool:
        h = bytes_to_int(hash_data(data)) % self.q
        z = list(signature)
        lhs = [(p * h) % self.q for p in self.pk]
        rhs = [zi % self.q for zi in z]
        return lhs == rhs