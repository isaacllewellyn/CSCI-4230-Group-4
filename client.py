#socket_echo_client.py
import socket
import sys
import message as mes

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 11000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)
print('Welcome to Group 4 Secure Socket Client!')
type = input('Input your authentication method:\n 0:'
             ' ECC\n1: DFH\n2: RSA\n enter the number of your choice: ')
message, key = '', ''
authenticated = 0
if(type == 0):
    message = b'ECC'
elif type == 1:
    message = b'DFH'
elif type == 2:
    message = b'RSA'
    type = 4 #fix to allow all
try:
    # Send data
    message = message + b': and this will be sent to the server.'
    print('sending {!r}'.format(message))
    sock.sendall(message)
    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(64)
        amount_received += len(data)
        print('received {!r}'.format(data))

    if(authenticated == 0):
        print('======= User Authentication =======')
        ###TODO

    while authenticated == 1:
        message = input("SHELL: ")
        message = mes.encrypt(type,message,key)
        sock.sendall(message)
        data = sock.recv(1024)
        print('Client RECV {!r}'.format(data))
        data = mes.decrypt(type,message,key)
        print('Response {!r}'.format(data))

finally:
    print('closing socket')
    sock.close()
