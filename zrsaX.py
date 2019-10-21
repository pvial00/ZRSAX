from Crypto.Util import number

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

def testencrypt(pk, sk, mod):
    #msg = "012345678901234567890"
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

def keygen():
    good = 0
    psize = 512
    while good != 1:
        k = number.getPrime(psize)
        l = number.getPrime(psize)
        m = number.getPrime(psize)
        n = k * l * m
        r = (pow(k, 3) + (k * l) + m)
        t = (((l - 1) * (m - 1) * (k - 1)))
        x = number.getRandomRange(1, r)
        y = number.getRandomRange(1, r)
        z = number.getRandomRange(1, r)
        e = ((pow(x, 3) + (x * y) + z))
        p = number.getRandomRange(1, e)
        q = number.getRandomRange(1, e)
        v = number.getRandomRange(1, e)
        pt = number.getRandomRange(1, e)
        g = mygcd(pt, e)
        while g != 1:
            pt = number.getRandomRange(1, e)
            g = mygcd(pt, e)
            if g == 1:
                break
        _pk = pt
        _sk = multiplicative_inverse(_pk, e)
        pk = _sk
        sk = multiplicative_inverse(pk, t)
        if pk != None:
            if testencrypt(pk, sk, n):
                good = 1
    return sk, pk, n
