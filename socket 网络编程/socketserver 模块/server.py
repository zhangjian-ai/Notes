# socketserver模块基于socket实现，主要实现tcp并发链接

import socketserver
import time


class MyServer(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        conn = self.request
        print(conn)

        while True:
            conn.send("你好".encode())
            time.sleep(1)


server = socketserver.ThreadingTCPServer(('127.0.0.1', 9004), MyServer)
server.serve_forever()

