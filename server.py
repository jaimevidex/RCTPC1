""" The server is launched before the client using the following command:
python zftp-server UDP_SPort
where UDP_Sport is the UDP port used by the server to receive commands. """

"""
AS DEFENIÇOES DOS COMMANDOS GET E PUT NAO ESTAO MUITO BEM
PORQUE NAO PRECEBO O ENUNCIADO
"""

from socket import *
import sys
import os

serverUDPPort = int(sys.argv[1])
serverName = 'localhost'
bufferSize = 1024

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((serverName, serverUDPPort))
print("UDP server up and listening")
print()

while True:
    commandSentence, clientAddress = serverSocket.recvfrom(bufferSize)
    commandSentence = commandSentence.decode()
    print("Command received: " + commandSentence)
    print("From: " + str(clientAddress))
    print()

    tcpPort = 0 
    command = commandSentence.split()[0]

    messageToSend = ""

    match command:
        case 'open':
            messageToSend = open()       
        case 'close':
            messageToSend = "ack"
        case 'get':
            messageToSend = get()
        case 'put':
            messageToSend = put()
        case _:
            messageToSend = "nack 1"

    serverSocket.sendto(messageToSend.encode(), clientAddress)

    def open():
        message = ""
        if len(commandSentence.split()) != 2:
            message = "nack 1";  
        else:
            try:
                tcpPort = int(commandSentence.split()[1])
                message = "ack"
            except ValueError:
                message = "nack 2"
        return message

    def get():
        message = ""

        if len(commandSentence.split()) != 3:
            message = "nack 1"
        elif commandSentence.split()[1] in os.listdir():
            message = "nack 2"
        elif commandSentence.split()[1] not in os.listdir():
            message = "nack 3"
        else:

            tcpSocket = socket(AF_INET, SOCK_STREAM)
            tcpSocket.connect((serverName, tcpPort))
            tcpSocket.send(commandSentence.encode())
            file = open(commandSentence.split()[1], 'wb')
            while True:
                data = tcpSocket.recv(1024)
                if not data:
                    break
                file.write(data)
            file.close()    
            tcpSocket.close()

        return message

    def put():
        message = ""

        if len(commandSentence.split()) != 3:
            message = "nack 1"
        elif commandSentence.split()[1] in os.listdir():
            message = "nack 2"
        elif commandSentence.split()[1] not in os.listdir():
            message = "nack 3"
        else:

            tcpSocket = socket(AF_INET, SOCK_STREAM)
            tcpSocket.connect((serverName, tcpPort))
            tcpSocket.send(commandSentence.encode())
            file = open(commandSentence.split()[1], 'rb')
            while True:
                data = file.read(1024)
                if not data:
                    break
                tcpSocket.send(data)
            file.close()
            tcpSocket.close()

        return message