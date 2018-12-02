#HMAC implementation
import sha_1.py
from __future__ import print_function
import io
import struct



def addPad(key, size):
	while len(key) < size:
		key += '0'

#Inputs - key - byte array
#		- m - message to be hashed
#		- Hash funciton - SHA-1
#		- blockSize = 64
#		- output size = 20
def hmac(key, m):
	block = 64
	out = 20

	#if key longer than the block, shorten using sha-1
	if len(key) > block:
		key = Hasha1().update(m).hexDigest()

	#if key shorter than block, lengthen using pad of 0s
	if len(key) < block:
		key = addPad(key,block)

	o_key_pad = key ^ (0x5c * block)
	i_key_pad = key ^ (0x36 * block)

	inner = Hasha1().update(i_key_pad + m).hexDigest()
	outer = Hasha1().update(o_key_pad + inner).hexDigest()

	return outer