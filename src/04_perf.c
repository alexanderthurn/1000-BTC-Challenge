#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
#include <unistd.h>
#include "secp256k1.h"
#include "addresses.h"
#include "common.h"
#include "sha2.h"
#include "ripemd160.h"

typedef uint8_t uint256[32];
typedef uint8_t uint160[20];
#define SHA256_BLOCK_LENGTH		64
#define SHA256_DIGEST_LENGTH		32
#define SHA256_DIGEST_STRING_LENGTH	(SHA256_DIGEST_LENGTH * 2 + 1)
#define BTC_ECKEY_UNCOMPRESSED_LENGTH 65
#define BTC_ECKEY_COMPRESSED_LENGTH 33
#define BTC_ECKEY_PKEY_LENGTH 32
#define BTC_ECKEY_PKEY_LENGTH 32
#define BTC_HASH_LENGTH 32

int64_t timespecDiff(struct timespec *timeA_p, struct timespec *timeB_p)
{
  return ((timeA_p->tv_sec * 1000000000) + timeA_p->tv_nsec) -
           ((timeB_p->tv_sec * 1000000000) + timeB_p->tv_nsec);
}

void btc_hash(const unsigned char* datain, size_t length, uint256 hashout)
{
    sha256_Raw(datain, length, hashout);
    sha256_Raw(hashout, SHA256_DIGEST_LENGTH, hashout);
}

int main() {

 printf("B\n");
   secp256k1_ecdsa_signature sig;
   secp256k1_pubkey pubkey;
   secp256k1_context* ctx = secp256k1_context_create(SECP256K1_CONTEXT_NONE); 

   secp256k1_selftest();

    unsigned char msg_hash[32] = {
        0x31, 0x5F, 0x5B, 0xDB, 0x76, 0xD0, 0x78, 0xC4,
        0x3B, 0x8A, 0xC0, 0x06, 0x4E, 0x4A, 0x01, 0x64,
        0x61, 0x2B, 0x1F, 0xCE, 0x77, 0xC8, 0x69, 0x34,
        0x5B, 0xFC, 0x94, 0xC7, 0x58, 0x94, 0xED, 0xD3,
    };

    int is_signature_valid2 = secp256k1_ecdsa_verify(secp256k1_context_static,
                                                 &sig, msg_hash, &pubkey);
    printf("IsValid:%d\n", is_signature_valid2);







   size_t length = BTC_HASH_LENGTH;
   uint256 hashSHA256;
   uint8_t hashRipeMD[RIPEMD160_DIGEST_LENGTH];


   unsigned char datain[] = {0xFF, 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0xFF};
   
   printf("In:");
   for(int i = 0; i < BTC_HASH_LENGTH; i++) {
      printf("%02X", datain[i]);
   }
   printf("\n");

   sha256_Raw(datain, length, hashSHA256);
   printf("SHA256:");
   for (int n=0;n<BTC_HASH_LENGTH;n++) {
      printf("%02x", hashSHA256[n]);
   }
   printf("\n");


   ripemd160(datain, BTC_HASH_LENGTH, hashRipeMD);
   printf("RIPEMD:");
   for (int n=0;n<RIPEMD160_DIGEST_LENGTH;n++) {
      printf("%02x", hashRipeMD[n]);
   }
   printf("\n");



   unsigned char privateKey[32] = {
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01,
    };

   int genKeyCheck = secp256k1_ec_pubkey_create(ctx,&pubkey,privateKey);
   unsigned char output[256];
   size_t olength = 256;

   int convertCheck = secp256k1_ec_pubkey_serialize(ctx, output, &olength, &pubkey, SECP256K1_EC_COMPRESSED);

   printf("IsValid:%d %d %ld\n", genKeyCheck, convertCheck, olength);
   printf("VerifiyingKeyC:");
   for (int n=0;n<olength;n++) {
      printf("%02x", output[n]);
   }
   printf("\n");

   // Performance 
   int amount = 10000;
   int sha256amount = amount * 100;
   int ripemd160amount = amount * 100;
   printf("Performance Test\n");
   struct timespec start, end;
   clock_gettime(CLOCK_MONOTONIC, &start);
   for (int n=0;n<sha256amount;n++) {
      sha256_Raw(datain, length, hashSHA256);
   }
   clock_gettime(CLOCK_MONOTONIC, &end);
   uint64_t timeElapsed = timespecDiff(&end, &start);
   printf("SHA256 %d: %.5f\n", sha256amount, timeElapsed/(float)1000000000);

   clock_gettime(CLOCK_MONOTONIC, &start);
   for (int n=0;n<ripemd160amount;n++) {
      ripemd160(datain, BTC_HASH_LENGTH, hashRipeMD);
   }
   clock_gettime(CLOCK_MONOTONIC, &end);
   timeElapsed = timespecDiff(&end, &start);
   printf("RipeMD %d: %.5f\n", ripemd160amount, timeElapsed/(float)1000000000);

   clock_gettime(CLOCK_MONOTONIC, &start);
   for (int n=0;n<amount;n++) {
      int genKeyCheck = secp256k1_ec_pubkey_create(ctx,&pubkey,privateKey);
      secp256k1_ec_pubkey_serialize(ctx, output, &olength, &pubkey, SECP256K1_EC_COMPRESSED);
   }
   clock_gettime(CLOCK_MONOTONIC, &end);
   timeElapsed = timespecDiff(&end, &start);
   printf("Secp256k1 %d: %.5f\n", amount, timeElapsed/(float)1000000000);

   return 0;



   /*int numAddresses = sizeof(publicBTCAddresses) / sizeof(publicBTCAddresses[0]);
   for (int i = 0; i < numAddresses; i+=10) {
      printf("%d: %s\n", i + 1, publicBTCAddresses[i]);
   }

   uint256_t myValue = {0x1234567890ABCDEF, 0xFEDCBA0987654321, 0x0F0F0F0F0F0F0F0F, 0xF0F0F0F0F0F0F0F0};
   char* valueStr = decimal_to_wif(myValue);
   if (valueStr != NULL) {
      printf("256-Bit Integer to WIF (TODO): %s\n", valueStr);
      free(valueStr);
   }

   uint256_t myValue2 = {0x1, 0xFEDC, 0x0, 0xF0};
   char* valueStr2 = decimal_to_hex_private_key(myValue2);
   if (valueStr2 != NULL) {
      printf("256-Bit Integer to Private Key Hex(TODO): %s\n", valueStr2);
      free(valueStr2);
   }*/

   return 0;
}