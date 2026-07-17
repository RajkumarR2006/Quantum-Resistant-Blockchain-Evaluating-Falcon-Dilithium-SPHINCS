import time
import statistics
from ..crypto import RSA, ECC, Dilithium

def run_benchmark():
    algorithms = [
        ("RSA-2048", RSA),
        ("ECC-256", ECC),
        ("Dilithium", Dilithium)
    ]
    
    print("Performance Comparison")
    print("=" * 50)
    print(f"{'Algorithm':<12} | {'Key Gen (ms)':>12} | {'Sign (ms)':>10} | {'Verify (ms)':>10}")
    print("-" * 50)
    
    for name, algo_class in algorithms:
        # Key generation
        start = time.time()
        crypto = algo_class()
        keygen_time = (time.time() - start) * 1000
        
        # Sign/verify test
        data = b"test_message"
        
        # Signing
        start = time.time()
        sig = crypto.sign(data)
        sign_time = (time.time() - start) * 1000
        
        # Verification
        start = time.time()
        valid = crypto.verify(data, sig)
        verify_time = (time.time() - start) * 1000
        
        if not valid:
            print(f"WARNING: Verification failed for {name}")
        
        print(f"{name:<12} | {keygen_time:>12.2f} | {sign_time:>10.2f} | {verify_time:>10.2f}")

if __name__ == "__main__":
    run_benchmark()