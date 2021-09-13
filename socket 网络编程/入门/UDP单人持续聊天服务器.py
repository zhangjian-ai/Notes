import socket

server = socket.socket(type=socket.SOCK_DGRAM)  # 指定协议类型为UDP，默认是TCP
server.bind(('127.0.0.1', 9001))

while True:
    # UDP无需创建链接可直接发送和接收消息
    resv_msg, origin = server.recvfrom(1024)  # 该接收函数多返回一个消息来源地址元组
    print(resv_msg.decode())

    send_msg = input(">>>")
    server.sendto(send_msg.encode(), origin)


# server.close()
