Name:  Mickey P. Somra

Programming language and version: Python (version 3.6.4)

Testing environment:
	OS: Windows 7 Professional
	IDE with entrance file:  Python 3.6.4 (Run Module – F5)		
	Command lines: N/A

Purpose: The two scripts demonstrate a basic network ping emulation where a client sends encoded data to a server, the server receives and unpack the data and returns a new packaged data to which the client receives and unpacks. Additionally, the client checks the round trip time from when the client sends and receives data to/from the server.  Moreover, the server is programmed to randomly ignore a return packet and as such the client handles this as a failed packet/time out, and calculates the statistics of packets sent and lost. 

References used:
String formatting => https://www.learnpython.org/en/String_Formatting

Socket timeout => https://docs.python.org/3/library/socket.html

Handling exception => https://docs.python.org/3/tutorial/errors.html#handling-exceptions

Handling all timeout and socket error => https://forum.micropython.org/viewtopic.php?t=2688

Escape % => https://stackoverflow.com/questions/10678229/how-can-i-selectively-escape-percent-in-python-strings

Import random => https://docs.python.org/3/library/random.html

Packing data in for networking 4-bytes order => https://docs.python.org/3/library/struct.html

No. of decimals in float => https://stackoverflow.com/questions/8568233/print-float-to-n-decimal-places-including-trailing-0s

Time function => https://docs.python.org/3/library/time.html
