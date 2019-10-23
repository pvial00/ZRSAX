import random
from Crypto.Util import number
from Crypto.Random import random as prandom
import math

# requires pycrypto

def mygcd(a, b):
    while True:
        while b != 0:
            a, b = b, a % b
        return a

def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi/e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2- temp1* x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi

def encrypt(ptxt, pk, mod):
    return pow(ptxt, pk, mod)

def decrypt(ctxt, sk, mod):
    return pow(ctxt, sk, mod)

def sign(ctxt, sk, mod):
    return pow(ctxt, sk, mod)

def verify(ptxt, ctxt, pk, mod, s):
    x = pow(ptxt, pk, mod)
    if x == ctxt:
        return True
    else:
        return False

def testencrypt(pk, sk, mod):
    msg = "012345678901234567890"
    msg = "H"
    m = number.bytes_to_long(msg)
    ctxt = encrypt(m, pk, mod)
    if sk != None:

        ptxt = decrypt(ctxt, sk, mod)
        if ptxt == m:
            return True
        else:
            return False
    return False

def keygen():
    good = 0
    psize = 4
    o = 2
    while good != 1:
        l = number.getPrime(psize)
        m = number.getPrime(psize)
        a = l * m
        e = pow(l, 2) + pow(m, 2)
        x = number.getRandomRange(1, (e))
        y = number.getRandomRange(1, (e))
        r = pow(x, 2) + pow(y, 2)
        p = number.getRandomRange(1, (r**o))
        q = number.getRandomRange(1, (r**o))
        v = number.getRandomRange(1, (r**o))
        if number.isPrime(e) == False:
            while True:
                e += 1
                if number.isPrime(e) == True:
                    break
        if number.isPrime(r) == False:
            while True:
                r += 1
                if number.isPrime(r) == True:
                    break
        n = (e * r)
        t = (((r - 1) * (e - 1)))
        z = (number.getRandomRange(1, t))
        g = number.GCD(z, t)
        while g != 1:
            z = (number.getRandomRange(1, t))
            g = number.GCD(z, t)
            if g == 1:
                break
        pk = z
        sk = number.inverse(pk, t)
        if pk != None:
            if testencrypt(pk, sk, n):
                print "lm", l, m, e, r
                good = 1
    return sk, pk, n
