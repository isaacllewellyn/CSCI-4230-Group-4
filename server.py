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
    type = -1
    if(data[:3] == 'ECC'):
        print("Attempting ECC authentication")
        key = message.authenticate(0)
        type = 0
    if(data[:3] == 'DFH'):
        print("Attempting DiffeHell authentication")
        key = message.authenticate(1)
        type = 1
    # if(data[:3] == 'SDS'):
    #     print("Attempting SimpleSimpleDes authentication")
    #     key = message.authenticate(2)
    #     type = 2
    # if(data[:3] == 'BBS'):
    #     print("Attempting BlumBlumblumBlumBlumShubbibiSubbi authentication")
    #     key = message.authenticate(3)
        type = 3
    if (data[:3] == 'RSA'):
        print("Attempting RenssslearSavyAdcryption authentication")
        key = message.authenticate(4)
        type = 4
    return key, type

Client_Key = ''
while True:
    # Wait for a connection
    print('======== INIT SERVER  ========')
    print('Waiting for a connection...')
    connected = 0
    connection, client_address = sock.accept()
    try:
        print('======== INIT USER  ========')
        print('Connection from client: ', client_address)
        # Receive the response and parse it
        while True:
            data = connection.recv(128)
            print('Received byte message {!r}'.format(data))
            if data:
                if(connected == 0):
                    print('======== User Authentication  ========')
                    Client_Key, type = authenticate(data)
                    if(Client_Key == ''):
                        data = b'You failed to authenticate'
                    else:
                        print('Key established.')
                        data = b'Please choose a data encryption type.\n0: BBS\n1: SDS'
                        dtype = input("Enter [0] for BBS or [1] for SDS")
                        data = b'You are connected! Congratulations.'
                        connected = 1
                else:
                    print('======== User Transmission ========')
                    data = message.decrypt(type, data, Client_Key)
                    print('Data to run on shell is: ', data)
                    response = subprocess.check_output([data])
                    print('Sending sub-shell Response: ', response)
                    data = message.encrypt(type, message, Client_Key)
                connection.sendall(data)
            else:
                print('no data from', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()
