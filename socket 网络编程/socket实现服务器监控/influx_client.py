# -*- coding: utf-8 -*-
"""
调用脚本需要传入三个命令行参数：监听时间(s)、服务器IP、端口号
python3 influx_client.py 120 127.0.0.1 8222
"""
import socket
import sys

from influxdb import InfluxDBClient

# 创建客户端socket对象
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 服务端IP地址和端口号元组
host = sys.argv[2]
port = sys.argv[3]
server_address = (host, int(port))
# 客户端连接指定的IP地址和端口号
socket.connect(server_address)

# 数据标题
title = ['cpu_used_rate.pct', 'mem_used_rate.pct', 'mem_used(MB)', 'mem_free(MB)', 'mem_available(MB)', 'receive(KB/S)', 'send(KB/S)']

# 监听时间 s
time = int(sys.argv[1])

# 实例化influx客户端
influx = InfluxDBClient(host="121.4.47.229",
                        port="8086",
                        username="influx",
                        password="influx",
                        database="jd_test")

while time > 0:
    # 客户端发送数据
    socket.send('next'.encode())
    # 客户端接收数据
    server_data = socket.recv(1024).decode('utf-8')
    data = server_data.split('-')

    # 拼装数据
    points = [
        {
            "measurement": "server",
            "tags": {
                "application": "CRM"
            },
            "fields": {key: float(value) for key, value in zip(title, data)},
        }
    ]
    influx.write_points(points)

    # 迭代时间
    time -= 1

socket.send('exit'.encode('utf-8'))
socket.close()
