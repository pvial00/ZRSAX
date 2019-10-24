import random
from Crypto.Util import number
import math

# requires pycrypto

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
    psize = 48
    o = 2
    while good != 1:
        # We generate 3 primes L and M and the cloaking prime K this is the base
        k = number.getPrime(psize)
        l = number.getPrime(psize)
        m = number.getPrime(psize)
        # Base modulus as the product of L and M
        a = l * m
        t = ((l - 1) * (m - 1))
        # Jump blockade
        r = pow(l, 2) * pow(m, 2) + k
        # Find 3 numbers in the jump field
        x = number.getRandomRange(1, (r))
        y = number.getRandomRange(1, (r))
        z = number.getRandomRange(1, (r))
        # Jump curve created from the 3 random points
        e = pow(x, 3) + (y * x) + z
        # Find 3 points in the jump curve field
        p = number.getRandomRange(1, (e))
        q = number.getRandomRange(1, (e))
        v = number.getRandomRange(1, (e))
        # Cloaking curve
        c = (pow(p, 3) + (q * p) + v)
        # Check to make sure the E curve is prime if not increment until it is
        if number.isPrime(e) == False:
            while True:
                e += 1
                if number.isPrime(e) == True:
                    break
        # Check to make sure the C curve is prime if not increment until it is
        if number.isPrime(c) == False:
            while True:
                c += 1
                if number.isPrime(c) == True:
                    break
        # Check to make sure the R blockade is prime if not increment until it is
        if number.isPrime(r) == False:
            while True:
                r += 1
                if number.isPrime(r) == True:
                    break
        # Create our modulus which is the product of the C curve and the square root of the Base Modulus
        n = (c * long(math.sqrt(a)))
        # Create our totient which is composed of E - 1 and the Square root of the base modulus - 1
        s = ((c - 1) * (long(math.sqrt(a)) -1))
        # Find a number in the totient field that is coprime to the totient which is the public key
        pk = (number.getRandomRange(1, s))
        g = number.GCD(pk, s)
        while g != 1:
            z = (number.getRandomRange(1, s))
            g = number.GCD(pk, s)
            if g == 1:
                break
        # Find the secret key using the totient S
        sk = number.inverse(pk, s)
        # Test if we can encrypt successfully
        if pk != None:
            if testencrypt(pk, sk, n):
                good = 1
    return sk, pk, n
