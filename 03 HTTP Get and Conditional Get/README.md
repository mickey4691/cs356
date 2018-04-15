Name:  Mickey P. Somra

Programming language and version: Python (version 3.6.4)

Testing environment:

	OS: Windows 7 Professional
	IDE with entrance file:  Python 3.6.4 (Run Module – F5)	
	Used IP and ports: (127.0.0.1:12000)	
	Command lines: N/A

Purpose: There are two scripts used in order to get data from an HTML file. The two scripts are client and server. There are three formats returned based on the GET request and these are:
1.	Status 404: File was not found, 
2.	Status 200: File found and the initial contents are printed, or
3.	Status 304: File found but the contents were not modified since a particular date so no data is displayed.

The client will send an initial get request by input the host/IP of the server, the port and the filename in the format host:port/filename. The exact input used to test was 127.0.0.1:12001/filename.html. Based on this, the client will send a GET request to the server to the get contents of the filename. The server will check to see if the file exist. If the server responds that the file does not exist, the client will print that information and exit. 
However, if the file exist, the server will need to handle the request based on a Get or Conditional Get method. 
Firstly, the server will check the client’s request for the GET format. If there is the “Last-Modified-Since” in the request, then it is a Conditional Get and if there no “Last-Modified-Since” string, then it is an initial GET request. The server will ensure that the file exist before sending the response of the contents if it is the initial GET request. For the response, it will send the HTTP version, the request date, the modified date, the content length, content type and the actual contents of the HTML. If the “Last-Modified-Since” from the conditional GET is the same date of when the HTML file was modified, then the response will indicate that the file has not been modified and as such it will not return the contents. The client incorporates a delay function to quickly modify the contents before the Conditional Get request is sent and in such, the proper implementation is displayed.

Note: Code format was taken from socketAPI.pdf.

References used:

Reading html from: https://stackoverflow.com/questions/27243129/how-to-open-html-file

Working with date/time from: Professor's hints

File exist from: https://docs.python.org/3/library/os.path.html

 

