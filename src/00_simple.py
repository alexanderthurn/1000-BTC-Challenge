import base58, binascii, hashlib
from ecdsa import SigningKey, SECP256k1
from python.addresses import btcadresses

def number_to_hex_private_key(number):
    # Konvertiere die Zahl in einen Hex-String ohne das '0x'-Präfix
    hex_string = hex(number)[2:]
    
    # Fülle den Hex-String mit führenden Nullen auf, um eine Länge von 64 Zeichen zu erreichen
    hex_string_padded = hex_string.zfill(64)
    
    return hex_string_padded

def hex_private_key_to_hex_public_key(hex_private_key):
    # Konvertiere den Hex-String in Bytes
    private_key_bytes = binascii.unhexlify(hex_private_key)
    # Erstelle ein SigningKey-Objekt aus den Private Key Bytes
    sk = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
    # Hole den VerifyingKey (Public Key) aus dem SigningKey
    vk = sk.verifying_key
    # Konvertiere den Public Key in seine komprimierte Form als Hex-String
    public_key_hex = binascii.hexlify(vk.to_string("compressed")).decode("utf-8")
    return public_key_hex

def hex_public_key_to_bitcoin_address(public_key_hex):
    public_key_bytes = binascii.unhexlify(public_key_hex)
    # Schritt 1: SHA-256 Hashing des Public Keys
    sha256_hash = hashlib.sha256(public_key_bytes).digest()
    # Schritt 2: RIPEMD-160 Hashing des SHA-256 Hashs
    ripemd160_hash = hashlib.new('ripemd160')
    ripemd160_hash.update(sha256_hash)
    # Schritt 3: Hinzufügen des Netzwerk-Bytes
    network_byte = b'\x00'
    network_and_ripemd160 = network_byte + ripemd160_hash.digest()
    # Schritt 4: Doppeltes SHA-256 Hashing für die Prüfsumme
    double_sha256 = hashlib.sha256(hashlib.sha256(network_and_ripemd160).digest()).digest()
    checksum = double_sha256[:4]
    # Schritt 5: Zusammensetzen und Base58Check-Kodierung
    binary_address = network_and_ripemd160 + checksum
    bitcoin_address = base58.b58encode(binary_address).decode('utf-8')
    return bitcoin_address

bits = 17
public_addr_to_find = btcadresses[bits]
start = pow(2,bits-1)
end = pow(2,(bits))

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


