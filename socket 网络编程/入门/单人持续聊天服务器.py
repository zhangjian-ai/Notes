import socket

server = socket.socket()

server.bind(('127.0.0.1', 20020))
server.listen()

while True:
    conn, addr = server.accept()
    print("Got connection from:", addr)
    while True:
        send_msg = input(">>>")
        conn.send(send_msg.encode())
        if send_msg.upper() == 'Q':
            break
        recv_msg = conn.recv(1024).decode()
        print(recv_msg)
        if recv_msg.upper() == 'Q':
            break
    conn.close()  # 断开server到client的链接

# server.close()  # 服务器关闭
