import json
import os
import socket

# ------------------方法区--------------------
import time


def get_file_info(file_path):
    name = os.path.basename(file_path)
    size = int(os.path.getsize(file_path))

    return name, size


def upload(client, name, current_size, size):
    # 发送文件信息
    info = {'name': name, 'size': size}
    client.send(json.dumps(info).encode())

    # 读取文件内容并发送
    with open(file_path, 'rb') as fp:
        data = fp.read()

        while size - current_size > 0:
            time.sleep(0.0002)
            content = data[current_size: current_size + 1024]
            client.send(content)

            current_size += len(content)


# ------------------方法区--------------------


# ------------------主程序--------------------

client = socket.socket()
server = ('127.0.0.1', 9005)

# 连接服务器
client.connect(server)

# 文件路径
file_path = '/Users/zhangjian/Documents/西吉包菜上市啦！.mp4'

# 发送文件名到服务器获取已经上传的文件大小
name, size = get_file_info(file_path)
client.send(name.encode())
current_size = int(client.recv(1024).decode())

# 开始上传
upload(client, name, current_size, size)

client.close()

# ------------------主程序--------------------
