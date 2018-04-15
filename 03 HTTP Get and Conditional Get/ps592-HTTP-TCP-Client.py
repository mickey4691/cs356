#!/usr/local/bin/python3

'''
Author: Mickey P. Somra
Last Updated: 03/28/2018
Purpose: This script will create a client that will conduct HTTP request to a
server that will return contents from an HTML file. 
Note: Code format was taken from socketAPI.pdf.
'''

import sys, time
from socket import *

#data = "127.0.0.1:12000/filename.html"
data = input("Enter URL in form IP:port/filename = ")
host, rawData = data.split(":")
port, filename = rawData.split("/")
port = int(port)

#Generating the first Get Request
RequestData = "GET /" + filename + " HTTP/1.1" + "\r\n"
RequestData += host + ":" + str(port) + "\r\n"
RequestData += "\r\n"

# Create TCP client socket. Note the use of SOCK_STREAM for TCP packet
clientSocket = socket(AF_INET, SOCK_STREAM)

# Create TCP connection to server
clientSocket.connect((host, port))

# Send data through TCP connection
clientSocket.send(RequestData.encode())
print("\nFirst request sent, respose below")

# Receive the server response
ResponseData = clientSocket.recv(4096)
ResponseData = ResponseData.decode()

if "HTTP/1.1 404" in ResponseData:
    #if the server returns a 404, that means the file does not exist.
    print(ResponseData)
    clientSocket.close()
else:
    #else, the file exist, as such contents will be printed
    print(ResponseData+"\n")
    clientSocket.close()

    #The client will now generate the conditional get request.
    #Uncomment the next line to slow the client down and modify the file
    #time.sleep(10) 
    
    #Client extracts Last-Modified date to generate the uncoditional get request
    for Data in ResponseData.split("\r\n"):
        if "Last-Modified" in Data:
            LastModDateTimeOld=Data[15:]
    
    #Creating the conditional get request based on 'If-Modified-Since'
    RequestData = "GET /"+ filename +" HTTP/1.1" + "\r\n"
    RequestData += host+":"+str(port)+"\r\n"
    RequestData +="If-Modified-Since: " + LastModDateTimeOld + "\r\n"
    RequestData += "\r\n"
    
    print("\nSecond request sent, respose below")
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((host, port))
    clientSocket.send(RequestData.encode())
    ResponseData = clientSocket.recv(4096)
    ResponseData = ResponseData.decode()
    print(ResponseData)
    clientSocket.close()
