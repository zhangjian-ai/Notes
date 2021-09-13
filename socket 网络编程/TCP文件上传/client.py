import json
import os
import socket
import struct
import sys


def login(client):
    while True:
        user = input("用户名：")
        pwd = input("密  码：")
        dic = {'user': user, 'pwd': pwd}

        if user and pwd:
            info_str, info_size = encode_dict(dic)
            client.send(info_size)
            client.send(info_str)
        else:
            continue

        content = client.recv(1024)
        msg = decode_bytes(content)

        if msg['type'] == 'login' and msg['code'] == 1:
            break


def encode_dict(dic):
    info_str = json.dumps(dic).encode()

    # 把info_str长度 封包成4位字节码。封包的最大长度是 2^31
    # i 表示四个章节； q 表示八个字节
    info_size = struct.pack('i', len(info_str))

    return info_str, info_size


def decode_bytes(content: bytes) -> dict:
    content = json.loads(content.decode().strip())
    return content


def get_file_info(file_path):
    name = os.path.basename(file_path)
    size = os.path.getsize(file_path)

    info = {'name': name, 'size': size}
    info_str, info_size = encode_dict(info)

    return info_size, info_str, size


def upload(client, file):
    info_bytes, info_str, size = get_file_info(file)
    # 发送文件信息
    client.send(info_bytes)
    client.send(info_str)

    # 读取文件内容并发送
    with open(file_path, 'rb') as fp:
        while size > 0:
            content = fp.read(1024)
            client.send(content)

            size -= len(content)


def operate():
    while True:
        index = input("选择要执行的操作：\n"
                      "upload: 1\n"
                      "download: 2\n")
        action_list = ["upload", "download"]

        action = action_list[int(index) - 1]

        if hasattr(sys.modules[__name__], action):
            # 调用当前运行模块中的方法
            getattr(sys.modules[__name__], action)(client, file_path)

            break


# ------------------主程序--------------------

client = socket.socket()
server = ('127.0.0.1', 9006)

# 连接服务器
client.connect(server)

# 文件路径
file_path = '/Users/zhangjian/Downloads/前端html css js jQuery阶段.zip'

# 登陆
login(client)

# 执行操作
operate()

client.close()
