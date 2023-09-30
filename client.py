from socket import *
import sys
from os import *

serverUDPPort = int(sys.argv[2])
serverName = str(sys.argv[1])
bufferSize = 1024

serverAddress = (serverName, serverUDPPort)
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.connect(serverAddress)

while True:
    commandSentence = input("Insert command: ")

    command = commandSentence.split()[0]

    if command == "close":
        clientSocket.send(commandSentence.encode())
        print("Connection closed")
        break
    
    elif command == "open":
        if len(commandSentence.split()) != 2:
            print("Connection refused with error: nack 1: Invalid number of arguments")
        elif len(commandSentence.split()[1]) != 5:
            print("Connection refused with error: nack 2: Invalid port number")
        else:
            clientSocket.send(commandSentence.encode())
            response, serverAddress = clientSocket.recvfrom(bufferSize)
            response = response.decode()
            if response == "ack":
                print("Connection established")
                tcpSocket = socket(AF_INET, SOCK_STREAM)
                tcpSocket.bind((serverName, int(commandSentence.split()[1])))
                tcpSocket.listen(1)   
            else:
                print("Connection refused with error: " + response)
        continue        
    
    else:
        if len(commandSentence.split()) != 3:
            print("Connection refused with error: nack 1: Invalid number of arguments")
            continue
        if command == "put":
            localFile = commandSentence.split()[1]
            remoteFile = commandSentence.split()[2]
            if not path.exists(localFile):
                print("Connection refused with error: nack 2: The indicated file does not exist on the client")
                continue
            else:
                newMessage = command + " " + remoteFile
                clientSocket.send(newMessage.encode())
                response, serverAddress = clientSocket.recvfrom(bufferSize)
                response = response.decode()
                if response == "nack 3":
                    print("Connection refused with error: nack 3: A file with the indicated name already exists on the server")
                if response == "ack":
                    localFile = open(localFile, 'rb')
                    connSocket, addr = tcpSocket.accept()
                    while True:
                        data = connSocket.recv(bufferSize)
                        if not data:
                            break
                        localFile.write(data)
                    localFile.close()
                    connSocket.close()
                    tcpSocket.close()
                    print("File uploaded")
        elif command == "get":
            localFile = commandSentence.split()[2]
            remoteFile = commandSentence.split()[1]
            if path.exists(localFile):
                print("Connection refused with error: nack 2: A file with the indicated name already exists on the client")
            else:
                newMessage = command + " " + remoteFile
                clientSocket.send(newMessage.encode())
                response, serverAddress = clientSocket.recvfrom(bufferSize)
                response = response.decode()
                if response == "nack 3":
                    print("Connection refused with error: nack 3: The indicated file does not exist on the server")
                if response == "ack":
                    localFile = open(localFile, 'wb')
                    connSocket, addr = tcpSocket.accept()
                    while True:
                        data = connSocket.recv(bufferSize)
                        if not data:
                            break
                        localFile.write(data)
                    localFile.close()
                    connSocket.close()
                    tcpSocket.close()
                    print("File downloaded")
clientSocket.close()