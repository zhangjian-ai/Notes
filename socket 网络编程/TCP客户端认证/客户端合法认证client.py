# 1、验证客户端的合法性
import json
import socket
import hmac

secret_key = b'klfudsfeenrhifyd$67*ehn2v326hvsbaesa7!@'

client = socket.socket()

server = ('127.0.0.1', 9002)

client.connect(server)

# 接收服务器的随机字符串
string = client.recv(32)

# 根据规定的密钥和加密方法对串进行加密，并发送给服务器完成验证
# md5返回数据长度的是128bit
# hexdigest()方法是返回十六进制的字符串，所以长度为32
# digest()方式使返回二进制的字节串，所以长度为16
zy = hmac.new(secret_key, string, digestmod='MD5')
secret_str = zy.digest()

client.send(secret_str)

while True:
    msg = client.recv(1024).decode()
    if msg == '链接成功！':
        username = input("输入账号：")
        password = input("输入密码：")
        account = {
            'username': username,
            'password': password
        }
        account_bytes = json.dumps(account).encode()

        # 此处通过设置消息头来规避粘包问题
        header = {
            'type': 'login',
            'size': len(account_bytes)
        }
        header_str = json.dumps(header)

        # 包头定长处理
        header_bytes = header_str.zfill(32).encode()

        client.send(header_bytes + account_bytes)

        # 接受服务端返回信息
        msg = client.recv(1024).decode()
        if msg == "success":
            print("yes, it's ok")
            break
        else:
            break

client.close()
