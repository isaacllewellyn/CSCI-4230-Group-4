#Sha-1 Implementation

from __future__ import print_function
import struct
import io


class Hasha1(object):

	dig = 20

	def __init__(self):

		self._h = (
            0x67452301,
            0xEFCDAB89,
            0x98BADCFE,
            0x10325476,
            0xC3D2E1F0,
        )

		self._unprocessed = b''

		self._message_byte_length = 0

	def update(self, arg):

		chunk = self._unprocessed + arg[:64]

		while len(chunk) == 64:
			self._h = process_chunk(chunk, *self._h)
			self._message_byte_length += 64
			chunk = arg[:64]

		self._unprocessed = chunk
		return self

	def digest(self):
		return b''.join(struct.pack(b'>I',h) for h in self.produce_digest())

	def hexdigest(self):
		return'%08x%08x%08x%08x%08x' % self.produce_digest()

	def produce_digest(self):

		message = self._unprocessed
		message_byte_length = self._message_byte_length + len(message)

		message += b'\x80'

		message += b'\x80' * ((56 - (message_byte_length + 1) % 64) % 64)

		message_bit_length = message_byte_length * 8
		message += struct.pack(b'>Q', message_bit_length)

		h = process_chunk(message[:64], *self._h)
		if len(message) == 64:
			return h
		return process_chunk(message[64:], *h)




def process_chunk(chunk, h0, h1, h2, h3, h4):
	#ensure chunk len is 64

	assert len(chunk) == 64

	w = [0] * 80

	for i in range(16):
		w[i] = struct.unpack(b'>I', chunk[i * 4:i * 4 + 4])[0]

	for i in range(16, 80):
		w[i] = left_rotate(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1)

	a = h0
	b = h1
	c = h2
	d = h3
	e = h4


	for i in range(80):
		if 0 <= i <= 19:
			f = d ^ (b & (c ^ d))
			k = 0x5A827999
		elif 20 <= i <= 39:
			f = b ^ c ^ d
			k = 0x6ED9EBA1
		elif 40 <= i <= 59:
			f = (b & c) | (b & d) | (c & d)
			k = 0x8F1BBCDC
		elif 60 <= i <= 79:
			f = b ^ c ^ d
			k = 0xCA62C1D6

		a, b, c, d, e = ((left_rotate(a, 5) + f + e + k + w[i]) & 0xffffffff,
						 a, left_rotate(b, 30), c, d)



	h0 = (h0 + a) & 0xffffffff
	h1 = (h1 + b) & 0xffffffff
	h2 = (h2 + c) & 0xffffffff
	h3 = (h3 + d) & 0xffffffff
	h4 = (h4 + e) & 0xffffffff

	return h0, h1, h2, h3, h4


def left_rotate(n, v):
    return ((n << v) | (n >> (32 - v))) & 0xffffffff




def sha1(message):

	return Hasha1().update(message).hexdigest()




def main():

	m = "This message will be hashed"
	m2 = "The quick brown fox jumps over the lazy dog"
	print(m)
	h = sha1(m)
	print(h)

	print(m2)
	h2 = sha1(m2)
	print(h2)

if __name__ == "__main__":
	main()