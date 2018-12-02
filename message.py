import random, time
#Simple helper methods
#Get random data of length
import sdes as des
import rsa as rsa
import blumblumshub as bbs
import ECC as ecc
import diffiehell as dfh

def getNonce(length):
    return ''.join([str(random.randint(0, 9)) for i in range(length)])

#Get timestamp used for nonce
def generate_timestamp():
    """Get seconds since epoch (UTC)."""
    return str(int(time.time()))

def getBuffer():
    return generate_timestamp() + getNonce(8)

def authenticate(enc_type):
    """return authenticate key  and success message"""
    if enc_type == 2:
        key = des.authenticate()
    elif enc_type == 4:
        key = rsa.authenticate()
    elif enc_type == 3:
        key = bbs.authenticate()
    elif enc_type == 0:
        key = ecc.authenticate()
    elif enc_type == 1:
        key = dfh.authenticate()
    return key, 1
def encrypt(enc_type, message, key):
    if enc_type == 2:
        message = des.encrypt(message, key)
    elif enc_type == 4:
        message = rsa.encrypt(message, key)
    elif enc_type == 3:
        message = bbs.encrypt(message, key)
    elif enc_type == 0:
        message = ecc.encrypt(message, key)
    elif enc_type == 1:
        message = dfh.encrypt(message, key)
    return message, 1
def decrypt(dec_type, message, key):
    if dec_type == 0:
        plain = ecc.decrypt(message, key)
    return plain
