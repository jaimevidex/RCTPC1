""" Clients are invoked by a command line such as:
python zftp-client server_name UDP_Sport
where server_name is the name of the server and UDP_Sport is the server port. """

from socket import *
import sys

serverUDPPort = int(sys.argv[2])
serverName = str(sys.argv[1])

serverAddress = (serverName, serverUDPPort)
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.connect(serverAddress)

def main():
    pass

main()
""" 
• open – this command starts an interaction session, sending to the server 
the TCP port number where the client will be waiting for connections.
Syntax: Errors:
Example:
open <port>
(1) invalid number of arguments; (2) invalid port number;
open 55555

• close – this command ends an interaction session. Syntax: close
Example: close

• get – this command downloads a file from the server, this means to transfer a 
file from the server file system to the client ́s file system.
Syntax: Errors:
Example:
get <remote_filename> <local_filename>
(1) invalid number of arguments;
(2) a file with the indicated name already exists on the client;
(3) the indicated file does not exist on the server;
get test1.pdf my_test1.pdf

• put – this command uploads a file to the server, this means 
transfer a file in the client file system to the server ́s file system.
Syntax: Errors:
Example:
put <local_filename> <remote_filename>
(1) invalid number of arguments;
(2) the indicated file does not exist on the client;
(3) a file with the indicated name already exists on the server; put my_test1.pdf test1_server.pdf 

"""