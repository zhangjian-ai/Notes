"""
协程
    协程，又称微线程，纤程。英文名Coroutine。一句话说明什么是协程：协程是一种用户态的轻量级线程。
    协程拥有自己的寄存器上下文和栈。协程调度切换时，将寄存器上下文和栈保存到其他地方，在切回来的时候，恢复先前保存的寄存器上下文和栈。因此：
    协程能保留上一次调用时的状态（即所有局部状态的一个特定组合），每次过程重入时，就相当于进入上一次调用的状态，换种说法：进入上一次离开时所处逻辑流的位置。

Gevent
    Gevent是基于协程的Python网络库

特性：
    基于libev的快速事件循环
    基于greenlet的轻量级执行单元
    重用Python标准库且概念相似的API
    支持SSL的协作socket
    通过c-ares或者线程池进行DNS查询
    使用标准库和第三方库中使用了阻塞socket的代码的能力
"""

# gevent.monkey.patch_all()  在文件开头执行，帮助实现协程遇到I/O时自动切换
#   - 因为协程间的切花是由用户控制，很多细小的I/O操作很难界定，所以引入该模块

import gevent
from gevent import monkey

monkey.patch_all()

# 如果项目使用的是gRPC协议，那么还需要在打标准库补丁之后，为gRPC的标准库打上补丁使其与gevent兼容
import my_grpc.experimental.gevent as grpc_gevent
grpc_gevent.init_gevent()


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

# g1.join()  # join 等待协程对象执行完成，阻塞当前线程

g2 = gevent.spawn(func2, 'zhangjian')

gevent.joinall([g1, g2])  # 批量等待协程结束。协程之间仍然是异步的

print("协程跑完了")  # 相对于主线程来说，join/joinall 是同步在执行，直到所有的协成执行完毕
