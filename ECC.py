import sys
import numpy as np
import math
import random
random.seed()

class ECC(object):
	def init(self, a, b, p):
		#WE DEFINE THE INFINITE POINT AS (-1, -1)
		self.inf = np.array([-1, -1])
		self.a = a
		self.b = b
		self.p = p
		
		
		
		print "computing a list of points"
		self.points = np.zeros((0, 2))
		
		#obtain a list of points
		for i in range(0, p):
			x = pow(i, 3, p)
			x += a*i
			x += b
			x = x%p
			for j in range(0, p):
				if pow(j, 2, p) == x:
					self.points = np.append(self.points, [[i, j]], axis=0)
		
		print self.points
		print self.points.shape
		print "randomly picking a key point"
		self.keypoint = self.points[random.randint(0, self.points.shape[0]-1)]
		print self.keypoint
		
		print "secret int:"
		self.secretint = random.randint(2, p)
		print self.secretint
		
		print "product:"
		self.bpoint = self.multoverec(self.keypoint, self.secretint)
		print self.bpoint
		
		#bpoint = keypoint*secretint
		#public: keypoint, curve formula, bpoint
		#secret: secretint
		
		pass
	
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
	
	#inputs: 2 nparrays of size 2
	#ouput: 1 nparray of size 2
	def addoverec(self, p1, p2):
		x1 = p1[0]
		x2 = p2[0]
		y1 = p1[1]
		y2 = p2[1]
		if np.array_equal(p1, self.inf):
			return p2
		if np.array_equal(p2, self.inf):
			return p1
		if x1 == x2 and (y1 != y2 or y1 == 0):
			return self.inf
		if np.array_equal(p1, p2):
			m = ((3*x1*x1 + self.a) * self.modinv(2*y1, self.p))
			m = m%self.p
		else:
			m = ((y2 - y1) * self.modinv(x2 - x1, self.p))
			m = m%self.p
		x3 = pow(m, 2) - x1 - x2
		y3 = (m*(x1 - x3)) - y1
		return np.array([x3%self.p, y3%self.p])
	
	def multoverec(self, p1, x):
		if x <= 0:
			return
		if x == 1:
			return p1
		p2 = self.addoverec(p1, p1)
		x -= 1
		while x > 1:
			p2 = self.addoverec(p2, p1)
			x -= 1
		return p2
	
	def encrypt(self, x, keypoint, bpoint):
		#alice's encryption
		print "msg:"
		msg = self.points[x]
		print msg

		print "ciphertext:"
		#computes y1 = k*keypoint, y2 = x+k*bpoint
		rand = random.randint(2, self.p)
		y1 = self.multoverec(keypoint, rand)
		y2 = self.multoverec(bpoint, rand)
		y2 = self.addoverec(y2, msg)
		print y1
		print y2
		return (y1, y2)
	
	def decrypt(self, y1, y2):
		#bob: computes x = y2-secretint*y1
		y1 = self.multoverec(y1, self.secretint)
		if (np.array_equal(y1, self.inf) == False):
			y1 = np.array([y1[0], (-y1[1])%self.p])
		y1 = self.addoverec(y2, y1)
		print "reconstructed plaintext:"
		print y1
	
	def authinit(self, g):
		self.x = random.randint(2, self.points.shape[0]-1)
		return ecc.multoverec(g, self.x)

	def authconfirm(self, g1):
		return ecc.multoverec(g1, self.x)

ecc = ECC()
ecc.init(3, 2, 17)
x = random.randint(0, ecc.points.shape[0]-1)
res = ecc.encrypt(x, ecc.keypoint, ecc.bpoint)
ecc.decrypt(res[0], res[1])

#authentication using ECC, run as many times until results in non-inf point
ecc2 = ECC()
ecc2.init(3, 2, 17)
x1 = ecc.authinit(ecc.keypoint)
print x1
x2 = ecc2.authinit(ecc.keypoint)
print x2
print ecc.x
print ecc2.x
print ecc.authconfirm(x2)
print ecc2.authconfirm(x1)


