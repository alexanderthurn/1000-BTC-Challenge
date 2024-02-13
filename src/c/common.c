#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <inttypes.h>
#include "common.h"

char* decimal_to_wif(uint256_t value) {
    char* result = malloc(65 * sizeof(char)); // 64 Zeichen + 1 für das Nullterminierungszeichen
    if (result == NULL) {
        return NULL;
    }

    snprintf(result, 65, "%016" PRIx64 "%016" PRIx64 "%016" PRIx64 "%016" PRIx64,
             value[0], value[1], value[2], value[3]);

    return result;
}

char* decimal_to_hex_private_key(uint256_t value) {
    char* result = malloc(65 * sizeof(char)); // 64 Zeichen + 1 für das Nullterminierungszeichen
    if (result == NULL) {
        return NULL;
    }

    snprintf(result, 65, "%016" PRIx64 "%016" PRIx64 "%016" PRIx64 "%016" PRIx64,
             value[0], value[1], value[2], value[3]);

    return result;
    
}