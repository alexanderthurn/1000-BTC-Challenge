import hashlib
import base58

def decimal_to_wif(private_key_decimal, compressed=True):
    # Convert the private key from decimal to bytes
    private_key_bytes = private_key_decimal.to_bytes(32, byteorder='big')
    
    # Add the wallet prefix (0x80 for Bitcoin)
    prefix = b'\x80'
    prefixed_key = prefix + private_key_bytes
    
    # For compressed public keys, append 0x01 at the end
    if compressed:
        prefixed_key += b'\x01'
    
    # Generate the checksum by double SHA-256 hashing
    hash_once = hashlib.sha256(prefixed_key).digest()
    hash_twice = hashlib.sha256(hash_once).digest()
    checksum = hash_twice[:4]  # The first four bytes of the checksum
    
    # Add the checksum and encode everything in Base58
    full_key = prefixed_key + checksum
    wif_key = base58.b58encode(full_key).decode('utf-8')
    
    return wif_key
