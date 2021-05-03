import re
from Crypto.Cipher import ARC4

# Calculates the hash of the TV program names
def hash(s):
    h = 0
    for i in s:
        c = ord(i)
        h = ((h << 8) ^ (h >> 8) ^ c) & 0xffff
    return h

# Extracts the information of each TV program
chaines = []
for i in range(2,34):
    chaine = {}
    wd = f"./Event_{i:02d}"
    with open(f"{wd}/Short_Event_Descriptor/event_name") as f:
        chaine["hash_name"] = hash(f.read())
    with open(f"{wd}/Short_Event_Descriptor/text") as f:
        chaine["short"] = f.read()
    with open(f"{wd}/Extended_Event_Descriptor/Descriptor_00/item_description") as f:
        chaine["long"] = f.read()
    chaines.append(chaine)

# Extracts the information of the key construction
re_int = re.compile("[0-9]+")

with open("list.txt") as f:
    list_b = f.readlines()

list_tests = []
for i in range(0,len(list_b),3):
    name_hash = int(re_int.search(list_b[i])[0])
    ind_key = int(re_int.search(list_b[i+1])[0])
    if("longDescription" in list_b[i+1]):
        desc = "long"
    elif("description" in list_b[i+1]):
        desc = "short"
    else:
        print("ERROR !!!!!")
    list_tests.append({"name_hash": name_hash, "ind_key":ind_key, "desc":desc})


# Recovers the key, given the key construction and TV program information
key = ["" for i in range(32)]
for test in list_tests:
    for chaine in chaines:
        if(chaine["hash_name"] == test["name_hash"]):
            c = chaine
    key[test["ind_key"]] = c[test["desc"]]

key = bytes.fromhex("".join(key))

print("The key is :", key.hex())
# Decrypts the ciphertext
ciphertexts = [
    "1c8fe6416ae2c7f40fad06e7d410aec734c23a96748a8aba9d7c2d5cac12d326aa1105e4820a1bbda27426a4557caebb97cff12c534c680284aceefff9b69c28ee0165394ec0aca77cc6364fc546c0072ff80480aba6ecb859f5ec374dd3cbbdfbd575b60f9e7952882f6214ff4dcc8158",
    "ceb21c62048e7324c1d30401f8d8dcbabe029cddf103ca9743f92113d9a89cfc96d49a436dc0e6941241bbb8a3773c7774cea837ca86020a80c04105bb6fc032a4d02d199ecce7352cf617344764d5f8d09b3180c3a2f07815685af1d8ee1d6a6d49ddcf6938487ee3b9477a946860d05c",
    "c3e2c2ab9f1884420ea83275160012cca881a13a9c93498e9beb7f270317dfdedf40a402b98ab862115318a798e4b105864670e9b0405744269f7bab43c888ea65bbabb45608f768220040d118b5ca435183b87ca9507423df69fa89e3962358dfde0621408e0fe75b40860e526a20c332",
    "930b88dcf93c16e66a9cdf0fb71d7ef9a8120dc5675f8372a18cc4cb350b8bb70ec2e500e197629a7f49e5467ac66864ba294996d600721b38c74781553983f763331acf265dec94aab8bf13ebb436f9322305330c430a61c8c1ea3c6c763d7b4db5a8905904bfdd80298bbb085bd92b92",
    "938ed5551251a0e3d3dbc2e2156c7407f2826ec9126baaaaf64d270801cccbabea52118e23c7c08ec5131017919f563e27c13825e50f3f1b212e98fff8c277eaa48c35c4cc0cd0724bf943cd81c7d42a9d659501d6aef4c8c759129a0b0af116c3b2bb5a1a5c85a95a932d0f3936eaf807"
]
check = bytes.fromhex("00112233445566778899aabbccddeeff")
key2 = ARC4.new(key).decrypt(check)
for c in ciphertexts:
    ciphertext = bytes.fromhex(c)
    plaintext = ARC4.new(key2).decrypt(ciphertext)
    if (b"FCSC" in plaintext):
        print(plaintext)
        exit(0)

