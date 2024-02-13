import sys, time, datetime, math
import base58, binascii, hashlib
from ecdsa import SigningKey, SECP256k1
from python.addresses import btcadresses
from python.RepeatedTimer import RepeatedTimer
from python.common import decimal_to_wif, number_to_hex_private_key, hex_private_key_to_hex_public_key, hex_public_key_to_bitcoin_address

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
bitcoin_address = ""
timeStart = time.perf_counter()
timeEnd = time.perf_counter()

print(f"Searching {(end-start)} {bits}bit long private keys for {public_addr_to_find} ({realstart}, {end})")

def printTiming(name): 
    timeEnd = time.perf_counter()
    t = str(datetime.timedelta(seconds=math.ceil((timeEnd - timeStart))))
    print(f"{name} {t} | {(number-start):.0f} keys | {100*(number-start)/(end-start):.0f} % | {0.000001*(number-start)/(timeEnd - timeStart):.3f} MKeys/sec", end="\r")

rt = RepeatedTimer(1, printTiming, "")

try:
    for number in range(realstart, end):
        private_key_hex = number_to_hex_private_key(number)
        public_key_hex = hex_private_key_to_hex_public_key(private_key_hex)
        bitcoin_address = hex_public_key_to_bitcoin_address(public_key_hex)
        
        if (bitcoin_address == public_addr_to_find):
            break
except (Exception, KeyboardInterrupt):
    print("")
    print("--------------------------------")
    print("Aborted")
    print(f"To resume: 'python3 src/01_measure.py {bits} {number}'")
    rt.stop()
    exit()

rt.stop()
printTiming('Total')
print("")
print("--------------------------------")
print(f"Congratulations - Private Key found")
print(f"Private Key (Decimal): {number}")
print(f"Private Key (HEX): {format(number, 'x')}")
print(f"Private Key (WIF): {decimal_to_wif(number)}")
print(f"Public Key (HEX): {public_key_hex}")
print(f"Public Key (BTC Address): {bitcoin_address}")
print(f"Bits: {bits}")
print("--------------------------------")