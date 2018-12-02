#socket_echo_client.py
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 11000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)
print('Welcome to Group 4 Secure Socket Client!')
type = input('Input your authentication method:\n 1:'
             ' ECC\n2: DFH\n3: RSA\n enter the number of your choice: ')
message = ''
authenticated = 0
if(type == 1):
    message = b'ECC'
elif type == 2:
    message = b'DFH'
elif type == 3:
    message = b'RSA'
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

    while authenticated == 1:
        input("SHELL: ")
        
finally:
    print('closing socket')
    sock.close()
