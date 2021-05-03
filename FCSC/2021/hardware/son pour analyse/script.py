import matplotlib.pyplot as plt
import wave
import code
from gmpy2 import gcd
import hashlib
from Crypto.Util.number import long_to_bytes as l2b
e = 65537
n = 114181065031786564590139505995090932681603488058093695383755920020714540043378009781380110655253006728353171921382633045444731450267353184468441566668432893992049978192406103162591416659000523363797206479008373775089128981682147631692898693610665109453356689955829711356078688003770094519986009441791800904261


sound  = wave.open("RSA.wav")
b = sound.readframes(sound.getnframes())
b2 = [int(int(b[i:i+2].hex(),16).to_bytes(2, "little").hex(),16) for i in range(0, len(b), 4)]
b3 = []

# extract each point, keeping its sign
for x in b2:
    if x >> 15 == 0:
        b3.append(x)
    else:
        b3.append(-(x^0xffff))

# Correspond to the dp and dq parts of the signal
parts = [b3[97500:714000], b3[714000:1333000]]
bits = ["",""]
for k in range(2):
    d1 = parts[k]
    l = len(d1)
    i = 0
    while(i < l):
        if(d1[i] > 15000 and i+600 < l): # If a high peek is encountered
            i+=100 # Search a small peek in the next 100 points
            up = False
            for j in range(500):
                up = up or d1[i] > 9000
                i += 1
            if(up):
                bits[k] += "1"
            else:
                bits[k] += "0"
        i += 1

dp = int(bits[0],2)
dq = int(bits[1],2)
print(f"dp = {dp}")
print(f"dq = {dq}")

# Recover p from dp, n and e
for k in range(e):
    x = e*dp-1+k
    if(gcd(n, x) > 1):
        p = int(gcd(n,x))
        break

print(f"p = {p}")

q = n//p
phi = (p-1)*(q-1)
d = pow(e,-1,phi)

# Sign and sha256 the file RSA.wav
f = open('RSA.wav','rb')
raw = bytearray(f.read())
m = hashlib.sha256(raw).digest()
m = int.from_bytes(m, byteorder='big', signed=False)
sig = pow(m, d, n)
flag = hashlib.sha256(sig.to_bytes(128, byteorder="big")).digest()
print(f"FCSC{{{flag.hex()}}}")

code.interact(local=locals())
