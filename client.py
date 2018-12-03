# socket_echo_client.py
import socket
import sys
import message as mes
import ECC, diffiehell
import numpy as np

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 11000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)
print('Welcome to Group 4 Secure Socket Client!')
type = input('Input your authentication method:\n 0:'
             ' ECC\n1: DFH\n2: RSA\n enter the number of your choice: ')
print("Type: {", type,"}")
type = int(type)
message, key = b'', ''
authenticated = 0
if (type == 0):
    message = b'ECC'
    ecc = ECC.ECC(3, 2, 17)
elif type == 1:
    message = b'DFH'
elif type == 2:
    message = b'RSA'
    type = 4  # fix to allow all
try:
    # Send data
    print('sending {!r}'.format(message))
    sock.sendall(message)
    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    if (type == 0):
        g0 = sock.recv(64)
        g1 = sock.recv(64)
        key = ecc.authinit(np.array([float(g0), float(g1)]))
        key0 = sock.recv(64)
        key1 = sock.recv(64)
        sock.sendall(str(key[0]))
        sock.sendall(str(key[1]))
        shared_key = ecc.authconfirm(np.array([float(key0), float(key1)]))[0]
        print("Shared key: ", shared_key)
    if (type == 1):
        p = diffiehell.getsmallprime()
        a = diffiehell.generateSecretKey()
        A = diffiehell.generatePublicKey(a, p)
        B = int(sock.recv(64).decode()) # possible thing here
        sock.sendall(str(A).encode())

        # Generate the shared secrets
        shared_key = pow(B, a, p)
        print("Shared key: ", shared_key)
        authenticated = 1
        #Setup diffi
    # while amount_received < amount_expected:
    #     data = sock.recv(64)
    #     amount_received += len(data)
    #     print('received {!r}'.format(data))

    if (authenticated == 0):
        print('======= User Authentication =======')

        ###TODO

    while authenticated == 1:
        message = input("SHELL: ")
        message = mes.encrypt(type, message, key)
        sock.sendall(message)
        data = sock.recv(1024)
        print('Client RECV {!r}'.format(data))
        data = mes.decrypt(type, message, key)
        print('Response {!r}'.format(data))

finally:
    print('closing socket')
    sock.close()
