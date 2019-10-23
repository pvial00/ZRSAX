import random
from Crypto.Util import number
from Crypto.Random import random as prandom

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
        #k = number.getPrime(psize)
        #l = number.getPrime(psize)
        #m = number.getPrime(psize)
        k = 179
        l = 131
        m = 221
        a = l * m
        e = pow(l, 3) + (l * m) + k
        r = pow(l, o) + pow(m, o) + k
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
        n = (r * k) % e
        t = ((e - 1) * (r - 1) * (k - 1))  
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
                print "klm", k, l, m, e, r
                good = 1
    return sk, pk, n

print "We want to encrypt the letter A"
msg = "A"
m = number.bytes_to_long(msg)
print "The message"
print m
sk, pk, mod = keygen()
print "Secret key, public key, modulus"
print sk, pk, mod
c = encrypt(m, pk, mod)
print "Cipher text"
print c
p = decrypt(c, sk, mod)
print "Plain Text"
print p

import math
print "Square root of modulus"
crack = int(math.sqrt(mod))
print crack

primes = []
for i in range(2, 600000, 1):
    try:
        if (mod % i) == 0 and i >= 1:
            primes.append(i)
    except ZeroDivisionError as zer:
        pass

print "Primes that traditionally would match the RSA modulus"
print primes
l = primes[1]
m = primes[2]
t = ((l - 1) * (m - 1))
#r = pow(l, 2) + pow(m, 2)
print "Sanity check"
sk2 = multiplicative_inverse(pk, (mod - 1))
print sk2
print pow(c, sk2, mod)
print "Crack attempt"
sk2 = multiplicative_inverse(pk, t)
print sk2
print pow(c, sk2, mod)
