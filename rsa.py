import sys
import numpy as np
import random
random.seed()

def gcd(a, b):
	if b == 0:
			return a
	else:
		return gcd(b, a%b)

class RSA(object):
    def __init__(self, p, q):
        self.p = p
        self.q = q
        self.n = p*q
        self.lam = ((p-1)*(q-1))//gcd(p-1, q-1)

        # find exponent coprime with lam
        self.e = random.randint(2, self.lam-1)
        while gcd(self.e, self.lam) != 1:
            self.e = random.randint(2, self.lam-1)

        self.d = self.modinv(self.e, self.lam)
    def encrypt(self, msg):
        c = pow(msg, self.e, self.n)
        return c

    def decrypt(self, ctext):
        m = pow(ctext, self.d, self.n)
        return m

    #extended euclidian alg for use in modinv
    def egcd(self, a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = self.egcd(b % a, a)
            return (g, x-(b//a)*y, y)
	
    #computes modular inverse assuming p is prime
    def modinv(self, a, p):
        g, x, y = self.egcd(a%p, p)
        return x % p

rsa = RSA(61, 53)
c = rsa.encrypt(533)
e = rsa.decrypt(c)
print(e)