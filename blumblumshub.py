#llewi
#Crypto HW 3

import math

def log2(number):
    return int(math.floor(math.log(number,2)))
#Return N, K, and H Page 4 Week 8.2
def get_n_k_and_h(p,q):
    return p*q, log2(p*q), log2(log2(p*q))
#Encrpyt message of size H with set n and random x
def BBS_chunk(message, h, n, x):
    cipher = 0
    #Initiate Blum Goldwasser Probabilistic Encryption Algorithm
    for i in range(int(len(bin(message)) / h) - 1,-1 , -1): #4. Iterate through each block
        mask = 1 << h  # Set mask to field for most signifigant bit.
        mask = mask - 1  # Invert to get least significant bit
        x = pow(x, 2, n)  # 4.1 xi = ((xi-1)^2 mod n)
        Pi = x & mask  # 4.2 Let Pi be the n least significant bits of x
        psudo = message >> (h * i)  # Get pseudorandom bits
        Mi = psudo & mask
        Ci = Pi ^ Mi  # 4.3 Ci = Pi xor our BBS
        cipher <<= h #Add h bits to our msg
        cipher |= Ci #BBS_chunk_encrypt(message, h , n ,x, i)# Encypt them and then OR them together to add Ci to our message
    return cipher, x
#Encrpyt message using p, q, and our 'random' x
def blumgold_encrypt( p, q, xrand, message):
    n, k , h = get_n_k_and_h(p,q)
    x = xrand
    #Page 5 Week 8.2
    cipher, x = BBS_chunk(message, h, n, x)
    x = pow(x, 2, n)
    return cipher, x # We send the other party our ctxt of our msg bits and the final result of x

def blumgold_decrypt( p, q, a, b, xrand, cipher):
    n, k, h = get_n_k_and_h(p, q)
    bs = int(len(bin(message)) / h)
    #Set based off slide 6 week 8.2
    d1 = pow(int((p + 1) / 4), bs + 1, p - 1)
    d2 = pow(int((q + 1) / 4), bs + 1, q - 1)
    u = pow(xrand, d1, p)
    v = pow(xrand, d2, q)
    x0 = (v * a * p + u * b * q) % n
    #Loop thru as before
    #Initiate Blum Goldwasser Probabilistic Decryption Algorithm as before with new x0 for decrpytion
    return BBS_chunk(cipher, h, n ,x0)

#Blum Protocol
p, q, a, b, x = 499, 547, -57, 52, 159201 #Starting Variables
# p, q, a, b, are used to create X/X0
message = int('10011100000100001100', 2) #Convert the binary message to an int
#Our message is given
cipher, x = blumgold_encrypt(p,q ,x, message)#Generate cipher and x to combine and send to other party securely

### 1. What is the ciphertext?
print("Cipher Text", bin(cipher)[2::], " == " , cipher)

### 2. Verify your answer by showing that D(C(m))=m
message1, x = blumgold_decrypt( p, q, a, b, x, cipher)
print("Decrypted Text", bin(message1)[2::], " == " , message1)
print("Equality Check: ", message == message1)