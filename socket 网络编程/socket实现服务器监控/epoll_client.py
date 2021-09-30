import socket

# 创建客户端socket对象
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 服务端IP地址和端口号元组
server_address = ('127.0.0.1', 8222)
# 客户端连接指定的IP地址和端口号
client.connect(server_address)

while True:
    # 输入数据
    data = input('please input:')
    # 客户端发送数据
    client.sendall(data.encode())
    # 客户端接收数据
    server_data = client.recv(1024)

    print("server >> ", server_data.decode())

    # 关闭客户端socket
    client.close()
