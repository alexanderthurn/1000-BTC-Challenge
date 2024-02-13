import base58, binascii, hashlib
from ecdsa import SigningKey, SECP256k1
from python.addresses import btcadresses

def number_to_hex_private_key(number):
    # Convert the number to a hex string without the '0x' prefix
    hex_string = hex(number)[2:]
    
    # Pad the hex string with leading zeros to achieve a length of 64 characters
    hex_string_padded = hex_string.zfill(64)
    
    return hex_string_padded

def hex_private_key_to_hex_public_key(hex_private_key):
    # Convert the hex string to bytes
    private_key_bytes = binascii.unhexlify(hex_private_key)
    # Create a SigningKey object from the private key bytes
    sk = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
    # Get the VerifyingKey (Public Key) from the SigningKey
    vk = sk.verifying_key
    # Convert the public key to its compressed form as a hex string
    public_key_hex = binascii.hexlify(vk.to_string("compressed")).decode("utf-8")
    return public_key_hex

def hex_public_key_to_bitcoin_address(public_key_hex):
    public_key_bytes = binascii.unhexlify(public_key_hex)
    # Step 1: SHA-256 hashing of the public key
    sha256_hash = hashlib.sha256(public_key_bytes).digest()
    # Step 2: RIPEMD-160 hashing of the SHA-256 hash
    ripemd160_hash = hashlib.new('ripemd160')
    ripemd160_hash.update(sha256_hash)
    # Step 3: Adding the network byte
    network_byte = b'\x00'
    network_and_ripemd160 = network_byte + ripemd160_hash.digest()
    # Step 4: Double SHA-256 hashing for the checksum
    double_sha256 = hashlib.sha256(hashlib.sha256(network_and_ripemd160).digest()).digest()
    checksum = double_sha256[:4]
    # Step 5: Assembly and Base58Check encoding
    binary_address = network_and_ripemd160 + checksum
    bitcoin_address = base58.b58encode(binary_address).decode('utf-8')
    return bitcoin_address

bits = 17
public_addr_to_find = btcadresses[bits]
start = pow(2, bits-1)
end = pow(2, bits)

print(f"Searching {bits} bit long private key for {public_addr_to_find} ({start}, {end})")

for number in range(start, end):
    private_key_hex = number_to_hex_private_key(number)
    public_key_hex = hex_private_key_to_hex_public_key(private_key_hex)
    bitcoin_address = hex_public_key_to_bitcoin_address(public_key_hex)
    
    if (number % 10000 == 0):
        print(f"{number}")

    if (bitcoin_address == public_addr_to_find):
        print(f"Private Key (Decimal): {number}")
        exit()
