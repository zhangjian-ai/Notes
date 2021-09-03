import socket


def server():
    s = socket.socket()

    # host = socket.gethostname()
    # print(host)
    host = '127.0.0.1'
    port = 1234

    s.bind((host, port))  # 绑定IP和端口
    s.listen(5)  # 开始监听(最大建链数量)

    while True:
        c, addr = s.accept()  # 等待建链，返回一个与客户端双端通信的socket对象和客户端地址(ip,port)元组
        print("Got connection from", addr)
        c.send("Thank you for connecting".encode())  # 向客户端发送消息
        c.close()  # 关闭客户端链接


if __name__ == '__main__':
    # 启动服务器
    server()
