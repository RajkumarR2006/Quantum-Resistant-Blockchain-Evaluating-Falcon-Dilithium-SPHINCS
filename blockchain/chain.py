from typing import List
from .block import Block
from .transaction import Transaction
from ..crypto import hash_data

class Blockchain:
    def __init__(self, difficulty: int = 2):
        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self.difficulty = difficulty
        self.create_genesis_block()
    
    def create_genesis_block(self):
        genesis_block = Block(0, [], "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
    
    def get_last_block(self) -> Block:
        return self.chain[-1]
    
    def add_transaction(self, transaction: Transaction):
        self.pending_transactions.append(transaction)
    
    def mine_pending_transactions(self):
        if not self.pending_transactions:
            return False
        
        last_block = self.get_last_block()
        new_block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            previous_hash=last_block.hash
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.pending_transactions = []
        return True
    
    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            if current_block.hash != current_block.calculate_hash():
                return False
            
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True