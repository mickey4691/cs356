#!/usr/local/bin/python3

'''
Author: Mickey P. Somra
Last Updated: 01/29/2018
Purpose: This script will create a server to listen on a specific port;
it randomly respond to a client's request.
It also make use of struct packing and unpacking of networking big endians
Note: Code format was taken from socketAPI.pdf
'''

# using python built in functions
import sys, time
from socket import *
from random import randint
from struct import *

#IP and Port for the server to listen on
serverIP = '127.0.0.1'
serverPort = 12001
dataLen = 1000000

# Create a UDP socket. Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Assign IP address and port number to socket
serverSocket.bind((serverIP, serverPort))

print('The server is ready to receive on port: ' + str(serverPort))

# loop forever listening for incoming datagram messages
while True:
    #randome from: https://docs.python.org/3/library/random.html
    num = randint(1, 10) #Generating random integers between 1 and 10
    
    # Receiving the data sent over the client.
    data, address = serverSocket.recvfrom(dataLen)
    #unpack from https://docs.python.org/3/library/struct.html
    msg_type, seq_num = unpack("!ii", data) #unpacking 2 4-bytes integers that was sent via networking standards

    time.sleep(0.5) #This is used to slow down server
    
    # Respond back to client if num>=4
    if (num>=4):
        print("Responding to ping request with sequence number " + str(seq_num) )
        #pack from: https://docs.python.org/3/library/struct.html
        data = pack('!ii', 2, seq_num) #packing the response and sequence number that was originally received
        serverSocket.sendto(data,address)
    else: #will not respond to client if random number is less than 4.
        print("Message with sequence number " + str(seq_num) + " dropped")
