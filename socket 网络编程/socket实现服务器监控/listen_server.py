# -*- coding: utf-8 -*-
import socket
import threading
import time

import psutil

server = socket.socket()
# 如果服务器运行在docker容器内，那么监听地址改为"0.0.0.0"
addr = ('121.4.47.229', 8222)

server.bind(addr)
server.listen(10)


def get_net_speed(interval):
    net_msg = psutil.net_io_counters()
    bytes_sent, bytes_recv = net_msg.bytes_sent, net_msg.bytes_recv
    time.sleep(interval)
    net_msg = psutil.net_io_counters()
    bytes_sent2, bytes_recv2 = net_msg.bytes_sent, net_msg.bytes_recv
    send = str(round((((bytes_sent2 - bytes_sent) / interval) / 1024), 2))
    recv = str(round(((bytes_recv2 - bytes_recv) / interval) / 1024, 2))

    return send, recv


def collect(conn):
    # 收集服务器信息
    while True:
        rec = conn.recv(1024).decode('utf-8')
        if rec == 'next':
            memory = psutil.virtual_memory()
            cpu_used_percent = str(psutil.cpu_percent(interval=1, percpu=False))
            mem_used_percent = str(memory.percent)
            mem_used = str(round(memory.used / (1024.0 * 1024.0), 2))
            mem_available = str(round(memory.available / (1024.0 * 1024.0), 2))
            mem_free = str(round(memory.free / (1024.0 * 1024.0), 2))
            sent_speed, recv_speed = get_net_speed(1)

            msg = '-'.join(
                [cpu_used_percent, mem_used_percent, mem_used, mem_free, mem_available, sent_speed, recv_speed]).encode(
                'utf-8')

            conn.send(msg)
        elif rec == 'exit':
            conn.close()
            break


while True:
    conn, _ = server.accept()
    t = threading.Thread(target=collect, args=(conn,))
    t.start()
