import socket

client = socket.socket()

server = ('127.0.0.1', 9004)

client.connect(server)

while True:
    content = client.recv(1024)

    print(content.decode())
