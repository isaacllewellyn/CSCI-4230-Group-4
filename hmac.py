#HMAC implementation
import sha_1.py
from __future__ import print_function
import io
import struct

#Inputs - key - byte array
#		- m - message to be hashed
#		- Hash funciton - SHA-1
#		- blockSize = 64
def hmac(key, m):
	block = 64
