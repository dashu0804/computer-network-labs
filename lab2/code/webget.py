
"""
webget.py —— 用 Python 标准库 socket 实现的HTTP客户端（实验2 Part D）
功能：
    向指定 HTTP 服务器发起一次 GET 请求，接收完整响应；打印状态行与全部响应头，
    并统计每一次 recv 的字节数和调用总次数；最后把响应体 body 以二进制写入 out.bin。

用法：
    python webget.py <host> <path> [port]
    port 省略时默认为 80。

仓库地址：
    https://github.com/dashu0804/computer-network-labs

    作者：251006108 柳松阳
"""
import socket
import sys
if len(sys.argv) < 3:
    print('用法: python webget.py host path [port]')
    sys.exit(1)
host = sys.argv[1]
path = sys.argv[2]
port = int(sys.argv[3]) if len(sys.argv) > 3 else 80
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)
s.connect((host, port))
req = b"GET " + path.encode() + b" HTTP/1.1\r\n"
req += b"Host: " + host.encode() + b"\r\n"
req += b"Connection: close\r\n"
req += b"\r\n"
s.sendall(req)
buffer = b''
recv = 0
head = None
content_length = 0
while True: #持续接收直到接受内容为空或超出接收大小限制
    chunk = s.recv(4096)
    recv += 1
    print('第 %d 次 recv：%d 字节' % (recv, len(chunk)))
    if chunk == b'':#确保进入解析的内容非空
        break#对端关闭
    buffer += chunk
    if head is None and b'\r\n\r\n' in buffer:#空行是头和 body 的分界；head is None 保证只解析一次
        head, body = buffer.split(b'\r\n\r\n', 1)
        for line in head.split(b'\r\n')[1:]:
            if line.lower().startswith(b'content-length:'):
                content_length = int(line.split(b':', 1)[1].strip())
        lines = head.decode('utf-8', 'ignore').split('\r\n')
        print('状态行:', lines[0])
        for h in lines[1:]:
            print('   ', h)
        print('Content-Length =', content_length)
    if head is not None and content_length and len(buffer) - len(head) - 4 >= content_length:
        with open('out.bin', 'wb') as f:
            f.write(buffer.split(b'\r\n\r\n', 1)[1])
        break#content收满
print('总共 recv %d 次，累计 %d 字节' % (recv, len(buffer)))
if head is not None:
    with open('out.bin', 'wb') as f:
        f.write(buffer.split(b'\r\n\r\n', 1)[1])
s.close()
