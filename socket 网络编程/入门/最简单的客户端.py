import socket


def client():
    s = socket.socket()

    host = '127.0.0.1'
    port = 1234

    s.connect((host, port))

    while True:
        # 发送的消息只能是bytes类型
        text = input("发送消息到服务器:")
        s.send(text.encode())
        print("来自服务器的消息：", s.recv(1024).decode())  # 接收服务端的消息


if __name__ == '__main__':
    client()
