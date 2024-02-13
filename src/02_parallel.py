import sys, time, datetime, math
import base58, binascii, hashlib
from multiprocessing import Pool
from ecdsa import SigningKey, SECP256k1
from python.addresses import btcadresses
from python.RepeatedTimer import RepeatedTimer
from python.common import decimal_to_wif

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

if (len(sys.argv) < 2):
    print("Missing parameter [amount of Bits (1-256)]")
    print("e.g. 'python3 01_measure.py 17'")
    exit()

bits = int(sys.argv[1])
public_addr_to_find = btcadresses[bits]
start = pow(2,bits-1)
realstart = start
if (len(sys.argv) > 2):
    realstart = int(sys.argv[2])
end = pow(2,(bits))
number = 0
result = 0
public_key_hex =""
bitcoin_address = ""
timeStart = time.perf_counter()
timeEnd = time.perf_counter()
stepwidth=10000


def printTiming(name): 
    timeEnd = time.perf_counter()
    t = str(datetime.timedelta(seconds=math.ceil((timeEnd - timeStart))))
    if (number-start > 0):
        print(f"{name} {t} | {(number-start):.0f} keys | {100*(number-start)/(end-start):.0f} % | {0.000001*(number-start)/(timeEnd - timeStart):.3f} MKeys/sec", end="\r")

rt = RepeatedTimer(1, printTiming, "")

def computeBatch(s):
    for n in range(s, s+stepwidth):
        private_key_hex = number_to_hex_private_key(n)
        public_key_hex = hex_private_key_to_hex_public_key(private_key_hex)
        bitcoin_address = hex_public_key_to_bitcoin_address(public_key_hex)
        if (bitcoin_address == public_addr_to_find):
            return s, n
    return s, 0

try:
    with Pool() as pool: 
        print(f"Searching in parallel {(end-start)} {bits}bit long private keys for {public_addr_to_find} ({realstart}, {end})")
        print(f"Processes: {pool._processes}")
        for r in pool.imap(computeBatch, range(realstart, end, stepwidth)):
            if (r[0] > 0):
                number = r[0]
            if (r[1] > 0):
                result = r[1]
                break

except (Exception, KeyboardInterrupt):
    pool.terminate()
    print("")
    print("--------------------------------")
    print("Aborted")
    print(f"To resume: 'python3 src/01_measure.py {bits} {number}'")
    rt.stop()
    exit()

rt.stop()
printTiming('Total')



private_key_hex = number_to_hex_private_key(result)
public_key_hex = hex_private_key_to_hex_public_key(private_key_hex)
bitcoin_address = hex_public_key_to_bitcoin_address(public_key_hex)
print("")
print("--------------------------------")
print(f"Congratulations - Private Key found")
print(f"Private Key (Decimal): {result}")
print(f"Private Key (HEX): {format(result, 'x')}")
print(f"Private Key (WIF): {decimal_to_wif(result)}")
print(f"Public Key (HEX): {public_key_hex}")
print(f"Public Key (BTC Address): {bitcoin_address}")
print(f"Bits: {bits}")
print("--------------------------------")