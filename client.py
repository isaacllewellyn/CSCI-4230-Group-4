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
authtype = raw_input('Input your authentication method:\n0:'
             ' ECC\n1: DFH\n2: RSA\n enter the number of your choice: ')
print("Authentication Type: {", authtype,"}")
authtype = int(authtype)
message, key = b'', ''
authenticated = 0
if (authtype == 0):
    message = b'ECC'
    ecc = ECC.ECC(31, 5672, 104729, False)
elif authtype == 1:
    message = b'DFH'
elif authtype == 2:
    message = b'RSA'
    authtype = 4  # fix to allow all
try:
    # Send data
    print('sending {!r}'.format(message))
    sock.sendall(message)
    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    if (authtype == 0):
        g0 = sock.recv(64)
        g1 = sock.recv(64)
        key0 = sock.recv(64)
        key1 = sock.recv(64)
        key = ecc.authinit(np.array([float(g0), float(g1)]))
        sock.sendall(str(key[0]))
        sock.sendall(str(key[1]))
        shared_key = ecc.authconfirm(np.array([float(key0), float(key1)]))[0]
        print("Shared key: ", shared_key)
        authenticated = 1
    if (authtype == 1):
        print("Recving prime from server")
        p = sock.recv(64).decode() # possible thing here
        print("Recived: ", p)
        p = str(p[1:])
        p = int(p.split("p")[0])
        print("Prime: ", p)
        a = diffiehell.generateSecretKey()
        A = diffiehell.generatePublicKey(a, p)
        sock.sendall(str(A).encode())

        B = int(sock.recv(8).decode()) # possible thing here

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
    
    #pick encryption type
    print("continue auth:")
    data = sock.recv(1024)
    print('Client RECV {!r}'.format(data))
    enctype = raw_input('Input your encryption method:\n0:'
             ' bbs\n1: DES\n2: RC4\n enter the number of your choice: ')
    print("Authentication Type: {", enctype,"}")
    sock.sendall(enctype)
    enctype = int(enctype)
    data = sock.recv(1024)
    print('Client RECV {!r}'.format(data))
    
    while authenticated == 1:
        message = str(raw_input("SHELL: "))
        message = mes.encrypt(enctype, message, shared_key)
        sock.sendall(message)
        data = sock.recv(1024)
        data = mes.decrypt(enctype, data, shared_key)
        print('Response {!r}'.format(data))

finally:
    print('closing socket')
    sock.close()
