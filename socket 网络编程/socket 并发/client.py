import socket

client = socket.socket()

client.connect(('127.0.0.1', 9003))

while True:
    msg = client.recv(1024).decode()
    print(msg)
