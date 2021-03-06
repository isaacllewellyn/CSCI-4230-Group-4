import random, time
#Simple helper methods
#Get random data of length
import sdes as des
import rsa as rsa
import blumblumshub as bbs
import ECC as ecc
import diffiehell as dfh
import hmac
import RC4

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
        message = bbs.encrypt(message, key)
    elif enc_type == 0:
        message = des.encrypt(message, key)
    elif enc_type == 1:
        message = RC4.encrypt(message, key)
    message = message + str(hmac.hmac(key, message))
    return message
def decrypt(dec_type, message, key):
    mac = message[-40:]
    message = message[:-40]
    if dec_type == 2:
        message = ecc.decrypt(message, key)
    elif dec_type == 0:
        message = des.decrypt(message, key)
    elif dec_type == 1:
        message = RC4.decrypt(message, key)
    if(hmac.hmac(key, message) == mac):
		return -1
    return message
