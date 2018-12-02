import sys
import numpy as np
import math
import random
random.seed()

#WE DEFINE THE INFINITE POINT AS (-1, -1)
inf = np.array([-1, -1])

p = 8831
a = 3
b = 45

#extended euclidian alg for use in modinv
def egcd(a, b):
	if a == 0:
		return (b, 0, 1)
	else:
		g, y, x = egcd(b % a, a)
		return (g, x-(b//a)*y, y)

#computes modular inverse assuming p is prime
def modinv(a, p):
	g, x, y = egcd(a%p, p)
	return x % p
	
#inputs: 2 nparrays of size 2
#ouput: 1 nparray of size 2
def addoverec(p1, p2, a, p):
	x1 = p1[0]
	x2 = p2[0]
	y1 = p1[1]
	y2 = p2[1]
	if np.array_equal(p1, inf):
		return p2
	if np.array_equal(p2, inf):
		return p1
	if x1 == x2 and (y1 != y2 or y1 == 0):
		return inf
	if np.array_equal(p1, p2):
		m = ((3*pow(x1, 2) + a) * modinv(2*y1, p))
		m = m%p
		if(m == 0):
			return inf
	else:
		m = ((y2 - y1) * modinv(x2 - x1, p))
		m = m%p
		if(m == 0):
			return inf
	x3 = pow(m, 2) - x1 - x2
	y3 = (m*(x1 - x3)) - y1
	return np.array([x3%p, y3%p])

def multoverec(p1, x, a, p):
	if x <= 0:
		return
	if x == 1:
		return p1
	p2 = addoverec(p1, p1, a, p)
	x -= 1
	while x > 1:
		p2 = addoverec(p2, p1, a, p)
		x -= 1
	return p2

points = np.zeros((0, 2))

print "computing a list of points"

#obtain a list of points
for i in range(0, p):
	x = pow(i, 3, p)
	x += a*i
	x += b
	x = x%p
	for j in range(0, p):
		if pow(j, 2, p) == x:
			points = np.append(points, [[i, j]], axis=0)

print points
print points.shape
print "randomly picking a key point"
keypoint = points[random.randint(0, points.shape[0]-1)]
print keypoint
secretint = random.randint(2, p)
print "secret int:"
print secretint

print "bpoint:"
bpoint = multoverec(keypoint, secretint, a, p)
print bpoint

#bpoint = keypoint*secretint
#public: keypoint, curve formula, bpoint

#alice
print "msg:"
msg = points[random.randint(0, points.shape[0]-1)]
print msg
#choose a point[msg value]
rand = random.randint(2, p)
while True:
	y2 = multoverec(bpoint, rand, a, p)
	if (np.array_equal(y2, msg) == False):
		break;
	rand = random.randint(2, p)
y1 = multoverec(keypoint, rand, a, p)
print "ciphertext:"
y2 = addoverec(y2, msg, a, p)
print y1
print y2
#chooses a random int
#computes y1 = k*keypoint, y2 = x+k*bpoint

#bob: computes x = y2-secretint*y1
# = y2 + (secretint*y1 (with inverted y))
y1 = multoverec(y1, secretint, a, p)
if (np.array_equal(y1, inf) == False):
	y1 = np.array([y1[0], (-y1[1])%p])
y1 = addoverec(y2, y1, a, p)
print "reconstructed plaintext:"
print y1