#HMAC implementation

from __future__ import print_function
import sha_1
import io
import struct
import string


trans_5C = bytes((x ^ 0x5C) for x in range(256))
trans_36 = bytes((x ^ 0x36) for x in range(256))



def addPad(key, size):
	while len(key) < size:
		key += '0'
	return key

#Inputs - key - byte array
#		- m - message to be hashed
#		- Hash funciton - SHA-1
#		- blockSize = 64
#		- output size = 20
def hmac(key, m):
	key2 = ""
	for i in range(0, 10):
		key2 = key2 + str((int(key)/pow(2, i)) % 2)
	block = 64
	out = 20
	#if key longer than the block, shorten using sha-1
	if len(key2) > block:
		key2 = Hasha1().update(m).hexDigest()

	#if key shorter than block, lengthen using pad of 0s
	if len(key2) < block:
		key2 = addPad(key2,block)

	tbl1 = string.maketrans(trans_5C, trans_5C)
	tbl2 = string.maketrans(trans_36, trans_36)

	o_key_pad = key2.translate(tbl1)
	i_key_pad = key2.translate(tbl2)


	preIn = i_key_pad + m
	inner = sha_1.sha1(preIn)
	preOut = o_key_pad + inner
	outer = sha_1.sha1(preOut)

	return outer


def main():

	m = "The quick brown fox jumps over the lazy dog"
	k = b'key'



	h = hmac(k,m)
	
	print(m)
	print("HMAC :")
	print(h)
	print(len(h))

if __name__ == "__main__":
	main()