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


# 面上对象开启线程
class MyThread(Thread):

    def __init__(self, a):
        self.a = a
        super().__init__()

    def run(self) -> None:
        time.sleep(0.2)
        global count
        count += self.a


# 开启线程
t_list = []
for i in range(100):
    t = Thread(target=consumer, )
    # print(t.getName())  # 线程名
    t.start()
    t_list.append(t)

for i in range(50):
    t = MyThread(i)
    t.start()
    t_list.append(t)

print(enumerate())  # 当前进程下所有激活的线程列表
print(active_count())  # 当前线程下激活的线程的数量

[t.join() for t in t_list]

print("执行结束")
print(count)
