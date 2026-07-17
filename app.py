from blockchain import Blockchain
from crypto import RSA, Dilithium

def demo():
    # Create blockchain
    blockchain = Blockchain()
    
    # Create crypto instances
    rsa = RSA()
    dilithium = Dilithium()
    
    # Create and add transactions
    tx1 = Transaction("Alice", "Bob", 10)
    tx1.sign(rsa)
    blockchain.add_transaction(tx1)
    
    tx2 = Transaction("Bob", "Charlie", 5)
    tx2.sign(dilithium)
    blockchain.add_transaction(tx2)
    
    # Mine block
    blockchain.mine_pending_transactions()
    
    # Verify chain
    print(f"Blockchain valid: {blockchain.is_chain_valid()}")
    print(f"Blockchain length: {len(blockchain.chain)}")

if __name__ == "__main__":
    demo()