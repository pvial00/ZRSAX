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
    psize = 64
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
        r = pow(l, 3) * (l * m) + k
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
        c = (pow(p, 3) + (q * p) + v) % a
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
        # Create our modulus which is the product of the C curve and the square root of the Base Modulus
        n = (e * int(math.sqrt(a)))
        # Create our totient which is composed of E - 1 and the Square root of the base modulus - 1
        s = ((e - 1) * (int(math.sqrt(a)) -1))
        # Find a number in the totient field that is coprime to the totient
        z = (number.getRandomRange(1, s))
        g = number.GCD(z, s)
        while g != 1:
            z = (number.getRandomRange(1, s))
            g = number.GCD(z, s)
            if g == 1:
                break
        pk = z
        # Wash the public key through the base totient
        _pk = number.inverse(pk, r)
        pk = _pk
        # Wash the public key through the C curve
        _pk = number.inverse(pk, c)
        pk = _pk
        # Find the secret key using the totient S
        sk = number.inverse(pk, s)
        # Test if we can encrypt successfully
        if pk != None:
            if testencrypt(pk, sk, n):
                good = 1
    return sk, pk, n
