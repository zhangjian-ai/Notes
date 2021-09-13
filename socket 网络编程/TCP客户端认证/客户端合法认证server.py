import hmac
import json
import os
import socket

secret_key = b'klfudsfeenrhifyd$67*ehn2v326hvsbaesa7!@'

server = socket.socket()
server.bind(('127.0.0.1', 9002))
server.listen()

conn, addr = server.accept()

# 获取随机字符串
random_str = os.urandom(32)  # 返回一个32字节的bytes类型字符串

conn.send(random_str)

# 验证客户端的加密信息
verify_info = conn.recv(16)

zy = hmac.new(secret_key, random_str, digestmod='MD5')
secret_str = zy.digest()

if secret_str == verify_info:
    conn.send('链接成功！'.encode())

    # 接收登陆信息
    receive = conn.recv(1024)

    # 解析包头
    header = receive[0: 32]
    header_dict = json.loads(header.decode().lstrip('0'))

    # 解析正文
    if header_dict['type'] == 'login':
        content = json.loads(receive[32:32 + header_dict['size']].decode())

        print(content['username'])
        print(content['password'])

        conn.send("success".encode())
        conn.close()
else:
    conn.send('链接失败！'.encode())
    conn.close()
