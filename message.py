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

def message(enc_type, data, key):
    """return encrypted string and success message"""
    if enc_type == "des":
        enc = des.encrypt(data, key)
    elif enc_type =="rsa":
        enc = rsa.encrypt(data, key)
    elif enc_type =="bbs":
        enc = bbs.encrypt(data, key)
    elif enc_type == "ecc":
        enc = ecc.encrypt(data, key)
    return (enc, 1)
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
    return key
def encrypt(message, key):
    return 1
def decrypt(message, key):
    return 1
