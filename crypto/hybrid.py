# new file: crypto/hybrid.py

from .falcon import Falcon
from .sphincs import SPHINCS

class HybridFalconSPHINCS:
    """
    A simulated hybrid cryptographic model combining Falcon and SPHINCS+.
    The `sign` and `verify` methods require both algorithms to be used.
    """
    def __init__(self):
        # Initialize both PQC algorithms
        self.falcon_signer = Falcon()
        self.sphincs_signer = SPHINCS()

    def sign(self, data):
        """
        Signs the data using both Falcon and SPHINCS+ and returns a combined signature.
        """
        # Sign the data with each algorithm
        falcon_sig = self.falcon_signer.sign(data)
        sphincs_sig = self.sphincs_signer.sign(data)
        
        # Combine the two signatures into one.
        # In a real implementation, this would be a carefully crafted structure.
        # Here, we'll simply concatenate them.
        return falcon_sig + b"|" + sphincs_sig

    def verify(self, data, signature):
        """
        Verifies the data against the combined signature.
        Both signatures must be valid for the verification to succeed.
        """
        # Split the combined signature
        if b"|" not in signature:
            return False
        
        falcon_sig, sphincs_sig = signature.split(b"|", 1)
        
        # Verify both signatures
        falcon_verified = self.falcon_signer.verify(data, falcon_sig)
        sphincs_verified = self.sphincs_signer.verify(data, sphincs_sig)
        
        # The signature is valid only if BOTH are valid
        return falcon_verified and sphincs_verified