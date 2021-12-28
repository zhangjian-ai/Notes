import os
import time
from multiprocessing import Process

print(os.getpid(), os.getppid(), '1')


def func(name):
    time.sleep(1)
    # 打印当前进程ID、父进程ID
    print(os.getpid(), os.getppid(), '3')
    print(name)
    print(__name__)


if __name__ == '__main__':
    print(__name__)
    # 打印当前进程的ID, 父进程ID
    print(os.getpid(), os.getppid(), '2')

    # 创建一个子进程，args为一个元组，为函数传参
    p = Process(target=func, args=('zhangjian',))

    # 异步非阻塞的方式启动子进程
    p.start()

    # 主动让子进程同步到主进程
    p.join()
else:
    print("子进程：" + __name__)


'''
打印结果说明：
    52611 19029 1  # 运行 py文件，开启进程，打印一次'1'。当前进程为运行中的py文件；父进程为pycharm
    __main__
    52611 19029 2  # 执行到判断条件if __name__ == '__main__': ，条件为真，执行if下面的代码，打印一次'2'，当前进程仍然是py文件
    52613 52611 1  # 继续执行，unix/linux中以fork的方式开启子进程。
                    - 经过fork()以后，父进程和子进程拥有相同内容的代码段、数据段和用户堆栈，就像父进程把自己克隆了一遍。
                    - 事实上，父进程只复制了自己的PCB块。而代码段，数据段和用户堆栈内存空间并没有复制一份，而是与子进程共享。
                    - PCB(Process Control Block):使一个在多道程序环境下不能独立运行的程序（包含数据），成为一个能独立运行的基本单位，一个能与其它进程并发执行的进程。
                    此时，在子进程中再次执行 入门.py 文件，启动子进程，再次打印'1'，但此时的进程是一个新的进程了，父进程则是开启当前进程的py文件
    子进程：__mp_main__  # 此时子进程不满足 if 条件，在调用 入门.py 时，就进入else逻辑
    52613 52611 3  # 入门.py 执行完之后，子进程再调用 func函数，打印一次'3'
    zhangjian      # 继续打印一次参数
    __mp_main__    
'''

