# -*- coding: utf-8 -*-
'''
import select 导入select模块

epoll = select.epoll() 创建一个epoll对象

epoll.register(文件句柄,事件类型) 注册要监控的文件句柄和事件

事件类型:

　　select.EPOLLIN    可读事件

　　select.EPOLLOUT   可写事件

　　select.EPOLLERR   错误事件

　　select.EPOLLHUP   客户端断开事件

epoll.unregister(文件句柄)   销毁文件句柄

epoll.poll(timeout)  当文件句柄发生变化，则会以列表的形式主动报告给用户进程,timeout

                     为超时时间，默认为-1，即一直等待直到文件句柄发生变化，如果指定为1

                     那么epoll每1秒汇报一次当前文件句柄的变化情况，如果无变化则返回空

epoll.fileno() 返回epoll的控制文件描述符(Return the epoll control file descriptor)，即句柄

epoll.modfiy(fineno,event) fineno为文件描述符 event为事件类型  作用是修改文件描述符所对应的事件

epoll.fromfd(fileno) 从1个指定的文件描述符创建1个epoll对象

epoll.close()   关闭epoll对象的控制文件描述符
'''
import socket
import select
import time

# 创建socket对象
import psutil

server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
# 设置IP地址复用
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# ip地址和端口号
server_address = ("121.4.47.229", 8888)
# server_address = ("0.0.0.0", 8888)
# 绑定IP地址
server.bind(server_address)
# 监听，并设置最大连接数
server.listen(20)
# 服务端设置非阻塞
server.setblocking(False)
# 超时时间
timeout = 10
# 创建epoll事件对象，后续要监控的事件添加到其中
epoll = select.epoll()
# 注册服务器监听 fd 到等待 读事件 集合
epoll.register(server.fileno(), select.EPOLLIN)
# 文件句柄到所对应对象的字典，格式为{句柄：对象}
fd_to_socket = {server.fileno(): server, }


def get_net_speed(interval):
    net_msg = psutil.net_io_counters()
    bytes_sent, bytes_recv = net_msg.bytes_sent, net_msg.bytes_recv
    time.sleep(interval)
    net_msg = psutil.net_io_counters()
    bytes_sent2, bytes_recv2 = net_msg.bytes_sent, net_msg.bytes_recv
    send = str(round((((bytes_sent2 - bytes_sent) / interval) / 1024), 2))
    recv = str(round(((bytes_recv2 - bytes_recv) / interval) / 1024, 2))

    return send, recv


while True:
    # 轮询注册的事件集合，返回值为[(文件句柄，对应的事件)，(...),....]
    events = epoll.poll(timeout)
    if not events:  # 如果没有事件，则进入下一次循环
        continue

    for fd, event in events:
        socket = fd_to_socket.get(fd)

        # 如果活动socket为当前服务器socket，表示有新连接
        if socket == server:
            connection, address = server.accept()
            # 新连接socket设置为非阻塞
            connection.setblocking(False)
            # 注册新连接fd到待读事件集合
            epoll.register(connection.fileno(), select.EPOLLIN)
            # 把新连接的文件句柄以及对象保存到字典
            fd_to_socket[connection.fileno()] = connection

        # 关闭事件
        elif event & select.EPOLLHUP:
            # 在epoll中注销客户端的文件句柄
            epoll.unregister(fd)
            # 关闭客户端的文件句柄
            fd_to_socket[fd].close()
            # 删除文件描述符的映射
            del fd_to_socket[fd]

        # 可读事件
        elif event & select.EPOLLIN:
            # 接收数据
            data = socket.recv(1024).decode('utf-8')
            if data:
                if data == 'next':
                    # 修改收到消息的socket 到等待写事件集合(即对应 socket 收到消息后，再将其fd加入写事件集合)
                    epoll.modify(fd, select.EPOLLOUT)
                elif data == 'exit':
                    epoll.modify(fd, select.EPOLLHUP)

        # 可写事件
        elif event & select.EPOLLOUT:
            # 监听服务器信息并发送
            memory = psutil.virtual_memory()
            cpu_used_percent = str(psutil.cpu_percent(interval=1, percpu=False))
            mem_used_percent = str(memory.percent)
            mem_used = str(round(memory.used / (1024.0 * 1024.0), 2))
            mem_available = str(round(memory.available / (1024.0 * 1024.0), 2))
            mem_free = str(round(memory.free / (1024.0 * 1024.0), 2))
            sent_speed, recv_speed = get_net_speed(1)

            msg = '-'.join(
                [cpu_used_percent, mem_used_percent, mem_used, mem_free, mem_available, sent_speed,
                 recv_speed]).encode(
                'utf-8')

            socket.send(msg)

            # 重新绑定 fd 到 读事件集合
            epoll.modify(fd, select.EPOLLIN)

# 在epoll中注销服务端文件句柄
epoll.unregister(server.fileno())
# 关闭epoll
epoll.close()
# 关闭服务器socket
server.close()
