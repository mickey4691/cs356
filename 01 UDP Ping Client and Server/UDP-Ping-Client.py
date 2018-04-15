#!/usr/local/bin/python3

'''
Author: Mickey P. Somra
Last Updated: 01/29/2018
Purpose: This script will create a client connection that will send data
to a server and port. If the server is running it will respond to this client.
This is a simulation of how ping works.
Note: Code format was taken from socketAPI.pdf
'''
import socket
import sys, time
from socket import *
from struct import *

# Get the server hostname, port to start ping sequence

hostname=input("Enter hostname or IP: ")
port=int(input("Enter port: "))

# Create client socket. SOCK_DGRAM is used for UDP
clientsocket = socket(AF_INET, SOCK_DGRAM)
#socket timeout from:  https://docs.python.org/3/library/socket.html
clientsocket.settimeout(1)  #setting timeout to 1 second

# initializing variable that will be used throughout in the code
dataEcho=""
seq_num=0
RTT=[]  # this will store all time for each ping request in array format
time_taken = 0.0 
start_time = 0.0     
packets_recv=0 

#string format from https://www.learnpython.org/en/String_Formatting
print("Pinging %s, %d" % (hostname, port))

while (True):
    # bult-in time from: https://docs.python.org/3/library/time.html
    start_time=time.time() #get current time for new sequence/ping 
    seq_num+=1  #incrementing sequence
    # pack from: https://docs.python.org/3/library/struct.html
    data = pack('!ii', 1, seq_num)  #packing sequence using struct big endian format
    clientsocket.sendto(data,(hostname, port))
    # handling exception from: https://docs.python.org/3/tutorial/errors.html#handling-exceptions
    # timeout and socket error from: Handling all timeout and socket error => https://forum.micropython.org/viewtopic.php?t=2688
    try:
        dataEcho, address = clientsocket.recvfrom(1024)
        time_taken = time.time() - start_time
        RTT.append(time_taken) #appending the time based on packet number
        #unpack from: https://docs.python.org/3/library/struct.html
        msg_type, seq_rcv = unpack("!ii", dataEcho) # getting the seq number from server
        print ( "Ping message number %d RTT: %f seconds" % (seq_rcv, time_taken) )
        packets_recv+=1  #increment successful packets received
    except Exception:
        # This will handle all socket error and/or timeout error.
        print ( "Ping message number %d timed out" % (seq_num) )        
    if (seq_num==10):
        break #quit while loop
    # time.sleep(1) #Delay program by one second for debugging
    # End of while loop
        
#Close the client socket
clientsocket.close()

#Generating packet lost, statistics and Round Trip Time Data
packet=seq_num
packets_lost = packet - packets_recv
lost_percent = ( (float(packets_lost) / packet) * 100 )
lost_percent = int(lost_percent)

print("\nPing statistics for %s" % (hostname))
#escape % from: https://stackoverflow.com/questions/10678229/how-can-i-selectively-escape-percent-in-python-strings
print("Packets: Sent=%d, Received=%d, Lost=%d (%d%% Loss)" % (packet, packets_recv, packets_lost, lost_percent))

#float conversion from: https://stackoverflow.com/questions/8568233/print-float-to-n-decimal-places-including-trailing-0s
print("The Minimum RTT is: %.6f seconds" % (min(RTT)))
print("The Maximum RTT is: %.6f seconds" % (max(RTT)))
print("The Average RTT is: %.6f seconds" %(( sum(RTT) / packets_recv)) )


# EOF=raw_input("Press enter to continute:") uncomment to run as terminal based
