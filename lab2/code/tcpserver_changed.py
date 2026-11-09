from socket import *
serverPort = 5202
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The server is ready to receive')
while True:
    connectionSocket, addr = serverSocket.accept()
    while True:
        sentence = connectionSocket.recv(1024).decode()
        if sentence=='':break
        print(sentence)
        capitalizedSentence="has print"
        connectionSocket.send(capitalizedSentence.encode())
    connectionSocket.close()
