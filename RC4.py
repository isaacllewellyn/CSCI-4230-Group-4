#RC4 implementation

import struct

#returns a keystream
def RC4(key):
	S = KSA(key)
	return PRGA(S)



#Key scheduling algorithm
def KSA(key):
	keyLen = len(key)
	s = range(256)

	j = 0
	for i in range(256):
		j = (j + s[i] + ord(key[i % keyLen])) % 256
		s[i], s[j] = s[j], s[i]

	return s

#pseudo-random generation algorithm
def PRGA(s):
	i = 0
	j = 0

	while True:
		i = (i+1) % 256
		j = (j + s[i]) % 256

		s[i], s[j] = s[j], s[i]
		k = s[(s[i] + s[j]) % 256]
		yield k


def convertKey(k):
	return struct.pack(">I", k)

def encrypt(message, key):
	key = convertKey(key)
	keyStream = RC4(key)

	cipher = []
	for c in message:
		val = ("%02X" % (ord(c) ^ keyStream.next()))
		cipher.append(val)

	return ''.join(cipher)

def decrypt(cipher, key):

	cipher = cipher.decode('hex')
	plain = encrypt(cipher, key)
	return plain.decode('hex')


def main():
	k1 = 593
	p1 = "Plaintext"

	c1 = encrypt(p1, k1)

	print(p1)
	print(c1)

	p2 = decrypt(c1, k1)

	print(p2)

if __name__ == '__main__':
	main()