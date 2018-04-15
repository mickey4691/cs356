#!/usr/local/bin/python3

'''
Author: Mickey P. Somra
Last Updated: 03/28/2018
Purpose: This script will create a server that will respond to HTTP request by returning
the contents from an HTML File. It returns data on 3 cases:
1. File does not exist
2. File exist as such, contents is responded.
3. File exist but it has not been modified since.
Note: Code format was taken from socketAPI.pdf.
'''


import os, datetime, time, os.path, codecs
from socket import *
serverIP = '127.0.0.1'
serverPort = 12000
dataLen = 1000000

#Function to get modified date
def GetLastMod(FileName):
    secs = os.path.getmtime(filename)
    #Working with date from: Professor's hints
    t = time.gmtime(secs)
    last_mod_time = time.strftime("%a, %d %b %Y %H:%M:%S GMT", t)
    return last_mod_time

#function to get contents of the html file.
def GetContentData(FileName):
    #reading html from: https://stackoverflow.com/questions/27243129/how-to-open-html-file
    FormatHTML=''
    f=codecs.open("filename.html", 'r', encoding='utf-8')
    Data = f.read()

    for Line in Data.split("\n"):
        if '<p class="p1">' in Line:
            FormatHTML+= Line
    
    FormatHTML=FormatHTML.replace('<p class="p1">', '')
    FormatHTML=FormatHTML.replace('</p>','')
    FormatHTML=FormatHTML.replace('&lt;','<')
    FormatHTML=FormatHTML.replace('&gt;','>')

    return FormatHTML

# Create a TCP "welcoming" socket. Notice the use of SOCK_STREAM for TCP packets
serverSocket = socket(AF_INET, SOCK_STREAM)

# Assign IP address and port number to socket
serverSocket.bind((serverIP, serverPort))

# Listen for incoming connection requests
serverSocket.listen(1)
print('The server is ready to serve on port: ' + str(serverPort))
LastModDateTimeOld=''
# loop forever listening for incoming connection requests on "welcoming" socket
while True:
    ResponseData=''
    # Accept incoming connection requests, and allocate a n ew socket for data communication
    connectionSocket, address = serverSocket.accept()
    #rint("Request from client " + address[0] + ", " + str(address[1]))
    
    # Receive and print the client data in bytes from "data" socket
    RequestData = connectionSocket.recv(dataLen).decode()

    #time programming from: professor's hints
    t = datetime.datetime.utcnow()
    RequestDateTime = t.strftime("%a, %d %b %Y %H:%M:%S GMT")
    print("Request received")
    
    RequestLineCount=0
    # will need to get lines of client get request:
    for Line in RequestData.split("\r\n"):
        RequestLineCount+=1

    #when the line is 5, we are receiving a conditional get.
    #as such we extract the modified since date from client.
    if RequestLineCount==5:
        for Line in RequestData.split("\r\n"):
            if "If-Modified-Since" in Line:
                LastModDateTimeOld = Line[19:]
    else:
        LastModDateTimeOld=''

    #Extracting filename from initial Request.
    for item in RequestData.split():
        if item[0] == "/":
            filename = item[1:]
            break
 
    #file exist from: https://docs.python.org/3/library/os.path.html
    if not(os.path.isfile(filename)):
        #If the file does not exist, a response will be generated.
        ResponseData += "HTTP/1.1 404 Not Found" + "\r\n"
        ResponseData += "Date: " + RequestDateTime + "\r\n"
        ResponseData += "\r\n"
    else:
        #Here the file exist but will need to respond to either Get or conditional get
        LastModDateTimeCurr = GetLastMod(filename)
        if LastModDateTimeCurr == LastModDateTimeOld:
            #here the LastModDateTimeOld was received from client
            #since it is the same date/time as the file, there's no modification.
            ResponseData += "HTTP/1.1 304 Not Modified\r\n"
            ResponseData += "Date: " + RequestDateTime + "\r\n"
            ResponseData += "\r\n"
        else:
            #will generate the a response with contents.
            ContentData = GetContentData(filename)
            ContentLength = str(len(ContentData))
            ResponseData += "HTTP/1.1 200 OK" + "\r\n"
            ResponseData += "Date: " + RequestDateTime  + "\r\n"
            ResponseData += "Last-Modified: " + LastModDateTimeCurr + "\r\n"
            ResponseData += "Content-Length: " + ContentLength + "\r\n"
            ResponseData += "Content-Type: text/html; charset=UTF-8" + "\r\n"
            ResponseData += "\r\n" + ContentData
    
    # Echo back to client
    connectionSocket.send(ResponseData.encode())
    print("Response sent!")

    connectionSocket.close()

