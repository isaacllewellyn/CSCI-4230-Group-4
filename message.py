import random, time
#Simple helper methods
#Get random data of length
def getNonce(length):
    return ''.join([str(random.randint(0, 9)) for i in range(length)])
#Get timestamp used for nonce
def generate_timestamp():
    """Get seconds since epoch (UTC)."""
    return str(int(time.time()))
def getBuffer():
    return generate_timestamp() + getNonce(8)
def encrypt(message, key):
    return 1
def decrypt(message, key):
    return 1