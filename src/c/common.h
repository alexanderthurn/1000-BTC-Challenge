#ifndef COMMON_H
#define COMMON_H

#include <stdint.h>

typedef uint64_t uint256_t[4];
typedef char* charPtrArray256[256];

char* decimal_to_wif(uint256_t value);
char* decimal_to_hex_private_key(uint256_t value);

#endif