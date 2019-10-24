# ZRSAX

ZRSAX is a prototype public key encryption algorithm that is different from RSA.

The goal still is to find the inverse of the totient but identifying the totient is the problem.

# Algorithm principles

Jump, Wash, Cloak

ZRSA and ZRSAX are based off the idea of RSA with some major differences.  The use of the pythagrean theorem and elliptic curve formulas are used in the jump and washing phases.

The algorithm generates a base, jumps off the base and then is washed and cloaked.  Some "curves" are generated as unique values that must be included in the key generation phase, this exchange between washing between R and C and then cloaking with S causes the totient to not respond with a zero when checking the modulus mod totient.  Checking the E curve against the modulus does give a zero but I have not been able to find a way to use that to invert as of this writing.

