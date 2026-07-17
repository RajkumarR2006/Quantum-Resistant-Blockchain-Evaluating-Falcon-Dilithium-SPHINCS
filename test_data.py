# test_data.py

import random, string, json

def random_transaction():
    return {
        "sender": ''.join(random.choices(string.ascii_uppercase, k=5)),
        "receiver": ''.join(random.choices(string.ascii_uppercase, k=5)),
        "amount": round(random.uniform(1, 1000), 2)
    }

def generate_transactions(n=100):
    return [random_transaction() for _ in range(n)]

if __name__ == "__main__":
    txs = generate_transactions(100)
    with open("tests/test_transactions.json", "w") as f:
        json.dump(txs, f, indent=2)
