from socket import *
serverPort = 5201
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("The server is ready to receive")
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    print(message.decode())
    responseMessage="has print"
    serverSocket.sendto(responseMessage.encode(), clientAddress)