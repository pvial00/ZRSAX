from zrsaX import encrypt as zrsa_encrypt
from zrsaX import decrypt as zrsa_decrypt
from dark import crypt
import sys
from os import urandom
from Crypto.Util import number

keylen = 32
noncelen = 16
Klen = 73
mode = sys.argv[1]
infile = sys.argv[2]
outfile = sys.argv[3]
key = long(sys.argv[4])
mod = long(sys.argv[5])

if mode == "e":
    f = open(infile, "r")
    msg = f.read()
    f.close()
    keyP = urandom(keylen)
    nonce = urandom(noncelen)
    KP = number.bytes_to_long(keyP)
    K = number.long_to_bytes(zrsa_encrypt(number.bytes_to_long(keyP), key, mod))
    print len(K)
    ctxt = crypt(msg, keyP, nonce)
    f = open(outfile, "w")
    f.write(K+nonce+ctxt)
    f.close()
elif mode == "d":
    f = open(infile, "r")
    data = f.read()
    f.close()
    K = data[:Klen]
    nonce = data[Klen:Klen+noncelen]
    msg = data[noncelen+Klen:len(data) - 1]
    KP = zrsa_decrypt(number.bytes_to_long(K), key, mod)
    keyP = number.long_to_bytes(zrsa_decrypt(number.bytes_to_long(K), key, mod))
    ptxt = crypt(msg, keyP, nonce)
    f = open(outfile, "w")
    f.write(ptxt)
    f.close()
