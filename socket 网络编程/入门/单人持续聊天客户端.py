import socket

client = socket.socket()

client.connect(('127.0.0.1', 20020))

while True:
    recv_msg = client.recv(1024).decode()
    print(recv_msg)
    if recv_msg.upper() == 'Q':
        break

    send_msg = input(">>>")
    client.send(send_msg.encode())
    if send_msg.upper() == 'Q':
        break

client.close()
