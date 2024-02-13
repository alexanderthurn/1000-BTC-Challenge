#include <stdio.h>
#include <stdlib.h>
#include "addresses.h"
#include "common.h"

int main() {
   int numAddresses = sizeof(publicBTCAddresses) / sizeof(publicBTCAddresses[0]);

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
   }

   return 0;
}