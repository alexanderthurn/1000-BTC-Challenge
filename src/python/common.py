import base58, binascii, hashlib
from ecdsa import SigningKey, SECP256k1

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

def number_to_hex_private_key(number):
    hex_string = hex(number)[2:]
    hex_string_padded = hex_string.zfill(64)
    return hex_string_padded

def hex_private_key_to_hex_public_key(hex_private_key):
    private_key_bytes = binascii.unhexlify(hex_private_key)
    sk = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
    vk = sk.verifying_key
    public_key_hex = binascii.hexlify(vk.to_string("compressed")).decode("utf-8")
    return public_key_hex

def hex_public_key_to_bitcoin_address(public_key_hex):
    public_key_bytes = binascii.unhexlify(public_key_hex)
    sha256_hash = hashlib.sha256(public_key_bytes).digest()
    ripemd160_hash = hashlib.new('ripemd160')
    ripemd160_hash.update(sha256_hash)
    network_byte = b'\x00'
    network_and_ripemd160 = network_byte + ripemd160_hash.digest()
    double_sha256 = hashlib.sha256(hashlib.sha256(network_and_ripemd160).digest()).digest()
    checksum = double_sha256[:4]
    binary_address = network_and_ripemd160 + checksum
    bitcoin_address = base58.b58encode(binary_address).decode('utf-8')
    return bitcoin_address
