#RC4 implementation

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
		j = (j + s[i] + key[i % keyLen]) % 256
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
	return [ord(c) for c in k]

def encrypt(message, key):
	key = convertKey(key)
	keyStream = RC4(key)

	cipher = ''
	for c in message:
		cipher += ("%02X" % (ord(c) ^ keyStream.next()))

	return cipher

def decrypt(cipher, key):
	print(cipher)


def main():
	k1 = "Key"
	p1 = "Plaintext"

	c1 = encrypt(p1, k1)

	print(p1)
	print(c1)

if __name__ == '__main__':
	main()