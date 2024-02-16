# 1000 BTC Challenge

A tool designed for educational purposes and brute-forcing n-bit long Bitcoin private keys, specifically crafted for the [Bitcoin puzzle transaction](https://blockchain.info/tx/08389f34c98c606322740c0be6a7125d9860bb8d5cb182c02f98461e5fa6cd15). This transaction initially contained 256 addresses, each progressively more challenging to decipher.


# Bitcoin Challenge

In the realm of Bitcoin, both public and private keys consist of 256 bits, represented as sequences of zeros and ones such as 010101001...00101. It's straightforward to derive a public key from a private key, but the reverse process is exceedingly difficult. Hence, you can freely share your public keys, but you must keep your private key confidential. If someone were to deduce the private key associated with a public key holding Bitcoins, they could transfer those Bitcoins to their own wallet.

This raises a question: Are 256 bits sufficient for security?

An anonymous individual initiated a challenge by creating 256 unique public keys, each holding some amount of Bitcoin. However, instead of using full 256-bit private keys for each address, he generated shorter versions, beginning with a length of just 1 bit. Thus, the first private key is only 1 bit long, the 69th key is 69 bits long, and so forth. The shorter the key, the easier it is to crack.

As of February 13, 2024, all keys up to 65 bits in length have been discovered using tools like Bitcrack. The challenge escalates with the number of bits; currently, many participants are attempting to crack the [66bit key](https://www.blockchain.com/explorer/addresses/btc/13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so), which contains 6.6 Bitcoins, although some are focusing on specific lengths, such as 125 bits.

But how is it done? How can one obtain the private key for a known address? This project aims to explore the fundamentals and perhaps develop a method that is remarkably efficient, even though existing programs are already highly optimized.

## History

* 15.01.2025: a transaction was created containing a transfer transaction for 256 different Bitcoin addresses.
* 11.07.2017: funds from addresses #161—256 were moved to the same number of addresses of the lower range – thus increasing the amount of funds on them.
* 31.05.2019: the creator of the "puzzles" creates outgoing transactions with the value of 1000 satoshi for addresses #65, #70, #75, #80, #85, #90, #95, #100, #105, #110, #115, #120, #125, #130, #135, #140, #145, #150, #155, #160 with the aim of probably comparing the difficulty of finding a private key for the address from which such a transaction was carried out, and one that there is no transaction.
* 16.04.2023: somebody (maybe the owner) increased the unsolved puzzles prizes again by x10. Now the puzzle #66 prize is 6.6 BTC, #67 is 6.7 BTC and so on... puzzle #160 prize is 16 BTC.


# How to solve this challenge?

The simplest concept for discovering a private key associated with a known Bitcoin address is to iterate through all possible private keys. Given that a private key is essentially a number, one could sequentially go through each number, generating its corresponding public key for values like k=1,2,3,4,5,6,7, and so forth. For each number, the private key in its 256-bit format will be calculated. Following this, the public key is derived and then transformed into a Bitcoin address. If this address matches the known address, you have successfully found the matching private key! To move the coins, you can import the private key in its Wallet Import Format (WIF) into your wallet, such as with [Electrum](https://electrum.org/), facilitating the transfer of the funds.


Example (5 Bits):

```
Bits: 5
Public Key (BTC Address): 1E6NuFjCi27W5zoXg8TRdcSRq84zJeBW3k
Congratulations - Private Key found 
Private Key (Decimal): 21
Private Key (WIF): KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjgd9M7rFU7Dq8Au4Pv
```

<img src="misc/electrum1.png" height="250" />
<img src="misc/electrum2.png" height="250" />

# Notice

If you're considering tackling this challenge independently, be aware that it could take years to complete on a single computer. Joining a pool, such as the 66 Bit Collective Bitcoin Private Key Cracking Pool, might be a more practical approach. By participating in a pool, you also don't need to grasp every detail of the challenge, as these pools typically offer ready-to-use executables. This collaborative effort can significantly increase the chances of success by combining the computational power of many individuals.

<img src="misc/httpttdsales.com66bitlogin.png" height="250"/><br />
[66 Bit Collective Bitcoin Private Key Cracking Pool](http://ttdsales.com/66bit)


# Using this project

This project is meant to get the concept of the challenge and trying to increase the performance step by step. It incorporates a variety of techniques:

* It starts with a foundational Python-based approach (Approach 00), which, while easy to understand, is slow! This method is intended to help you to get the basics.
* The next technique (Approach 01) adds complexity by monitoring computation time and allowing for the continuation of calculations. It also prints out some useful information (WIF key and so on)
* The next technique (Approach 02) leverages parallelization to enhance efficiency.
* The next one (Approach 03) optimizes the comparison method, splitting components by RIPEMD and SHA256
* Future enhancements include developing a version in C to improve performance
* Additionally, a GPU-accelerated version is planned to further expedite the computation process. Python CUDA and C Cuda is on the list

# Quickstart

## Approach 00 - Understandable code

The first approach stands as the simplest among the methods employed. It serves as an excellent starting point and is configured by default to solve the 17-bit challenge, provided there are no modifications to the code in line 45. Read the code and try to understand its used libraries. I know it is tough, as there are several methods used, but it is worth to use the time understand the concept. A very good source is also this article [Generate BTC Private Key Explanation](https://groups.google.com/g/comp.lang.c/c/fbLnwQRBcPU?pli=1)

1. Install [Python 3](https://www.python.org/downloads/)
2. Then:

```
pip install base58
pip install ecdsa
python3 src/00_simple.py
```

### Output:

```
Searching 17 bit long private key for 1HduPEXZRdG26SUT5Yk83mLkPyjnZuJ7Bm (65536, 131072)
70000
80000
90000
Private Key (Decimal): 95823
```

## Approach 01 - Measure time and more

This method focuses on measuring the duration of operations and outputs the results in a format that can be readily utilized in your wallet. It requires you to specify the number of bits you wish to search for. Using this method, the performance achieved was 0.016 MKeys/sec, which is minimal when compared to BitCrack's capabilities. For instance, a 6800xt can achieve approximately 303 MKeys/sec, while a 6700xt can manage about 215 MKeys/sec with BitCrack.

```
python3 src/01_measure.py 22
Searching 2097152 22bit long private keys for 1CfZWK1QTQE3eS9qn61dQjV89KDjZzfNcv (2097152, 4194304)
Total 0:00:56 | 910351 keys | 43 % | 0.016 MKeys/sec
--------------------------------
Congratulations - Private Key found
Private Key (Decimal): 3007503
Private Key (HEX): 2de40f
Private Key (WIF): KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjgd9M7rP9Ja2dhtxoh
Public Key (HEX): 023ed96b524db5ff4fe007ce730366052b7c511dc566227d929070b9ce917abb43
Public Key (BTC Address): 1CfZWK1QTQE3eS9qn61dQjV89KDjZzfNcv
Bits: 22
--------------------------------
```

### Resume

In case you have to abort the computation, you can resume the process. The program will print the last checked private key, which you can then pass as the starting number the next time you start the computation, e.g.

```
python3 src/01_measure.py 21
Searching 1048576 21bit long private keys for 14oFNXucftsHiUMY8uctg6N487riuyXs4h (1048576, 2097152)
^C:00:03 | 38518 keys | 4 % | 0.018 MKeys/sec
--------------------------------
Aborted
To resume: 'python3 src/01_measure.py 21 1101338'
```

```
python3 src/01_measure.py 21 1101338
Searching 1048576 21bit long private keys for 14oFNXucftsHiUMY8uctg6N487riuyXs4h (1101338, 2097152)
```

## Approach 02 - Python with Parallelization

This approach leverages parallel computing techniques to significantly enhance the speed of the key search process. By distributing the workload across multiple processors or threads, it aims to improve efficiency and reduce the time required to find a matching key.

On my machine, 32 processes were created. The parallel method was 14 times faster than the standard version in solving the 22-bit challenge.

```
python3 src/02_parallel.py 22
Searching in parallel 2097152 22bit long private keys for 1CfZWK1QTQE3eS9qn61dQjV89KDjZzfNcv (2097152, 4194304)
Processes: 32
Total 0:00:03 | 910000 keys | 43 % | 0.329 MKeys/sec
--------------------------------
Congratulations - Private Key found
Private Key (Decimal): 3007503
Private Key (HEX): 2de40f
Private Key (WIF): KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjgd9M7rP9Ja2dhtxoh
Public Key (HEX): 023ed96b524db5ff4fe007ce730366052b7c511dc566227d929070b9ce917abb43
Public Key (BTC Address): 1CfZWK1QTQE3eS9qn61dQjV89KDjZzfNcv
Bits: 22
--------------------------------
```

## Approach 03 - Optimized comparison with Python

This version employs a different strategy. The process of converting a private key into a Bitcoin address involves multiple hashing and encoding/decoding steps. Each of these steps requires some time, so minimizing them is beneficial. While these steps are essential for generating the final Bitcoin address, to verify if the outcome is correct, the Bitcoin address can be divided into its RIPEMD and double SHA-256 components before beginning the loop. This allows for a comparison of only the RIPEMD portion, and the SHA-256 computation is performed only if the RIPEMD part is a match.

```
python3 src/03_optimize.py 22
Searching in parallel and optimized 2097152 22bit long private keys for 1CfZWK1QTQE3eS9qn61dQjV89KDjZzfNcv (2097152, 4194304)
Processes: 32
Total 0:00:03 | 910000 keys | 43 % | 0.378 MKeys/sec
--------------------------------
Congratulations - Private Key found
Private Key (Decimal): 3007503
Private Key (HEX): 2de40f
Private Key (WIF): KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjgd9M7rP9Ja2dhtxoh
Public Key (HEX): 023ed96b524db5ff4fe007ce730366052b7c511dc566227d929070b9ce917abb43
Public Key (BTC Address): 1CfZWK1QTQE3eS9qn61dQjV89KDjZzfNcv
Bits: 22
--------------------------------
```

## Approach 5 - C vs Python

This method involves implementing the algorithm in C, a low-level programming language known for its speed and efficiency. The simplicity of the code focuses on straightforward implementation without parallelization, offering improved performance over Python-based methods due to the compiled nature of C.

* Prerequisites: Make sure you have gcc. Should be preinstalled on bash/wsh. For Windows: Install gcc with Cygwin [cygwin](https://sourceware.org/cygwin/)
* Optional if gcc throws errors: Install secp256k1 and copy library (.a or .so) to src/c/secp256k1/ from https://github.com/bitcoin-core/secp256k1/   (unix2dos can help on windows)

C:
```
gcc src/04_perf.c src/c/addresses.c src/c/common.c src/c/sha2.c src/c/memzero.c src/c/ripemd160.c -I src/c -I src/c/secp256k1/include -Lsrc/c/secp256k1/.libs -l:libsecp256k1.a -o out/04_perf -O2 && out/04_perf
```
vs

Python:
```
python3 src/04_perf.py
```

## (TODO) Approach 6 - C Code Parallelization

Building on the fourth approach, this method adds parallelization to the C implementation. It utilizes multi-threading or other parallel computing techniques within C to further accelerate the search process by taking advantage of multiple CPU cores.

## (TODO) Approach 7 - Cuda

This approach employs CUDA (Compute Unified Device Architecture), a parallel computing platform and programming model developed by NVIDIA for general computing on graphical processing units (GPUs). By harnessing the power of GPU acceleration, this method can achieve orders of magnitude higher performance than CPU-based approaches, making it significantly faster at processing massive amounts of data, such as brute-forcing cryptographic keys.


# Performance

22 Bit challenge 

* AMD Ryzen 9 5950X 3,4 Ghz Base Speed L1/L2/L3: 1,8,64 MB
* NVIDIA GeForce RTX 3080 10GB - 64GB shared
* 128 GB RAM 2667 MHz

|Approach|Description|Language|MKeys/sec| 
|---|---|---|---|
|01|Serial|Python|0.016| 
|02|Parallel|Python|0.329| 
|03|Parallel Optimized|Python|0.378| 

# Links

* [Bitcoin puzzle transaction](https://blockchain.info/tx/08389f34c98c606322740c0be6a7125d9860bb8d5cb182c02f98461e5fa6cd15) The original transaction
* [Generate BTC Private Key Explanation](https://groups.google.com/g/comp.lang.c/c/fbLnwQRBcPU?pli=1) A good starting point
* [Bitcrack](https://github.com/brichard19/BitCrack) A cuda and cl based approach
* [Original Forum Post](https://bitcointalk.org/index.php?topic=1306983.0)
* [TPs Go Bitcoin Tests - Addresses](http://gobittest.appspot.com/Address) Convert private to public key online
* [BitAddress.org](https://www.bitaddress.org) Generate a private key by mouse movements
* [66 Bit Collective Bitcoin Private Key Cracking Pool](http://ttdsales.com/66bit)

# Author

Alexander Thurn

