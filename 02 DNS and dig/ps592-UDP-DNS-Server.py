#!/usr/local/bin/python3

'''
Author: Mickey P. Somra
Last Updated: 02/14/2018
Purpose: This script will create a server to listen on a specific port (6789);
it responds to a dig request to return the IP address for a hostname.
Note: Code format was taken from socketAPI.pdf.
'''

# command prompt: dig +norecurse @127.0.0.1 -p 6789 host1.student.test

import sys, struct, base64
from socket import *
from struct import *

DNS_init={}
DNS_list={}
counter=0
tempStr=""

#working with files from: https://docs.python.org/3/tutorial/inputoutput.html
#reading lines from: https://stackoverflow.com/questions/6213063/python-read-next
#encoding format from: https://stackoverflow.com/questions/9233027/unicodedecodeerror-charmap-codec-cant-decode-byte-x-in-position-y-character
file = open('dns-master.txt', 'r', encoding="utf8")
lines = file.readlines()

#storing all hostname and values in DNS_list
for i in range(0, len(lines)):    
    if "student.test" in lines[i]:
        if len(lines[i].split()) == 3:
            DNS_list[counter]=(lines[i].split())
            counter+=1
    #END oF Condition
    
#storing DOMAIN header in DNS_init
for i in range(0, len(lines)):
    if "domain" in lines[i]:
        DNS_init["DOMAIN"]=lines[i+1].split()
        break
    #END oF Condition
    
#Storing TTL in DNS_init
for i in range(0, len(lines)):
    if "TTL" in lines[i]:
        DNS_init["TTL"]=lines[i+1].split()
        break
    #END oF Condition
    
#storing authoritive number in DNS_init
DNS_init["AUTH"]=[0]
for key in DNS_list:
    if "NS" in  DNS_list[key]:
        DNS_init["AUTH"][0]+=1
    #END oF Condition

file.close() # end of file operation.

# hardcoded local ip and port.
serverIP = '127.0.0.1'
serverPort = 6789
dataLen = 1000000

# Create a UDP socket. Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Assign IP address and port number to socket
serverSocket.bind((serverIP, serverPort))
print('The server is ready to receive on port: ' + str(serverPort))

while True:    
    # Receive socket information and storing it as is.
    rawData, address = serverSocket.recvfrom(dataLen)
    
    #unpack number from: https://stackoverflow.com/questions/444591/convert-a-string-of-bytes-into-an-int-python
    ID = (struct.unpack_from("!H", rawData, 0)[0])
    
    #unpack byte hex from: https://stackoverflow.com/questions/46235001/python-unpack-hex-floating-numbers-from-an-udp-message
    decimal_data = struct.unpack_from('!24B', rawData, 12)

    hostname=""
    char=""
    hostArray=[]
    for num in decimal_data:
        #convert decimal to ascii from: https://stackoverflow.com/questions/4387138/pythonascii-character-decimal-representation-conversion
        char = chr(num)
        if ( char.isdigit() or char.isalpha() ):
            hostname+=chr(num)
        else:
            hostname+="."
        #END oF Condition

    #storing the hostname only if it contains a letter or digit (this ensures that a hostname is lengthy)
    while True:
        if ( (hostname[0].isalpha()) and (hostname[len(hostname) - 1].isalpha()) ):
            break
        if not(hostname[len(hostname) - 1].isalpha()):
            hostname = hostname[:-1]
        if not(hostname[0].isalpha()):
            hostname = hostname[1:]
        #END oF Condition
    
    hostArray.append(hostname) #ensuring that hostArray will always be one (this works well for dig overhead check)
    
    #checking the data structure for hostname match
    record=[]
    RCODE=0
    
    for keyFirst in DNS_list:
        if ( ( hostname == DNS_list[keyFirst][0] ) and ("A" == DNS_list[keyFirst][1] )):
            record.append(DNS_list[keyFirst])
        elif ( ( hostname == DNS_list[keyFirst][0] ) and ("CNAME" == DNS_list[keyFirst][1] )):
            record.append(DNS_list[keyFirst])
            for keySecond in DNS_list:
                if ( ( DNS_list[keyFirst][2] == DNS_list[keySecond][0] ) and ("A" == DNS_list[keySecond][1] )):
                    record.append(DNS_list[keySecond])
                    # print("Record found =",record)
                
    QR=1 #Set to 1 for repsonse.

    if len(record) > 0:
        RCODE=0
    else:
        RCODE=3

    AA = 0
    for key in DNS_list:
        if hostname in DNS_list[key]:
            AA = 1
            
    #building DNS packet to send to command prompt
    #building dns from: https://stackoverflow.com/questions/24814044/having-trouble-building-a-dns-packet-in-python
    QDCOUNT = 0
    if (len(hostArray)==1):
        QDCOUNT=1
    
    ANCOUNT = len(record)
    NSCOUNT = DNS_init["AUTH"][0]

        
    # adding NS hostnames and reference to IP for additional section.
    nsLIST=[]
    for keyFirst in DNS_list:
        if DNS_list[keyFirst][1] == "NS":
            for keySecond in DNS_list:
                if DNS_list[keyFirst][2] == DNS_list[keySecond][0]:
                    nsLIST.append(DNS_list[keySecond])
                
    ARCOUNT = len(nsLIST)
 
    DNSpacket = struct.pack("!H", ID)     #ID Packing
    bitRow = 0  
    # bitwise shift from: https://www.codecademy.com/en/forum_questions/523edafaabf82109d900617b
    # bit packing from: Professor.
    bitRow += AA << 15
    bitRow += QR << 13
    bitRow += RCODE    
    DNSpacket += struct.pack("!H", bitRow)
    DNSpacket += struct.pack("!HHHH", QDCOUNT, ANCOUNT, NSCOUNT, ARCOUNT)
    # Building Question Section
    for QNAMEpart in hostname.split("."):
        DNSpacket += struct.pack("!B", len(QNAMEpart))
        for byte in bytes(QNAMEpart.encode()):
            DNSpacket += struct.pack("!B", byte)
    DNSpacket += struct.pack("!B", 0)  # End of String
    DNSpacket += struct.pack("!H", 1)  # Query Type
    DNSpacket += struct.pack("!H", 1)  # Query Class
    
    #record is an array of record found.
    IP = []
    TTL = int(DNS_init["TTL"][0])
    if len(record) == 1: #packing A value
        for part in record[0][0].split("."):   # hostname 
            DNSpacket += struct.pack("!B", len(part))
            for byte in bytes(part.encode()):
                DNSpacket += struct.pack("!B", byte)
        DNSpacket += struct.pack("!B", 0)  # End of String
        DNSpacket += struct.pack("!H", 1)  # Query Type
        DNSpacket += struct.pack("!H", 1)  # Query Class
        DNSpacket += struct.pack("!i", TTL)  # TTL
        DNSpacket += struct.pack("!H", 4)   # RD Length - A Type to provide 32 bit IP
        for ipPart in record[0][2].split("."):    # IP address
            IP.append(int(ipPart))
        DNSpacket += struct.pack("!BBBB", IP[0], IP[1], IP[2], IP[3])
    elif len(record) == 2: #packing CNAME value
        for part in record[0][0].split("."):   # hostname CNAME Record
            DNSpacket += struct.pack("!B", len(part))
            for byte in bytes(part.encode()):
                DNSpacket += struct.pack("!B", byte)
        DNSpacket += struct.pack("!B", 0)  # End of String
        DNSpacket += struct.pack("!H", 5)  # Query Type
        DNSpacket += struct.pack("!H", 1)  # Query Class
        DNSpacket += struct.pack("!i", TTL)  # TTL
        DNSpacket += struct.pack("!H", ( len(record[0][2]) + 2) )   # RD Length - A Type to provide # for cname
        for part in record[0][2].split("."):   # hostname 
            DNSpacket += struct.pack("!B", len(part))
            for byte in bytes(part.encode()):
                DNSpacket += struct.pack("!B", byte)
        DNSpacket += struct.pack("!B", 0)
        
        for part in record[1][0].split("."):   # hostname with actual IP record
            DNSpacket += struct.pack("!B", len(part))
            for byte in bytes(part.encode()):
                DNSpacket += struct.pack("!B", byte)
        DNSpacket += struct.pack("!B", 0)  # End of String
        DNSpacket += struct.pack("!H", 1)  # Query Type
        DNSpacket += struct.pack("!H", 1)  # Query Class
        DNSpacket += struct.pack("!i", TTL)  # TTL
        DNSpacket += struct.pack("!H", 4)   # RD Length - A Type to provide 32 bit IP
        for ipPart in record[1][2].split("."):    # IP address
            IP.append(int(ipPart))
        DNSpacket += struct.pack("!BBBB", IP[0], IP[1], IP[2], IP[3])
        
    # Authority
    for key in DNS_list:
        if DNS_list[key][1] == "NS":
            for part in DNS_list[key][0].split("."):  
                if (len(part) > 0 ):
                    DNSpacket += struct.pack("!B", len(part))
                    for byte in bytes(part.encode()):
                        DNSpacket += struct.pack("!B", byte)
            DNSpacket += struct.pack("!B", 0)  # End of String
            DNSpacket += struct.pack("!H", 2)  # Query Type
            DNSpacket += struct.pack("!H", 1)  # Query Class
            DNSpacket += struct.pack("!i", TTL)  # TTL
            DNSpacket += struct.pack("!H", ( len(DNS_list[key][2]) + 2 ) )   # RD Length - A Type to provide # for cname
            for part in DNS_list[key][2].split("."):   # hostname 
                DNSpacket += struct.pack("!B", len(part))
                for byte in bytes(part.encode()):
                    DNSpacket += struct.pack("!B", byte)
            DNSpacket += struct.pack("!B", 0)

    # Additional
    for i in range(0, len(nsLIST)):
        for part in nsLIST[i][0].split("."):  
            DNSpacket += struct.pack("!B", len(part))
            for byte in bytes(part.encode()):
                DNSpacket += struct.pack("!B", byte)
        DNSpacket += struct.pack("!B", 0)  # End of String
        DNSpacket += struct.pack("!H", 1)  # Query Type
        DNSpacket += struct.pack("!H", 1)  # Query Class
        DNSpacket += struct.pack("!i", TTL)  # TTL
        DNSpacket += struct.pack("!H", 4)   # RD Length - A Type to provide 32 bit IP
        IP=[]
        for ipPart in nsLIST[i][2].split("."):    # IP address
            IP.append(int(ipPart))
        DNSpacket += struct.pack("!BBBB", IP[0], IP[1], IP[2], IP[3])
        

    #Sending DNSpack to command prompt
    serverSocket.sendto(DNSpacket,address)
  
    print("DNS Responded\n")
    
serverSocket.close()
