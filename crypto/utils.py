from Crypto.Hash import SHA3_256

def hash_data(data: bytes) -> bytes:
    h = SHA3_256.new()
    h.update(data)
    return h.digest()

def bytes_to_int(b: bytes) -> int:
    return int.from_bytes(b, 'big')

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')