import time

class SPHINCS:
    def __init__(self, key_size='128f'):
        # In a real implementation, this would generate public and private keys.
        # We'll use a simulated delay to mimic the key generation time.
        # SPHINCS+ key generation is very fast, so we'll use a small value.
        time.sleep(0.0001)  # Simulate a 0.1 ms key generation
        self.key_size = key_size
        self.public_key = b"mock_public_key"
        self.private_key = b"mock_private_key"

    def sign(self, data):
        # In a real implementation, this would perform the signing operation.
        # SPHINCS+ signing is relatively slow.
        if self.key_size == '128f':
            time.sleep(0.005)  # Simulate a 5 ms signing delay
        else:
            time.sleep(0.01)  # Simulate a 10 ms delay for larger keys
        return b"mock_signature_for_" + data

    def verify(self, data, signature):
        # In a real implementation, this would perform the verification operation.
        # SPHINCS+ verification is much faster than signing.
        if self.key_size == '128f':
            time.sleep(0.0005)  # Simulate a 0.5 ms verification delay
        else:
            time.sleep(0.001)  # Simulate a 1 ms delay for larger keys
        return True