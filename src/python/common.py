import hashlib
import base58

def decimal_to_wif(private_key_decimal, compressed=True):
    # Konvertiere den Private Key von Dezimal in Bytes
    private_key_bytes = private_key_decimal.to_bytes(32, byteorder='big')
    
    # Füge das Wallet Präfix hinzu (0x80 für Bitcoin)
    prefix = b'\x80'
    prefixed_key = prefix + private_key_bytes
    
    # Für komprimierte Public Keys, füge 0x01 am Ende hinzu
    if compressed:
        prefixed_key += b'\x01'
    
    # Generiere die Prüfsumme durch doppeltes SHA-256 Hashing
    hash_once = hashlib.sha256(prefixed_key).digest()
    hash_twice = hashlib.sha256(hash_once).digest()
    checksum = hash_twice[:4]  # Die ersten vier Bytes der Prüfsumme
    
    # Füge die Prüfsumme hinzu und kodiere das Ganze in Base58
    full_key = prefixed_key + checksum
    wif_key = base58.b58encode(full_key).decode('utf-8')
    
    return wif_key

