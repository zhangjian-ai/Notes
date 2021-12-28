import socket
import gevent
from gevent import monkey

monkey.patch_all()


def accept_conn(conn):
    while True:
        conn.send(b"hello")
        gevent.sleep(2)


server = socket.socket()
server.bind(('127.0.0.1', 9003))
server.listen()

while True:
    conn, _ = server.accept()
    gevent.spawn(accept_conn, conn)
