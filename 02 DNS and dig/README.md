Name:  Mickey P. Somra

Programming language and version: Python (version 3.6.4)

Testing environment:
	OS: Windows 7 Professional
	IDE with entrance file:  Python 3.6.4 (Run Module – F5)	
	Used IP and ports: hardcoded (127.0.0.1:6789)	
	Command lines: dig +norecurse @127.0.0.1 -p 6789 <hosotname>

Purpose: This script will create a server to listen on a specific port. The server will be running on IP 127.0.0.1 and port 6789 which are both hardcoded. It responds to a dig request to return the IP address for a hostname. The server will unpack the hostname and query a data structure file which has the stored DNS text file for matching contents. A successful query, will return the answer section, authority section and additional section. 

If a hostname does not exist, the answer section does not print. However, the authority and additional section prints to command prompt. I’m unsure about this part but professor says that’s not important. 

Note: Code format was taken from socketAPI.pdf.

References used:
Working with files from: https://docs.python.org/3/tutorial/inputoutput.html

Reading lines from: https://stackoverflow.com/questions/6213063/python-read-next

Encoding format from: https://stackoverflow.com/questions/9233027/unicodedecodeerror-charmap-codec-cant-decode-byte-x-in-position-y-character

Unpack number from: https://stackoverflow.com/questions/444591/convert-a-string-of-bytes-into-an-int-python

Unpack byte hex from: https://stackoverflow.com/questions/46235001/python-unpack-hex-floating-numbers-from-an-udp-message

Convert decimal to ascii from: https://stackoverflow.com/questions/4387138/pythonascii-character-decimal-representation-conversion

Bitwise shift from: https://www.codecademy.com/en/forum_questions/523edafaabf82109d900617b

Bitwise packing from: Professor.

 

