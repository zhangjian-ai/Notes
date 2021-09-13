import socket

client = socket.socket(type=socket.SOCK_DGRAM)

server = ('127.0.0.1', 9001)

while True:
    # 直接发
    send_msg = input(">>>")
    if send_msg.upper() == "Q":
        break

    # UDP需要指明接收地址
    client.sendto(send_msg.encode(), server)

    recv_msg = client.recv(1024).decode()
    print(recv_msg)
    if send_msg == "Q":
        break


client.close()

