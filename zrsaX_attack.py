from Crypto.Util import number
from zrsaX import keygen, encrypt, decrypt, multiplicative_inverse

sk, pk, mod = keygen()
print sk, pk, mod

import math
crack = int(math.sqrt(mod))
print crack
primes = []
for i in range(crack, crack-1000, -1):
    try:
        if (mod % i) == 0 and i >= 1:
            primes.append(i)
    except ZeroDivisionError as zer:
        pass

print primes
t = ((primes[1] - 1) * (primes[0] - 1) * (primes[2] - 1))
r = (pow(primes[0], 3) + (primes[0] * primes[1]) + primes[2])
print "r", r
#x = number.getRandomRange(1, r)
#y = number.getRandomRange(1, r)
#z = number.getRandomRange(1, r)
#e = ((pow(x, 3) + (x * y) + z))
#print "e", e
#p = number.getRandomRange(1, e)
#q = number.getRandomRange(1, e)
#v = number.getRandomRange(1, e)
#pt = p + q + v
#sk_tmp = (pow(x, 3) + (x * y) + pt)
sk2 = multiplicative_inverse(pk, t)
print sk2
