#ifndef ADDRESSES_H
#define ADDRESSES_H

#define NUM_BTC_ADDRESSES 256 // Definiert die Größe des Arrays

extern const char* publicBTCAddresses[NUM_BTC_ADDRESSES];
extern const char* publicBTCDoubleSHA256[NUM_BTC_ADDRESSES];
extern const char* publicBTCRipemd160[NUM_BTC_ADDRESSES];
extern const char* publicBTCB58Decoded[NUM_BTC_ADDRESSES];

#endif