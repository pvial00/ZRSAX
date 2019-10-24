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
    psize = 48
    o = 2
    while good != 1:
        # Our example primes L, M and the cloaking prime K
        k = 17
        l = 13
        m = 11
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
        # Create our modulus which is the product of the C curve and the square root of the Base Modulus
        n = (c * long(math.sqrt(a)))
        # Create our totient which is composed of E - 1 and the Square root of the base modulus - 1
        sq = long(math.sqrt(a))
        s = ((c - 1) * (long(math.sqrt(a)) -1))
        # Find a number in the totient field that is coprime to the totient
        pk = (number.getRandomRange(1, s))
        g = number.GCD(pk, s)
        while g != 1:
            pk = (number.getRandomRange(1, s))
            g = number.GCD(pk, s)
            if g == 1:
                break
        # Find the secret key using the totient S
        sk = number.inverse(pk, s)
        # Test if we can encrypt successfully
        if pk != None:
            if testencrypt(pk, sk, n):
                good = 1
    return sk, pk, n, s, e, r, c, a, sq

msg = "Hi"
m = number.bytes_to_long(msg)
print m
sk, pk, mod, s, e, r, c, a, sq =  keygen()
print sk, pk, mod
ctxt = encrypt(m, pk, mod)
print ctxt
p = decrypt(ctxt, sk, mod)
print p

import math
crack = int(math.sqrt(math.sqrt(mod)))
print "crack", crack

primes = []
ceiling = 500000
start = 1
inc = 1
for i in range(start, ceiling, inc):
#for i in range(crack, 6500, 1):
    #print i, mod % i
    #if i == t:
    #    print mod & i
    #if i == s:
    #    print mod & i
    #if i == l:
    #    print mod & i
    try:
        if (mod % i) == 0 and i >= 1:
            primes.append(i)
    except ZeroDivisionError as zer:
        pass

print primes
t = ((e - 1) )
print "Check e - 1"
sk2 = multiplicative_inverse(pk, t)
print sk2
print "Modulus sanity check"
print decrypt(ctxt, sk2, mod)
sk2 = multiplicative_inverse(pk, mod)
print sk2
print decrypt(ctxt, sk2, mod)
print "Modulus - 1 sanity check"
sk2 = multiplicative_inverse(pk, (mod - 1))
print sk2
print decrypt(ctxt, sk2, mod)
print "Check e"
sk2 = multiplicative_inverse(pk, e)
print sk2
print decrypt(ctxt, sk2, mod)
print "Check S, this should always decrypt the message"
sk2 = multiplicative_inverse(pk, s)
print sk2
print decrypt(ctxt, sk2, mod)
print "S ", s
print "mod mod E"
print mod % e
print "mod mod R"
print mod % r
print "mod mod S"
print mod % s
print "mod mod C"
print mod % c
print "mod mod A"
print mod % a
print "mod mod sq"
print mod % sq
print "Solve"
s = ((c - 1) * (sq - 1))
sk2 = multiplicative_inverse(pk, s)
print sk2
print decrypt(ctxt, sk2, mod)
