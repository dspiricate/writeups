# Write-Ups for the FCSC 2021



## Write-Up - Bienvenue à l'ANSSI



### Challenge discovery

We are presented  two files:

1. **ciphertexts.txt**, containing 3000 ciphertexts done by an AES circuit corrupted by UV exposition
2. **flag.enc.json**, a JSON containing the encrypted flag and its IV.





The statement tells us that the ciphertexts given are encrypted by an AES circuit that was degraded with UV. By searching on the internet about degraded AES by UV, I found this paper : http://www.mhutter.org/papers/Schmidt2009OpticalFaultAttacks.pdf

It describes how it is possible, given thousands of ciphertexts of a corrupted AES, according to how hard it was corrupted, to recover the main key of the circuit. It mainly described cases where only the SBox was corrupted, that gave me the intuitions for the attack.



### Analyzing the ciphertexts



I loaded the ciphertexts inside a Python script to perform frequency analysis over each byte of the ciphertexts (grouped by their position in the ciphertexts, e.g. every 1st byte of the ciphertexts, then every 2nd byte, etc.)



The idea I wanted to test was the following.

The last steps of an AES encryption are : SubBytes -> ShiftRows -> AddRoundKey

That means that, as ShiftRows does not modify the value, each byte of the ciphertext equals : `c[i] = Sbox[xi] ^ rkey[i]` where **rkey** is the last round key derived from the original key and **xi** is unknown.

However, if the Sbox is corrupted, some of the values will not be possible for **Sbox[xi]**.

Indeed, for example, let's take the case where `Sbox[a1] = b1` is corrupted, so that `Sbox[a1] = b2`.

As the original Sbox is a permutation, we also have another `a2 != a1` so that `Sbox[a2] = b2`, but also, as now `Sbox[a1] = b2` there does not exist a value a such that `Sbox[a] = a1`

So, for every `0 <= i < 16` , there exists a value yi such that `c[i] = Sbox[xi] ^ rkey[i]`cannot be equal to yi, but also a value zi such that `c[i] = Sbox[xi] ^ rkey[i]` will be equal to zi twice more often.

Given that, if we find such a value yi for each byte position, we can express each byte of the key as `rkey[i] = yi ^ b2`, where b2 is the value that disappeared from the Sbox.



So, for every 256 possibilities of such a value, we can try to recover the key from the computed last round key and then try to decrypt the flag.



### Getting the flag



The final program was:



```python
import code
import numpy as np
import os
from Crypto.Cipher import AES
import json

class myAES(object):
    #Stolen from one of \J's challenge on Root-me
 
    S = [
      0x63,0x7C,0x77,0x7B,0xF2,0x6B,0x6F,0xC5,0x30,0x01,0x67,0x2B,0xFE,0xD7,0xAB,0x76,
      0xCA,0x82,0xC9,0x7D,0xFA,0x59,0x47,0xF0,0xAD,0xD4,0xA2,0xAF,0x9C,0xA4,0x72,0xC0,
      0xB7,0xFD,0x93,0x26,0x36,0x3F,0xF7,0xCC,0x34,0xA5,0xE5,0xF1,0x71,0xD8,0x31,0x15,
      0x04,0xC7,0x23,0xC3,0x18,0x96,0x05,0x9A,0x07,0x12,0x80,0xE2,0xEB,0x27,0xB2,0x75,
      0x09,0x83,0x2C,0x1A,0x1B,0x6E,0x5A,0xA0,0x52,0x3B,0xD6,0xB3,0x29,0xE3,0x2F,0x84,
      0x53,0xD1,0x00,0xED,0x20,0xFC,0xB1,0x5B,0x6A,0xCB,0xBE,0x39,0x4A,0x4C,0x58,0xCF,
      0xD0,0xEF,0xAA,0xFB,0x43,0x4D,0x33,0x85,0x45,0xF9,0x02,0x7F,0x50,0x3C,0x9F,0xA8,
      0x51,0xA3,0x40,0x8F,0x92,0x9D,0x38,0xF5,0xBC,0xB6,0xDA,0x21,0x10,0xFF,0xF3,0xD2,
      0xCD,0x0C,0x13,0xEC,0x5F,0x97,0x44,0x17,0xC4,0xA7,0x7E,0x3D,0x64,0x5D,0x19,0x73,
      0x60,0x81,0x4F,0xDC,0x22,0x2A,0x90,0x88,0x46,0xEE,0xB8,0x14,0xDE,0x5E,0x0B,0xDB,
      0xE0,0x32,0x3A,0x0A,0x49,0x06,0x24,0x5C,0xC2,0xD3,0xAC,0x62,0x91,0x95,0xE4,0x79,
      0xE7,0xC8,0x37,0x6D,0x8D,0xD5,0x4E,0xA9,0x6C,0x56,0xF4,0xEA,0x65,0x7A,0xAE,0x08,
      0xBA,0x78,0x25,0x2E,0x1C,0xA6,0xB4,0xC6,0xE8,0xDD,0x74,0x1F,0x4B,0xBD,0x8B,0x8A,
      0x70,0x3E,0xB5,0x66,0x48,0x03,0xF6,0x0E,0x61,0x35,0x57,0xB9,0x86,0xC1,0x1D,0x9E,
      0xE1,0xF8,0x98,0x11,0x69,0xD9,0x8E,0x94,0x9B,0x1E,0x87,0xE9,0xCE,0x55,0x28,0xDF,
      0x8C,0xA1,0x89,0x0D,0xBF,0xE6,0x42,0x68,0x41,0x99,0x2D,0x0F,0xB0,0x54,0xBB,0x16
    ]
 
    RCON = [0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]
 
    def xor(self, L1, L2):
        return [ a^b for a,b in zip(L1, L2) ]
 
    def invExpandKey(self, key, disp = 0, double = 0):
        S = self.S.copy()
        S[S.index(disp)] = double
        subkeys = [key[i*4:(i+1)*4] for i in range(4)]
        for i in range(9, -1, -1):
            subkeys =  [self.xor(subkeys[3], subkeys[2])] + subkeys
            subkeys =  [self.xor(subkeys[3], subkeys[2])] + subkeys
            subkeys =  [self.xor(subkeys[3], subkeys[2])] + subkeys
            t1 = [self.RCON[i+1] ^ subkeys[3][0], subkeys[3][1], subkeys[3][2], subkeys[3][3]]
            c, d, e, f = subkeys[2]
            t2 = [S[d], S[e], S[f], S[c]]
            subkeys = [self.xor(t1, t2)] + subkeys 
        return subkeys[:4]


if __name__ == "__main__":

    with open("flag.enc.json") as f:
        flagenc = json.loads(f.read())
        iv = bytes.fromhex(flagenc["iv"])
        enc = bytes.fromhex(flagenc["ciphertext"])

    with open("ciphertexts.txt") as f:
        ciphertexts = [bytes.fromhex(x[:-1]) for x in f.readlines()]

    frequences = [np.zeros(256, dtype="int") for i in range(16)]

    for ciphertext in ciphertexts:
        for i in range(16):
            frequences[i][ciphertext[i]] += 1

    c1 = np.where(frequences[1] == frequences[1].min())[0][0]
    d1 = np.where(frequences[1] == frequences[1].max())[0][0]

    mins = []
    maxs = []
    for i in range(16):
        mins.append(np.where(frequences[i] == frequences[i].min())[0][0])
        maxs.append(c1 ^ d1 ^ mins[-1])

    myaes = myAES()
    for disp in range(256):
        key = [mins[i] ^ disp for i in range(16)]
        double = c1 ^ d1 ^ disp
        newkey = np.array(myaes.invExpandKey(key, disp, double))
        newkey = newkey.reshape(16)
        newkey = bytes(x for x in newkey)
        cipher = AES.new(newkey, AES.MODE_CBC, iv)
        dec = cipher.decrypt(enc)
        if (b"FCSC" in dec):
            print(dec)
```



And we get the flag : **FCSC{ff53c72a1783d8dc7deecc31fedac8ba575e56738440a16443fc29d8d2ca6a49}**
