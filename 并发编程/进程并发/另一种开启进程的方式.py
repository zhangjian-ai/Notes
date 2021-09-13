import os
import time
from multiprocessing import Process


class MyProcess(Process):

    def __init__(self, *args):
        super().__init__()
        self.args = args

    def run(self) -> None:
        """
        继承方式下，子进程要完成的代码放这里
        :return:
        """
        time.sleep(2)
        print(os.getpid(), os.getppid())
        print(self.args)


if __name__ == '__main__':
    print(os.getpid(), os.getppid())
    p = MyProcess('zhangjian', 'lilei')
    p.start()

    # join方法：让异步的子进程同步到主进程执行，所以调用join后，会等待子进程结束才会继续执行主进程
    p.join()

    print("主进程结束")
