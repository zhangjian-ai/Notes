import time
from threading import Thread, current_thread, Lock, enumerate, active_count

count = 0


def consumer():
    time.sleep(1)
    global count
    count += 1
    # 获取当前线程对象
    t = current_thread()
    print(t.ident)
    print(t.getName())


# 面向对象开启线程
class MyThread(Thread):

    def __init__(self, a):
        self.a = a
        super().__init__()

    def run(self) -> None:
        count = 0
        while True:
            print("didi -> ", count)
            time.sleep(1)

            count += 1
            if count == 10:
                break


# 开启线程
t_list = []
# for i in range(10):
#     t = Thread(target=consumer, )
#     # print(t.getName())  # 线程名
#     t.start()
#     t_list.append(t)

for i in range(1):
    t = MyThread(i)
    t.start()
    t_list.append(t)

print(enumerate())  # 当前进程下所有激活的线程列表
print(active_count())  # 当前线程下激活的线程的数量

[t.join() for t in t_list]  # join() 阻塞 主线程，要等到 子线程都执行结束后，才继续执行 主线程

print("执行结束")
print(count)

# 注意：当开启子线程后，就算 主线程 执行完毕，进程也不会退出，因为 现成内部还有线程在执行。
#      只有当 进程 内部所有线程都退出后，进程才退出
