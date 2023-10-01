from socket import *
import sys
from os import *

serverUDPPort = int(sys.argv[1])
serverName = 'localhost'
bufferSize = 1024

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((serverName, serverUDPPort))
print("UDP server up and listening")
print()

tcpPort = 0

def put(remoteFile):
    remoteFile = str(remoteFile)
    tcpSocket = socket(AF_INET, SOCK_STREAM)
    tcpSocket.connect((serverName, tcpPort))
    tcpSocket.send(commandSentence.encode())
    file = open(remoteFile, 'rb')
    while True:
        data = file.read(1024)
        if not data:
            break
        tcpSocket.send(data)
    file.close()
    tcpSocket.close()

def get(remoteFile):
    print(remoteFile)
    tcpSocket = socket(AF_INET, SOCK_STREAM)
    tcpSocket.connect((serverName, tcpPort))
    file = open(remoteFile, 'wb')
    while True:
        data = tcpSocket.recv(1024)
        if not data:
            break
        file.write(data)
    file.close()    
    tcpSocket.close()

while True:
    commandSentence, clientAddress = serverSocket.recvfrom(bufferSize)
    commandSentence = commandSentence.decode()
    print("Command received: " + commandSentence)
    print("From: " + str(clientAddress))
    print()

    command = commandSentence.split()[0]

    messageToSend = ""

    match command:
        case 'open':
            if tcpPort == 0:
                tcpPort = int(commandSentence.split()[1])
                messageToSend = "ack"
            else:
                messageToSend = "nack 2: already one client connected" 
        case 'close':
            tcpPort = 0
            messageToSend = "ack"      
        case 'put':
            remoteFile = commandSentence.split()[1]
            if path.exists(remoteFile):
                messageToSend = "nack 3: A file with the indicated name already exists on the server"
                continue
            else:
                put(remoteFile)
                messageToSend = "ack"
        case 'get':
            remoteFile = commandSentence.split()[1]
            if not path.exists(remoteFile):
                messageToSend = "nack 3: The indicated file does not exist on the server"
                continue
            else:
                get(remoteFile)
                messageToSend = "ack"
        case _:
            messageToSend = "this must never happen"

    serverSocket.sendto(messageToSend.encode(), clientAddress)