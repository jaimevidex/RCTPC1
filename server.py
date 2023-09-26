

"""
• open – The client sends the string open followed by a space and a 5-digit port number. 
The server replies with the byte array corresponding to the strings ack or nack.

• close – The client sends the string close. 
The server replies with the byte array corresponding to the strings ack or nack.

• get – The client sends the string get followed by a space and the name of the file in the server’s file system. 
The server replies nack if the named file does not exist or ack in the opposite case.
If the file exists, the server creates a TCP socket, connects it to the TCP_Port of the client, and sends the file contents. 
After sending all the bytes of the file, closes (and destroys) the socket. 
The client receives the bytes and writes them in its local system; 
the closing of the socket by the server indicates the end of the file.

• put – The client sends the string put followed by a space and the name of the file in the server’s file system.
The server replies nack if the named file already exists or ack in the opposite case.
In the case of success, the server creates a TCP socket, connects it to the TCP_Port of the client and receives the file contents.
After sending all the bytes of the file, the client closes (and destroys) the socket. 
The server receives the bytes and writes them to its local system; 
the closing of the socket by the client indicates the end of the file.

Note: the nack reply is a message with the format nack error_number. 
For example, when trying to get a file that does not exist on the server it will send the message “nack 3”, where 3 is the error number.

"""