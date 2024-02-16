#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
#include <unistd.h>

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

   return 0;



   int amount = 100000;
   int sha256amount = amount * 100;

   printf("Testing %d conversions\n", amount);
   struct timespec start, end;
 clock_gettime(CLOCK_MONOTONIC, &start);
  
   for (int n=0;n<sha256amount;n++) {
      // int sha256 = number_to_network_and_ripemd160(n);
      sha256_Raw(datain, length, hashSHA256);
   }

   clock_gettime(CLOCK_MONOTONIC, &end);
   uint64_t timeElapsed = timespecDiff(&end, &start);
   printf("Simple SHA256 x100: %.5f\n", timeElapsed/(float)1000000000);




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