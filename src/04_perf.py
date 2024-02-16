import sys, time, datetime, math
import base58, binascii, hashlib
from multiprocessing import Pool
from ecdsa import SigningKey, SECP256k1
from python.addresses import btcadresses
from python.RepeatedTimer import RepeatedTimer
from python.common import decimal_to_wif, number_to_hex_private_key, hex_private_key_to_hex_public_key, hex_public_key_to_bitcoin_address


datain = "FF000102030405060708090001020304050607080900010203040506070809FF"
datainBytes = bytearray.fromhex(datain)
sha256result = hashlib.sha256(datainBytes).digest()
ripemd160_hash = hashlib.new('ripemd160')
ripemd160_hash.update(datainBytes)
ripemd160result = ripemd160_hash.digest()
print("In:"+datain)
print("SHA256:"+sha256result.hex())
print("RIPEMD:"+ripemd160result.hex())
sk = SigningKey.from_secret_exponent(1, curve=SECP256k1)
print('VerifyingKey:'+sk.verifying_key.to_string().hex())
print('VerifyingKeyC:'+sk.verifying_key.to_string('compressed').hex())


# Performance 
amount = 10000
sha256amount = amount * 100
ripemd160amount = amount * 100

print(f"Performance Test")

# 0 - SHA256
timeStart = time.perf_counter()
for n in range(1, sha256amount):
    hashlib.sha256(datainBytes).digest()
timeEnd = time.perf_counter()
t = str(datetime.timedelta(seconds=math.ceil((timeEnd - timeStart))))
print(f"SHA256 {sha256amount}: {(timeEnd - timeStart):.3f}")


# 1 -  RIPEMD
timeStart = time.perf_counter()
for n in range(1, ripemd160amount):
    ripemd160_hash = hashlib.new('ripemd160')
    ripemd160_hash.update(datainBytes)
    ripemd160result = ripemd160_hash.digest()
timeEnd = time.perf_counter()
t = str(datetime.timedelta(seconds=math.ceil((timeEnd - timeStart))))
print(f"RipeMD {ripemd160amount}: {(timeEnd - timeStart):.3f}")

# 2 - secp256k1
timeStart = time.perf_counter()
for n in range(1, amount):
    sk = SigningKey.from_secret_exponent(1, curve=SECP256k1)
    sk.verifying_key.to_string('compressed').hex()

timeEnd = time.perf_counter()
t = str(datetime.timedelta(seconds=math.ceil((timeEnd - timeStart))))
print(f"Secp256k1 {amount}: {(timeEnd - timeStart):.3f}")
