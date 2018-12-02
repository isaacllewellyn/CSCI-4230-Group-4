#https://pymotw.com/3/socket/tcp.html
#socket_echo_server.py
import socket, message, subprocess
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 11000)
print('Starting up the most secure server on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)


def authenticate(data):
    key = '696969'
    if(data[:3] == 'ECC'):
        print("Attempting ECC authentication")
    if(data[:3] == 'DFH'):
        print("Attempting DiffeHell authentication")
    if(data[:3] == 'SDS'):
        print("Attempting SimpleSimpleDes authentication")
    if(data[:3] == 'BBS'):
        print("Attempting BlumBlumblumBlumBlumShubbibiSubbi authentication")
    return key

Client_Key = ''
while True:
    # Wait for a connection
    print('Waiting for a connection')
    connected = 0
    connection, client_address = sock.accept()
    try:
        print('Connection from client: ', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            print('Received byte message {!r}'.format(data))
            if data:
                if(connected == 0):
                    print('User authentication stage')
                    Client_Key = authenticate(data)
                    data = b'You are connected! Congratulations, enjoy your shell.'
                    connected = 1
                else:
                    print('User Transmission stage')
                    data = message.decrypt(data, Client_Key)
                    data = b'ls'
                    print('Data to run on shell is: ', data)
                    response = subprocess.check_output([data])
                    print('Sending Response: ', response)
                    data = message.encrypt(message, Client_Key)

                connection.sendall(data)
            else:
                print('no data from', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()
