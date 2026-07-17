import json
import time
from typing import Dict, Any
from ..crypto import hash_data

class Transaction:
    def __init__(self, sender: str, receiver: str, amount: float, signature: bytes = None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = time.time()
        self.signature = signature
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'timestamp': self.timestamp
        }
    
    def serialize(self) -> bytes:
        return json.dumps(self.to_dict(), sort_keys=True).encode()
    
    def hash(self) -> bytes:
        return hash_data(self.serialize())
    
    def sign(self, private_key) -> bytes:
        """Sign the transaction hash with the provided private key"""
        self.signature = private_key.sign(self.hash())
        return self.signature
    
    def verify(self, public_key) -> bool:
        """Verify the transaction signature with the provided public key"""
        if not self.signature:
            return False
        return public_key.verify(self.hash(), self.signature)