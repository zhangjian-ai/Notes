import json
import socket
import struct
import hashlib


def get_dict():
    # 获取上传文件信息。通过先上传文件描述信息长度，来规避粘包
    len_msg = conn.recv(4)  # 文件描述信息字节码长度固定为4
    info_len = struct.unpack('i', len_msg)  # 将编码解包成实际长度

    file_info = json.loads(conn.recv(int(info_len[0])).decode())

    return file_info


def auth():
    while True:
        dic = get_dict()
        user, pwd = dic['user'], dic['pwd']

        username = 'zhangjian'
        password = b"\xa1\xcf\x0c\xf8'V\xf6\xcf\x05-\xf26\xbf\xcf\xa2\xfe"

        # 把用户名字节码当作盐加到对象中，加强密码的安全性
        # 返回一个新的类
        md5 = hashlib.md5(user.encode('utf-8'))
        # 添加要加密的字节码
        md5.update(pwd.encode())
        # 获得密文
        content = md5.digest()

        if user == username and password == content:
            res, _ = encode_dict({'type': 'login', 'code': 1})
            conn.send(res)
            break
        else:
            res, _ = encode_dict({'type': 'login', 'code': 0})
            conn.send(res)


def encode_dict(dic):
    info_str = json.dumps(dic).encode()

    # 把info_str长度 封包成4位字节码。封包的最大长度是 2^31
    # i 表示四个章节； q 表示八个字节
    info_size = struct.pack('i', len(info_str))

    return info_str, info_size


def upload():
    file_info = get_dict()
    # 保存到服务器
    with open("upload" + file_info['name'], 'wb') as fp:
        while file_info['size'] > 0:
            content = conn.recv(1024)
            fp.write(content)

            # 当接收完了文本大小的内容则退出
            # 由于tcp在传输过程中会切块发送，所以即便客户端每次都发1024字节，但服务器接收的很可能没有1024
            # 所以要以实际接收到的字节长度来计算退出条件
            file_info['size'] -= len(content)


# ------------------主程序--------------------

server = socket.socket()  # 指定协议类型为UDP，默认是TCP
server.bind(('127.0.0.1', 9006))

server.listen()

# 等待链接
conn, addr = server.accept()

# 登陆认证
auth()

upload()

conn.close()
server.close()
