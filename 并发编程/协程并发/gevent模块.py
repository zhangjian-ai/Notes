# gevent.monkey.patch_all()  在文件开头执行，帮助实现协程遇到I/O时自动切换
#   - 因为协程间的切花是由用户控制，很多细小的I/O操作很难界定，所以引入该模块


# 如果项目使用的是gRPC协议，那么还需要在打补丁之前，为gRPC的标准库打上补丁使其与gevent兼容
import grpc.experimental.gevent as grpc_gevent
grpc_gevent.init_gevent()

import gevent
from gevent import monkey

monkey.patch_all()


def func():
    print("开启新协程：")
    print(gevent.getcurrent())
    gevent.sleep(1)
    print("关闭新协程：")


def func2(name):
    print("开启新协程：", name)
    print(gevent.getcurrent())
    gevent.sleep(2)
    print("关闭新协程：", name)


g1 = gevent.spawn(func)  # 单纯的开启一个协程，如果在当前线程无阻塞操作，则不会切换到该协程执行
# gevent.sleep(1)  # 有了阻塞就会切进去

# g1.join()  # join 等待协程对象执行完成

g2 = gevent.spawn(func2, 'zhangjian')

gevent.joinall([g1, g2])  # 批量等待协程结束。协程之间仍然是异步的

print("协程跑完了")  # 相对于主线程来说，join/joinall 是同步在执行，直到所有的协成执行完毕
