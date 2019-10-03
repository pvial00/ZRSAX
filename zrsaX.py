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
    msg = "Hi"
    #msg = "012345678901234567890"
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
    y = 1218141
    y = 171151
    y = 1012761
    y = 1095713
    y = 9050205
    y = 33046797361
    o = 8
    good = 0
    while good != 1:
        x = number.getRandomRange(1, (y**o))
        g = mygcd(x, y)
        while g != 1:
            x = number.getRandomRange(1, (y ** o))
            g = mygcd(x, y)
        z = number.getRandomRange(1, x)
        g = mygcd(z, x)
        while g != 1:
            z = number.getRandomRange(1, x)
            g = mygcd(z, x)
        n = x * y * z
        r = (pow(x, o) * pow(z, o))
        t = (((x - 1) * (y - 1) * (z - 1)) * (r - 1))
        pk = r
        sk = multiplicative_inverse(r, t)
        if pk != None:
            if testencrypt(pk, sk, n):
                good = 1
    return sk, pk, n
