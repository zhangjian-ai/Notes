import json
import socket


# ------------------方法区--------------------
def check_file(conn):
    # 接收文件名称信息
    file_name = conn.recv(1024).decode()

    # 在库中查找文件信息，如果没有就新增
    with open('server_file.json', 'r') as fp:
        content = json.load(fp)

    file = content.get(file_name)
    if not file:
        content[file_name] = {'size': '0', 'type': file_name.rsplit('.', 1)[1]}

        with open('server_file.json', 'w') as fp:
            json.dump(content, fp)

    # 返回给客户端服务器文件的大小
    msg = content[file_name]['size'].encode()
    conn.send(msg)


def upload(conn):
    # 接收文件信息
    msg = conn.recv(1024).decode()
    file = json.loads(msg)
    name = file['name']
    size = file['size']

    # 保存到服务器
    with open('server_file.json', 'r') as fp:
        data = json.load(fp)
        current_size = int(data[name]['size'])

    with open(name, 'ab') as wp:
        # 设置超时时间，超过10s没有继续上传就算超时
        conn.settimeout(10)

        while size > current_size:
            try:
                content = conn.recv(1024)
            except:
                break

            wp.write(content)
            current_size += len(content)

        conn.settimeout(None)

    # 更新文件信息
    with open('server_file.json', 'w') as fp:
        data[name]['size'] = str(current_size)
        json.dump(data, fp)


# ------------------方法区--------------------


# ------------------主程序--------------------

server = socket.socket()  # 指定协议类型为UDP，默认是TCP
server.bind(('127.0.0.1', 9005))

server.listen()

# 等待链接
conn, addr = server.accept()

# 接收客户端要上传的文件名称，并返回服务端当前文件的大小
check_file(conn)

# 开始上传
upload(conn)

conn.close()
server.close()

# ------------------主程序--------------------
