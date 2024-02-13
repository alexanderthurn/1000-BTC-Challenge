import sys, time, datetime, math
import base58, binascii, hashlib
from multiprocessing import Pool
from ecdsa import SigningKey, SECP256k1
from python.addresses import btcadresses
from python.RepeatedTimer import RepeatedTimer
from python.common import decimal_to_wif, number_to_hex_private_key, hex_private_key_to_hex_public_key, hex_public_key_to_bitcoin_address

def number_to_network_and_ripemd160(number):
    sk = SigningKey.from_secret_exponent(number, curve=SECP256k1)
    sha256_hash = hashlib.sha256(sk.verifying_key.to_string("compressed")).digest()
    ripemd160_hash = hashlib.new('ripemd160')
    ripemd160_hash.update(sha256_hash)
    return ripemd160_hash.digest()
    
def network_and_ripemd160_to_double_sha256(network_and_ripemd160):
    return hashlib.sha256(hashlib.sha256(network_and_ripemd160).digest()).digest()

# optimization alternative without split (not as good as seperated so within a comment)

# def number_to_bitcoin_address_b58decoded(number):
#     sk = SigningKey.from_secret_exponent(number, curve=SECP256k1)
#     sha256_hash = hashlib.sha256(sk.verifying_key.to_string("compressed")).digest()
#     ripemd160_hash = hashlib.new('ripemd160')
#     ripemd160_hash.update(sha256_hash)
#     network_and_ripemd160 = b'\x00' + ripemd160_hash.digest()
#     double_sha256 = hashlib.sha256(hashlib.sha256(network_and_ripemd160).digest()).digest()
#     return network_and_ripemd160 + double_sha256[:4]

if (len(sys.argv) < 2):
    print("Missing parameter [amount of Bits (1-256)]")
    print("e.g. 'python3 01_measure.py 17'")
    exit()

bits = int(sys.argv[1])
public_addr_to_find = btcadresses[bits]
public_addr_to_find_b58decoded = base58.b58decode(public_addr_to_find)
public_addr_to_find_ripemd = public_addr_to_find_b58decoded[1:-4]
public_addr_to_find_double_sha256 = public_addr_to_find_b58decoded[-4:]
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
        ripemd = number_to_network_and_ripemd160(n)
        if (ripemd == public_addr_to_find_ripemd):
            if ((network_and_ripemd160_to_double_sha256(b'\x00' + ripemd))[:4] == public_addr_to_find_double_sha256):
                return s, n
        
        # optimization alternative without split (not as good as seperated so within a comment)
        # bitcoin_address_b58decoded=number_to_bitcoin_address_b58decoded(n)
        # if (bitcoin_address_b58decoded == public_addr_to_find_b58decoded):
        #    return s, n
            
    return s, 0

try:
    with Pool() as pool: 
        print(f"Searching in parallel and optimized {(end-start)} {bits}bit long private keys for {public_addr_to_find} ({realstart}, {end})")
        print(f"Processes: {pool._processes}")
        for r in pool.imap_unordered(computeBatch, range(realstart, end, stepwidth)):
            number = r[0]
            if (r[1] > 0):
                result = r[1]
                pool.close()
                break
except (Exception, KeyboardInterrupt):
    rt.stop()
    print("")
    print("--------------------------------")
    print("Aborted")
    print(f"To resume: 'python3 src/01_measure.py {bits} {number}'")
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