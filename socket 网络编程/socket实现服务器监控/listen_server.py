import socket
import threading
import time

import psutil

server = socket.socket()
# 如果服务器运行在docker容器内，那么监听地址改为"0.0.0.0"
addr = ('127.0.0.1', 8887)

server.bind(addr)
server.listen(10)


def get_net_speed(interval):
    net_msg = psutil.net_io_counters()
    bytes_sent, bytes_recv = net_msg.bytes_sent, net_msg.bytes_recv
    time.sleep(interval)
    net_msg = psutil.net_io_counters()
    bytes_sent2, bytes_recv2 = net_msg.bytes_sent, net_msg.bytes_recv
    sent_speed = (bytes_sent2 - bytes_sent) / interval
    sent_speed = str(round((sent_speed / 1048576), 2)) + " MB/s" if sent_speed >= 1048576 else str(
        round((sent_speed / 1024), 2)) + " KB/s"
    recv_speed = (bytes_recv2 - bytes_recv) / interval
    recv_speed = str(round((recv_speed / 1048576), 2)) + " MB/s" if recv_speed >= 1048576 else str(
        round(recv_speed / 1024, 2)) + " KB/s"

    return sent_speed, recv_speed


def collect(conn):
    # 收集服务器信息
    while True:
        rec = conn.recv(1024).decode('utf-8')
        if rec == 'next':
            memory = psutil.virtual_memory()
            cpu_used_percent = str(psutil.cpu_percent(interval=1, percpu=False)) + '%'
            mem_used_percent = str(memory.percent) + '%'
            mem_used = str(round(memory.used / (1024.0 * 1024.0 * 1024.0), 2)) + "Gb"
            mem_available = str(round(memory.available / (1024.0 * 1024.0 * 1024.0), 2)) + "Gb"
            mem_free = str(round(memory.free / (1024.0 * 1024.0 * 1024.0), 2)) + "Gb"
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
