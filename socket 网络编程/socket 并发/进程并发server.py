import socket
import time

from multiprocessing import Process


def func(client):
    while True:
        time.sleep(2)
        client.send(b'hello')


if __name__ == '__main__':

    server = socket.socket()
    server.bind(('127.0.0.1', 19009))
    server.listen()

    while True:
        conn, _ = server.accept()
        # 每链接一个客户端，就为其开一个子进程
        Process(target=func, args=(conn,)).start()
