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



datain = "ff000102030405060708090001020304050607080900010203040506070809ff"
datainBytes = bytearray.fromhex(datain)

sha256result = hashlib.sha256(datainBytes).digest()
ripemd160_hash = hashlib.new('ripemd160')
ripemd160_hash.update(datainBytes)
ripemd160result = ripemd160_hash.digest()
print("In:"+datain)
print("SHA256:"+sha256result.hex())
print("RIPEMD:"+ripemd160result.hex())


exit()



amount = 100000
sha256amount = amount * 100
print(f"Testing {amount} conversions")

# 0 - Measure simple sha256 12345678901234567890123456789032
timeStart = time.perf_counter()
byteArray = "12345678901234567890123456789032".encode()
for n in range(1, sha256amount):
    hashlib.sha256(byteArray).digest()

timeEnd = time.perf_counter()
t = str(datetime.timedelta(seconds=math.ceil((timeEnd - timeStart))))
print(f"Simple SHA256 x100: {(timeEnd - timeStart):.3f}")


# 1 - Measure RIPEMD
timeStart = time.perf_counter()

for n in range(1, amount):
    ripemd = number_to_network_and_ripemd160(n)

timeEnd = time.perf_counter()
t = str(datetime.timedelta(seconds=math.ceil((timeEnd - timeStart))))
print(f"Ripemd160: {(timeEnd - timeStart):.3f}")

# 2 - Measure SHA256
timeStart = time.perf_counter()

ripemd = number_to_network_and_ripemd160(5)
for n in range(1, amount):
    sha56 = network_and_ripemd160_to_double_sha256(b'\x00' + ripemd)[:4]
    
timeEnd = time.perf_counter()
t = str(datetime.timedelta(seconds=math.ceil((timeEnd - timeStart))))
print(f"DoubleSHA256: {(timeEnd - timeStart):.3f}")

# 3 - Measure both
timeStart = time.perf_counter()

for n in range(1, amount):
    ripemd = number_to_network_and_ripemd160(n)
    sha56 = network_and_ripemd160_to_double_sha256(b'\x00' + ripemd)[:4]
    
    
timeEnd = time.perf_counter()
t = str(datetime.timedelta(seconds=math.ceil((timeEnd - timeStart))))
print(f"Both: {(timeEnd - timeStart):.3f}")
