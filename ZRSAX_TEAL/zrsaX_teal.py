from teal import Teal
from zrsaX import encrypt as zrsaX_encrypt
from zrsaX import decrypt as zrsaX_decrypt
import sys
from os import urandom
from Crypto.Util import number

# 2040 bit key max
keylen = 8
Klen = 29
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
    K = number.long_to_bytes(zrsaX_encrypt(number.bytes_to_long(keyP), key, mod))
    ctxt = Teal().encrypt(msg, keyP)
    print len(K)
    f = open(outfile, "w")
    f.write(K+ctxt)
    f.close()
elif mode == "d":
    f = open(infile, "r")
    data = f.read()
    f.close()
    K = data[:Klen]
    msg = data[Klen:len(data) -1]
    keyP = number.long_to_bytes(zrsaX_decrypt(number.bytes_to_long(K), key, mod))
    ptxt = Teal().decrypt(msg, keyP)
    f = open(outfile, "w")
    f.write(ptxt)
    f.close()
