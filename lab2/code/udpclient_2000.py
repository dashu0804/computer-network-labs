import sys
from socket import *
SERVER_NAME = '172.26.128.1'
SERVER_PORT = 5201
PAYLOAD_FILE = 'payload2000.txt'
def main():
    try:
        with open(PAYLOAD_FILE, 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        print('找不到文件:', PAYLOAD_FILE)
        print('请先在本脚本同目录执行：')
        print("  $s = 'A' * 2000")
        print("  Set-Content -Path payload2000.txt -Value $s -NoNewline -Encoding ascii")
        sys.exit(1)
    print('文件字节数 =', len(data))
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    sent = clientSocket.sendto(data, (SERVER_NAME, SERVER_PORT))
    print('内核已接受发送字节数 =', sent)
    print('本端临时端口 =', clientSocket.getsockname()[1])
    print('目标 =', SERVER_NAME, ':', SERVER_PORT)
    clientSocket.close()
    print('已关闭 socket')
if __name__ == '__main__':
    main()
