from Crypto.Util import number

# requires pycrypto

#def findP():
#    while True:
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
    msg = "01234567890ABCDEF"
    m = number.bytes_to_long(msg)
    ctxt = encrypt(m, pk, mod)
    if sk != None:

        ptxt = decrypt(ctxt, sk, mod)
        if ptxt == m:
            return True
        else:
            return False
    return False

def keygen(y=9500312376742331583088991749194050124736697592448250512935268051009042866265607311822644150435880307382824997406646222806092916647296825480010806761125109):
    good = 0
    while good != 1:
        x = number.getRandomRange(1, (y**2))
        g = mygcd(x, y)
        while g != 1:
            x = number.getRandomRange(1, (y ** 2))
            g = mygcd(x, y)
        z = number.getRandomRange(1, y)
        g = mygcd(z, y)
        while g != 1:
            z = number.getRandomRange(1, y)
            g = mygcd(z, y)
        n = x * y * z
        t = ((x - 1) * (y - 1) * (z - 1))
        pk = z
        sk = multiplicative_inverse(z, t)
        if testencrypt(pk, sk, n):
            good = 1
    return sk, pk, n
