import os

from locust import HttpUser, TaskSet, task


class Task(TaskSet):
    def on_start(self):
        print("前置操作，每个模拟用户开始执行task前都会执行")

    def on_stop(self):
        print("后置操作，每个模拟用户结束task后都会执行")

    @task
    def index(self):
        response = self.client.get('/')

        # 断言
        assert response.status_code == 200


class WebSite(HttpUser):
    tasks = [Task, ]  # 新版本用列表指定任务类
    host = 'https://www.baidu.com/'  # 这里写上host，在启动locust时就可以不写了
    min_wait = 2000
    max_wait = 3000  # task 每个用户执行两个任务间隔的上下限在2～3秒之间


if __name__ == '__main__':
    os.system('locust -f 百度首页测试.py ')
